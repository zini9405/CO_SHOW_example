import matplotlib.pyplot as plt

def plot_predictions(predictions, true_labels):
    """
    예측값과 실제값을 비교하는 산점도 생성
    """
    # 모든 데이터를 torch.Tensor로 변환
    predictions = torch.cat([torch.tensor(p).unsqueeze(0) for p in predictions]).detach().cpu()
    print(predictions*100000)
    true_labels = torch.cat([torch.tensor(t).unsqueeze(0) for t in true_labels]).detach().cpu()
    print(true_labels)

    # 산점도 생성
    plt.figure(figsize=(8, 8))
    plt.scatter(true_labels, predictions, alpha=0.6, edgecolor="k")
    plt.plot(
        [true_labels.min().item(), true_labels.max().item()],
        [true_labels.min().item(), true_labels.max().item()],
        'r--', lw=2
    )  # y=x 선
    plt.title("Predictions vs True Labels")
    plt.xlabel("True Labels")
    plt.ylabel("Predictions")
    plt.grid(True)
    plt.show()


# def plot_predictions(predictions, true_labels):
#     """
#     정답값(x축)과 예측값(y축)을 비교하는 산점도 생성
#     """

#     predictions = torch.cat([torch.tensor(p).unsqueeze(0) for p in predictions]).detach().cpu()
#     true_labels = torch.cat([torch.tensor(t).unsqueeze(0) for t in true_labels]).detach().cpu()
#     plt.figure(figsize=(8, 8))
    
#     # 산점도 생성
#     plt.scatter(
#         true_labels,
#         predictions,
#         alpha=0.6,
#         edgecolor="k",
#         label="Predictions vs True Labels",
#         color="blue"
#     )
    
#     # y=x 선 추가 (이상적인 경우)
#     plt.plot(
#         [min(true_labels), max(true_labels)],
#         [min(true_labels), max(true_labels)],
#         'r--',
#         lw=2,
#         label="Ideal Line (y=x)"
#     )
    
#     # 그래프 설정
#     plt.title("Predictions vs True Labels")
#     plt.xlabel("True Labels")
#     plt.ylabel("Predictions")
#     plt.legend(loc="upper left")
#     plt.grid(True)
#     plt.show()

# 4. Masked MSE Loss
def mse_loss(output, target):
    return torch.mean((output - target) ** 2)

criterion=mse_loss

def test_model(model, test_loader, device, load_path):
    model.load_state_dict(torch.load(load_path))
    model.to(device)
    model.eval()
    test_loss = 0.0
    test_accuracy = 0.0
    predictions = []
    true_labels = []
    with torch.no_grad():
        for batch_data, batch_labels in tqdm(test_loader, desc="Testing"):
            batch_data = batch_data.to(device)
            batch_labels = batch_labels.to(device)
            outputs = model(batch_data).squeeze()
            loss = criterion(outputs.squeeze(), batch_labels)
            test_loss += loss.item()

            accuracy = calculate_accuracy(outputs.squeeze(), batch_labels)
            test_accuracy += accuracy
            predictions.extend(outputs)
            true_labels.extend(batch_labels)
    avg_test_loss = test_loss / len(test_loader)
    avg_test_accuracy = test_accuracy / len(test_loader)
    
    print(f"test Loss: {avg_test_loss:.4f}, test Accuracy: {avg_test_accuracy:.4f}")

    return predictions, true_labels



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
    """
    예측값과 정답값을 비교하는 산점도 생성
    """
    plt.figure(figsize=(8, 8))
    
    # 정답값 (True Labels)
    plt.scatter(
        range(len(true_labels[:200])),
        true_labels[:200],
        alpha=0.6,
        edgecolor="blue",
        label="True Labels",
        color="blue"
    )
    
    # 예측값 (Predictions)
    plt.scatter(
        range(len(predictions[:200])),
        predictions[:200],
        alpha=0.6,
        edgecolor="red",
        label="Predictions",
        color="red"
    )
    
    # 그래프 설정
    plt.title("Predictions vs True Labels")
    plt.xlabel("Sample Index")
    plt.ylabel("Values")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()


