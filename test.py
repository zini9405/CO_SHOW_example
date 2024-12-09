import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
import glob
import os
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter


# Custom Dataset for loading multiple .npy files and applying masking for -9999 values
class MaskedWaferDataset(Dataset):
    def __init__(self, data_dir, window_size=3, mask_value=-9999):
        self.data_files = sorted(glob.glob(os.path.join(data_dir, "*_data.npy")))
        self.label_files = sorted(glob.glob(os.path.join(data_dir, "*_labels.npy")))
        self.window_size = window_size
        self.mask_value = mask_value

        # Load all data and labels into memory
        self.data = []
        self.labels = []
        for data_file, label_file in zip(self.data_files, self.label_files):
            data = np.load(data_file)  # Shape: [Num Sequences, Steps, Features]
            labels = np.load(label_file)  # Shape: [Num Sequences]
            self.data.append(data)
            self.labels.append(labels)

        # Concatenate all data and labels
        self.data = np.concatenate(self.data, axis=0)
        self.labels = np.concatenate(self.labels, axis=0)

    def __len__(self):
        return len(self.data) - self.window_size + 1

    def __getitem__(self, idx):
        data_window = self.data[idx:idx + self.window_size]  # Shape: [Window Size, Steps, Features]
        label_window = self.labels[idx:idx + self.window_size]  # Shape: [Window Size]

        # Apply masking
        mask = data_window != self.mask_value  # Mask for valid values
        masked_data_window = data_window * mask  # Zero out invalid values

        # Use the label of the last sequence in the window as the target
        return (
            torch.tensor(masked_data_window, dtype=torch.float32),
            torch.tensor(label_window[-1], dtype=torch.float32),
            torch.tensor(mask, dtype=torch.bool),
        )


# Transformer model definition
class FullMultiLevelTransformer(nn.Module):
    def __init__(self, input_dim, steps, window_size, d_model=64, nhead=4, num_layers=2, dim_feedforward=128, dropout=0.1):
        super(FullMultiLevelTransformer, self).__init__()
        self.steps = steps
        self.window_size = window_size

        self.feature_embedding = nn.Linear(1, d_model)
        self.feature_transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout),
            num_layers=num_layers
        )

        self.step_embedding = nn.Linear(input_dim, d_model)
        self.step_transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout),
            num_layers=num_layers
        )

        self.time_transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout),
            num_layers=num_layers
        )

        self.fc = nn.Linear(d_model, 1)

    def forward(self, x, mask):
        batch_size, window_size, steps, features = x.size()

        # Apply mask to ignore -9999 values
        x = x * mask.float()  # Zero out -9999 values in the input

        # --- Feature Transformer: 변수 간 관계 학습 ---
        x = x.view(batch_size * window_size * steps, features, 1)
        x = self.feature_embedding(x)
        x = x.permute(1, 0, 2)
        x = self.feature_transformer(x)
        x = x[-1, :, :]

        # --- Step Transformer: Step 간 관계 학습 ---
        x = x.view(batch_size * window_size, steps, -1)
        x = x.permute(1, 0, 2)
        x = self.step_transformer(x)
        x = x[-1, :, :]

        # --- Time Transformer: 웨이퍼 간 시간축 관계 학습 ---
        x = x.view(batch_size, window_size, -1)
        x = x.permute(1, 0, 2)
        x = self.time_transformer(x)
        x = x[-1, :, :]

        output = self.fc(x)
        return output


# Masked MSE Loss
def masked_mse_loss(output, target, mask):
    valid_mask = mask.any(dim=[1, 2, 3])  # Reduce mask to valid samples
    valid_output = output[valid_mask]  # Predictions for valid samples
    valid_target = target[valid_mask]  # Ground truth for valid samples
    return torch.mean((valid_output - valid_target) ** 2)


# Accuracy calculation
def calculate_accuracy(output, target, threshold=1.0):
    correct = torch.abs(output - target) <= threshold
    return correct.sum().item() / len(target)


# Train/Val split
def train_val_split(dataset, val_ratio=0.2):
    val_size = int(len(dataset) * val_ratio)
    train_size = len(dataset) - val_size
    return random_split(dataset, [train_size, val_size])


# Training loop
def train_model_with_masked_inputs(model, train_loader, val_loader, criterion, optimizer, num_epochs, device, log_dir):
    writer = SummaryWriter(log_dir)
    model.to(device)

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        total_accuracy = 0.0

        for batch_data, batch_labels, batch_masks in tqdm(train_loader, desc=f"Training Epoch {epoch + 1}/{num_epochs}"):
            batch_data, batch_labels, batch_masks = batch_data.to(device), batch_labels.to(device), batch_masks.to(device)

            # Forward pass with masking
            outputs = model(batch_data, batch_masks)

            # Compute loss
            loss = criterion(outputs.squeeze(), batch_labels, batch_masks)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            # Calculate accuracy
            accuracy = calculate_accuracy(outputs.squeeze(), batch_labels)
            total_accuracy += accuracy

        avg_train_loss = running_loss / len(train_loader)
        avg_train_accuracy = total_accuracy / len(train_loader)
        writer.add_scalar("Loss/Train", avg_train_loss, epoch)
        writer.add_scalar("Accuracy/Train", avg_train_accuracy, epoch)
        print(f"Epoch [{epoch + 1}/{num_epochs}], Train Loss: {avg_train_loss:.4f}, Train Accuracy: {avg_train_accuracy:.4f}")

        # Validation step
        model.eval()
        val_loss = 0.0
        val_accuracy = 0.0
        with torch.no_grad():
            for batch_data, batch_labels, batch_masks in val_loader:
                batch_data, batch_labels, batch_masks = batch_data.to(device), batch_labels.to(device), batch_masks.to(device)
                outputs = model(batch_data, batch_masks)
                loss = criterion(outputs.squeeze(), batch_labels, batch_masks)
                val_loss += loss.item()

                # Calculate accuracy
                accuracy = calculate_accuracy(outputs.squeeze(), batch_labels)
                val_accuracy += accuracy

        avg_val_loss = val_loss / len(val_loader)
        avg_val_accuracy = val_accuracy / len(val_loader)
        writer.add_scalar("Loss/Validation", avg_val_loss, epoch)
        writer.add_scalar("Accuracy/Validation", avg_val_accuracy, epoch)
        print(f"Epoch [{epoch + 1}/{num_epochs}], Validation Loss: {avg_val_loss:.4f}, Validation Accuracy: {avg_val_accuracy:.4f}")

    writer.close()


# Main
data_dir = "processed"
window_size = 3
batch_size = 8
num_epochs = 10
learning_rate = 1e-3
log_dir = "logs"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

dataset = MaskedWaferDataset(data_dir, window_size=window_size)
train_dataset, val_dataset = train_val_split(dataset, val_ratio=0.2)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

model = FullMultiLevelTransformer(input_dim=36, steps=13, window_size=3, d_model=64, nhead=4, num_layers=2, dim_feedforward=128)
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

train_model_with_masked_inputs(
    model=model,
    train_loader=train_loader,
    val_loader=val_loader,
    criterion=masked_mse_loss,
    optimizer=optimizer,
    num_epochs=num_epochs,
    device=device,
    log_dir=log_dir,
)