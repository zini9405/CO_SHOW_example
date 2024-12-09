import os
import pandas as pd
import torch
import matplotlib.pyplot as plt
from tqdm import tqdm
from torch.utils.data import Dataset, DataLoader, random_split


# 데이터 매핑 함수
def map_to_numeric(values):
    return {val: idx for idx, val in enumerate(sorted(values))}


# Custom Dataset 정의
class CustomDataset(Dataset):
    def __init__(self, df):
        self.data = df
        self.filtered_data = self.data[self.data['STEP_NAME'] == 'DEPO']
        self.labels = self.filtered_data['SFQR_AFS2'].values
        self.features = self.filtered_data.drop(
            columns=['SFQR_AFS2', 'STEP_NAME', "WAF_ID", "HST_REG_DTTM", 'STEP_ID']
        ).values

    def __len__(self):
        return len(self.filtered_data)

    def __getitem__(self, idx):
        return (
            torch.tensor(self.features[idx], dtype=torch.float32),
            torch.tensor(self.labels[idx], dtype=torch.float32),
        )


# Transformer 모델 정의
class FullMultiLevelTransformer(torch.nn.Module):
    def __init__(self, input_dim, d_model=64, nhead=4, num_layers=6, dim_feedforward=128):
        super(FullMultiLevelTransformer, self).__init__()
        self.feature_embedding = torch.nn.Linear(input_dim, d_model)
        self.feature_transformer = torch.nn.TransformerEncoder(
            torch.nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward),
            num_layers=num_layers,
        )
        self.fc = torch.nn.Linear(d_model, 1)

    def forward(self, x):
        x = self.feature_embedding(x)
        x = x.unsqueeze(1)  # (batch_size, seq_len=1, d_model)
        x = self.feature_transformer(x)
        x = x.mean(dim=1)  # (batch_size, d_model)
        return self.fc(x)


# 손실 함수
def mse_loss(output, target):
    return torch.mean((output - target) ** 2)


# 정확도 계산 함수
def calculate_accuracy(output, target, threshold=0.5):
    correct = torch.abs(output - target) <= threshold
    return correct.sum().item() / len(target)


# Train/Validation Split
def train_val_split(dataset, val_ratio=0.2):
    val_size = int(len(dataset) * val_ratio)
    train_size = len(dataset) - val_size
    return random_split(dataset, [train_size, val_size])


# 테스트 함수
def test_model(model, test_loader, device, load_path):
    model.load_state_dict(torch.load(load_path))
    model.to(device)
    model.eval()

    predictions, true_labels = [], []
    with torch.no_grad():
        for batch_data, batch_labels in tqdm(test_loader, desc="Testing"):
            batch_data, batch_labels = batch_data.to(device), batch_labels.to(device)
            outputs = model(batch_data).squeeze()
            predictions.extend(outputs.cpu().tolist())
            true_labels.extend(batch_labels.cpu().tolist())

    return predictions, true_labels


# 그래프 그리기 함수
def plot_predictions(predictions, true_labels):
    plt.figure(figsize=(8, 8))
    plt.scatter(true_labels, predictions, alpha=0.6, edgecolor="k")
    plt.plot(
        [min(true_labels), max(true_labels)],
        [min(true_labels), max(true_labels)],
        'r--', lw=2
    )
    plt.title("Predictions vs True Labels")
    plt.xlabel("True Labels")
    plt.ylabel("Predictions")
    plt.grid(True)
    plt.show()


# Main 실행
def main():
    # 데이터 경로 설정
    data_dir = "grouped_datasets"
    save_path = "model_weights.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    RECIPE_ID = {...}  # 생략
    EQP_ID_MODULE_NAME = {...}  # 생략

    recipe_mapping = map_to_numeric(RECIPE_ID)
    eqp_mapping = map_to_numeric(EQP_ID_MODULE_NAME)

    for i in os.listdir(data_dir):
        csv_file = f"{data_dir}/{i}"
        df = pd.read_csv(csv_file).dropna()
        df = df.sort_values("HST_REG_DTTM")

        if "RECIPE_ID" in df.columns:
            df["RECIPE_ID"] = df["RECIPE_ID"].map(recipe_mapping)
        if "EQP_ID_MODULE_NAME" in df.columns:
            df["EQP_ID_MODULE_NAME"] = df["EQP_ID_MODULE_NAME"].map(eqp_mapping)

        dataset = CustomDataset(df)
        train_dataset, val_dataset = train_val_split(dataset, val_ratio=0.2)
        train_loader = DataLoader(train_dataset, batch_size=512, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=512, shuffle=False)

        # 모델 및 옵티마이저 설정
        model = FullMultiLevelTransformer(input_dim=33, d_model=64, nhead=4, num_layers=6, dim_feedforward=128)
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

        # 테스트
        test_loader = DataLoader(val_dataset, batch_size=512, shuffle=False)
        predictions, true_labels = test_model(model, test_loader, device, save_path)

        # 그래프 출력
        plot_predictions(predictions, true_labels)
        print("Test completed. Predictions and labels collected.")


if __name__ == "__main__":
    main()