import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter

# MaskedWaferDataset 클래스 재사용
class MaskedWaferDataset(Dataset):
    def __init__(self, data_dir, window_size=3, mask_value=-9999):
        """
        Args:
            data_dir: Directory containing .npy files (both data and labels).
            window_size: Number of overlapping sequences to include in each sample.
            mask_value: Value to be masked in the dataset.
        """
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
        # Ensure we have enough sequences for the window size
        return len(self.data) - self.window_size + 1

    def __getitem__(self, idx):
        # Extract overlapping window of sequences
        data_window = self.data[idx:idx + self.window_size]  # Shape: [Window Size, Steps, Features]
        label_window = self.labels[idx:idx + self.window_size]  # Shape: [Window Size]

        # Apply masking
        mask = data_window != self.mask_value  # Create mask for valid values
        masked_data_window = data_window * mask  # Zero out invalid values

        # Use the label of the last sequence in the window as the target
        return (
            torch.tensor(masked_data_window, dtype=torch.float32),
            torch.tensor(label_window[-1], dtype=torch.float32),
            torch.tensor(mask, dtype=torch.bool),  # Include the mask for further processing if needed
        )

# Transformer 모델 정의
class FullMultiLevelTransformer(nn.Module):
    def __init__(self, input_dim, steps, window_size, d_model=64, nhead=4, num_layers=2, dim_feedforward=128, dropout=0.1):
        super(FullMultiLevelTransformer, self).__init__()
        self.steps = steps
        self.window_size = window_size

        # Feature Transformer: 변수 간 관계 학습
        self.feature_embedding = nn.Linear(1, d_model)
        self.feature_transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout),
            num_layers=num_layers
        )

        # Step Transformer: Step 간 관계 학습
        self.step_embedding = nn.Linear(input_dim, d_model)
        self.step_transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout),
            num_layers=num_layers
        )

        # Time Transformer: 웨이퍼 간 시간축 관계 학습
        self.time_transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout),
            num_layers=num_layers
        )

        # Output layer
        self.fc = nn.Linear(d_model, 1)

    def forward(self, x):
        batch_size, window_size, steps, features = x.size()

        # --- Feature Transformer: 변수 간 관계 학습 ---
        x = x.view(batch_size * window_size * steps, features, 1)  # [Batch * Window * Step, Features, 1]
        x = self.feature_embedding(x)  # [Batch * Window * Step, Features, d_model]
        x = x.permute(1, 0, 2)  # [Features, Batch * Window * Step, d_model]
        x = self.feature_transformer(x)  # [Features, Batch * Window * Step, d_model]
        x = x[-1, :, :]  # 마지막 Feature 출력 사용 [Batch * Window * Step, d_model]

        # --- Step Transformer: Step 간 관계 학습 ---
        x = x.view(batch_size * window_size, steps, -1)  # [Batch * Window, Steps, d_model]
        x = x.permute(1, 0, 2)  # [Steps, Batch * Window, d_model]
        x = self.step_transformer(x)  # [Steps, Batch * Window, d_model]
        x = x[-1, :, :]  # 마지막 Step 출력 사용 [Batch * Window, d_model]

        # --- Time Transformer: 웨이퍼 간 시간축 관계 학습 ---
        x = x.view(batch_size, window_size, -1)  # [Batch, Window, d_model]
        x = x.permute(1, 0, 2)  # [Window, Batch, d_model]
        x = self.time_transformer(x)  # [Window, Batch, d_model]
        x = x[-1, :, :]  # 마지막 Window 출력 사용 [Batch, d_model]

        # Output layer
        output = self.fc(x)  # [Batch, 1]
        return output

# Train/Val Split 함수
def train_val_split(dataset, val_ratio=0.2):
    val_size = int(len(dataset) * val_ratio)
    train_size = len(dataset) - val_size
    return random_split(dataset, [train_size, val_size])

# 학습 함수
def train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs, device, log_dir):
    writer = SummaryWriter(log_dir)  # TensorBoard
    model.to(device)

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for batch_data, batch_labels, _ in tqdm(train_loader, desc=f"Training Epoch {epoch + 1}/{num_epochs}"):
            batch_data, batch_labels = batch_data.to(device), batch_labels.to(device)

            # Forward pass
            outputs = model(batch_data)
            loss = criterion(outputs.squeeze(), batch_labels)

            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        avg_train_loss = running_loss / len(train_loader)
        writer.add_scalar("Loss/Train", avg_train_loss, epoch)
        print(f"Epoch [{epoch + 1}/{num_epochs}], Train Loss: {avg_train_loss:.4f}")

        # Validation step
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for batch_data, batch_labels, _ in val_loader:
                batch_data, batch_labels = batch_data.to(device), batch_labels.to(device)
                outputs = model(batch_data)
                loss = criterion(outputs.squeeze(), batch_labels)
                val_loss += loss.item()

        avg_val_loss = val_loss / len(val_loader)
        writer.add_scalar("Loss/Validation", avg_val_loss, epoch)
        print(f"Epoch [{epoch + 1}/{num_epochs}], Validation Loss: {avg_val_loss:.4f}")

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
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs, device, log_dir)