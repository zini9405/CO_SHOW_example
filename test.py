import os
import pandas as pd
import numpy as np
import torch
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.preprocessing import QuantileTransformer
from torch.utils.data import Dataset, DataLoader, random_split
from sklearn.metrics import r2_score
import shap


# 데이터 매핑 함수
def map_to_numeric(values):
    return {val: idx for idx, val in enumerate(sorted(values))}


# 데이터 필터링 함수
def filter_data(df, recipe_filter=None, eqp_filter=None):
    """
    특정 Recipe와 Equipment로 데이터 필터링
    Args:
        df: 원본 데이터프레임
        recipe_filter: 필터링할 RECIPE_ID 값 (set 형식)
        eqp_filter: 필터링할 EQP_ID_MODULE_NAME 값 (set 형식)
    Returns:
        필터링된 데이터프레임
    """
    if recipe_filter:
        df = df[df["RECIPE_ID"].isin(recipe_filter)]
    if eqp_filter:
        df = df[df["EQP_ID_MODULE_NAME"].isin(eqp_filter)]
    return df


# Custom Dataset 정의
class CustomDataset(Dataset):
    def __init__(self, df):
        self.data = df
        self.filtered_data = self.data[self.data['STEP_NAME'] == 'DEPO']
        self.labels = self.filtered_data['SFQR_AFS2'].values
        self.quantile_transformer = QuantileTransformer(output_distribution='normal', random_state=42)
        self.labels = self.quantile_transformer.fit_transform(self.labels.reshape(-1, 1)).flatten()
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


# Train/Validation Split
def train_val_split(dataset, val_ratio=0.2):
    val_size = int(len(dataset) * val_ratio)
    train_size = len(dataset) - val_size

    generator = torch.Generator()
    generator.manual_seed(42)  # 시드 고정으로 순서 재현 가능
    return random_split(dataset, [train_size, val_size], generator=generator)


# 테스트 함수
def test_model(model, test_loader, device, load_path, quantile_transformer):
    model.load_state_dict(torch.load(load_path))
    model.to(device)
    model.eval()
    predictions = []
    true_labels = []
    with torch.no_grad():
        for batch_data, batch_labels in tqdm(test_loader, desc="Testing"):
            batch_data = batch_data.to(device)
            batch_labels = batch_labels.to(device)
            outputs = model(batch_data).squeeze()
            predictions.extend(outputs.cpu().numpy())
            true_labels.extend(batch_labels.cpu().numpy())
    return predictions, true_labels


# SHAP 분석 함수
def shap_analysis(model, dataset, device):
    """
    SHAP 분석 및 시각화
    Args:
        model: 학습된 Transformer 모델
        dataset: CustomDataset 객체
        device: 실행할 디바이스 (CPU/GPU)
    """
    print("Starting SHAP analysis...")

    # 모델 평가 모드
    model.eval()
    
    # 데이터 샘플 추출 (SHAP 계산 속도를 위해 일부 데이터 사용)
    num_samples = min(len(dataset), 500)  # 최대 500개 샘플 사용
    sampled_features = dataset.features[:num_samples]
    sampled_labels = dataset.labels[:num_samples]

    # 모델 예측 함수 정의
    def model_predict(x):
        x_tensor = torch.tensor(x, dtype=torch.float32).to(device)
        with torch.no_grad():
            return model(x_tensor).cpu().numpy()

    # SHAP Explainer 초기화
    explainer = shap.Explainer(model_predict, sampled_features)
    
    # SHAP 값 계산
    shap_values = explainer(sampled_features)
    
    # SHAP 요약 시각화
    shap.summary_plot(
        shap_values,
        sampled_features,
        feature_names=[f"Feature_{i}" for i in range(sampled_features.shape[1])]
    )

    # 특정 샘플 SHAP Force Plot
    sample_index = 0  # 첫 번째 샘플
    shap.force_plot(
        explainer.expected_value[0],
        shap_values[sample_index],
        sampled_features[sample_index],
        feature_names=[f"Feature_{i}" for i in range(sampled_features.shape[1])]
    )


# 예측 및 실제 값 비교 시각화
def visualize_predictions(predictions, true_labels):
    """
    모델 예측값과 실제값의 비교 시각화
    Args:
        predictions: 모델 예측값 리스트
        true_labels: 실제값 리스트
    """
    plt.figure(figsize=(10, 6))
    plt.plot(predictions, label="Predictions", color="blue")
    plt.plot(true_labels, label="True Labels", color="orange")
    plt.title("Model Predictions vs True Labels")
    plt.xlabel("Sample Index")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.show()


# Main 실행
def main():
    # 데이터 경로 설정
    csv_file = 'all.csv'
    save_path = "model_weights_multi_all.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    RECIPE_ID = {...}  # 생략 (기존 코드와 동일)
    EQP_ID_MODULE_NAME = {...}  # 생략 (기존 코드와 동일)

    recipe_mapping = map_to_numeric(RECIPE_ID)
    eqp_mapping = map_to_numeric(EQP_ID_MODULE_NAME)

    # 데이터셋 로드 및 전처리
    df = pd.read_csv(csv_file).dropna()
    df = df.sort_values("HST_REG_DTTM")

    if "RECIPE_ID" in df.columns:
        df["RECIPE_ID"] = df["RECIPE_ID"].map(recipe_mapping)
    if "EQP_ID_MODULE_NAME" in df.columns:
        df["EQP_ID_MODULE_NAME"] = df["EQP_ID_MODULE_NAME"].map(eqp_mapping)

    # 데이터 필터링 (선택적으로 필터 적용)
    recipe_filter = {'CAN3_01_CA', 'CIS_P+_CA'}  # 원하는 Recipe만 사용
    eqp_filter = {'CENC10A', 'CENC10B'}  # 원하는 Equipment만 사용
    df = filter_data(df, recipe_filter=recipe_filter, eqp_filter=eqp_filter)

    dataset = CustomDataset(df)

    # Train/Test Split
    train_dataset, val_dataset = train_val_split(dataset, val_ratio=0.2)
    test_loader = DataLoader(val_dataset, batch_size=512, shuffle=False)

    # 모델 초기화
    model = FullMultiLevelTransformer(input_dim=33, d_model=256, nhead=4, num_layers=4, dim_feedforward=512)

    # 테스트 실행
    predictions, true_labels = test_model(model, test_loader, device, save_path, dataset.quantile_transformer)

    # 예측 정확도 확인
    print(f"R2 Score: {r2_score(true_labels, predictions)}")

    # 예측 결과 시각화
    visualize_predictions(predictions, true_labels)

    # SHAP 분석
    shap_analysis(model, dataset, device)


if __name__ == "__main__":
    main()