# Main 실행
def main():
    # 데이터 경로 설정
    data_dir = "grouped_datasets"
    save_path = "model_weights.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    RECIPE_ID = {'CAN3_01_CA', 'CAN3_01_CB', 'CIS_CA', 'CIS_CB', 'CIS_P+_CA', 'CIS_P+_CB', 'CIS_P+_CXT5_CB', 'CIS_P+_GLX5_CA', 'CIS_P+_GLX5_CB', 'CIS_P+_HUA4_CA', 'CIS_P+_HUA4_CB', 'CIS_P+_ICR5_CB', 'CIS_P+_ONS6_CA', 'CIS_P+_ONS6_CB', 'CIS_P+_PSM4_CA', 'CIS_P+_SKH6_CA', 'CIS_P+_SKH6_CB', 'CIS_P+_SKH9_CA',
    'CIS_P+_SKH9_CB', 'CIS_P+_SMI4_CA', 'CIS_P+_UMC4_CA', 'CIS_P+_UMC4_CB', 'CIS_P_SKH6_CA', 'CIS_P_SKH6_CB', 'GF_01_CA', 'GF_01_CB', 'GF_02_CA', 'GF_02_CB', 'GF_03_CA', 'GF_03_CB', 'HUALI_01_CA', 'HUALI_01_CB',
    'INTEL10_CA', 'INTEL10_CB', 'INTEL14_CB', 'INTEL2_CA', 'INTEL2_CB', 'INTEL7_CA', 'INTEL7_CB', 'L2_CB', 'LOG_TSM1_CA', 'LOG_TSM1_CB', 'LOG_TSM3_CA', 'LOG_TSM3_CB', 'MIC_01_CA', 'MIC_01_CB', 'MXIC_01_CA', 'MXIC_01_CB', 'PSMC_02_CA', 'PSMC_02_CB', 'PSMC_FSI_CA', 'S14_CA', 'S14_CB', 'SEC_L58_CA', 'SEC_L58_CB',
    'SKH_CIS_CA', 'SKH_CIS_P+_CA', 'SKH_CIS_P+_CB', 'SL_CA', 'SL_CB', 'SMIC2_R0_CA', 'SMIC2_R0_CB', 'SMIC4_R0_CA', 'SMIC_L7_CB', 'STM_01_CA', 'STM_01_CB', 'STM_P+_CA', 'STM_P+_CB', 'TIX_R0_CA', 'TIX_R0_CB', 'TIX_R1_CA', 'TIX_R1_CB', 'TSMC2_CA', 'TSMC2_CB', 'TSMC_CA', 'TSMC_CB', 'UMC_R0_CA', 'UMC_R0_CB'}

    EQP_ID_MODULE_NAME = {'CENC10A', 'CENC10B', 'CENC11A', 'CENC11B', 'CENC12A', 'CENC12B', 'CENC13A', 'CENC13B', 'CENC14A', 'CENC14B', 'CENC15A', 'CENC15B', 'CENC16A', 'CENC16B', 'CENC17A', 'CENC17B', 'CENC31A', 'CENC31B', 'CENC32A',
    'CENC32B', 'CENC33A', 'CENC33B', 'CENC34A', 'CENC34B', 'CENC35A', 'CENC35B', 'CENC36A', 'CENC36B', 'CENC41A', 'CENC41B', 'CENC42A', 'CENC42B', 'CENC43A', 'CENC43B', 'CENC44A', 'CENC44B', 'CENC45A', 'CENC45B',
    'CENC46A', 'CENC46B', 'CENC47A', 'CENC47B', 'CENC48A', 'CENC48B', 'CENC5A', 'CENC5B', 'CENC6A', 'CENC6B', 'CENC7A', 'CENC7B', 'CENC8A', 'CENC8B', 'CENC9A', 'CENC9B', 'ZCENC01A', 'ZCENC01B', 'ZCENC02A', 'ZCENC02B',
    'ZCENC03A', 'ZCENC03B', 'ZCENC04A', 'ZCENC04B'}

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
