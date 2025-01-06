import os
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter
from einops import rearrange, reduce
from sklearn.preprocessing import QuantileTransformer


import torch
import numpy as np
import random
import pickle

def set_seed(seed: int):
    """
    학습의 재현 가능성을 위해 시드를 고정합니다.
    Args:
        seed (int): 고정할 시드 값
    """
    random.seed(seed)                      # Python의 random 모듈 시드 고정
    np.random.seed(seed)                   # NumPy 시드 고정
    torch.manual_seed(seed)                # PyTorch CPU 시드 고정
    torch.cuda.manual_seed(seed)           # PyTorch CUDA 시드 고정
    torch.cuda.manual_seed_all(seed)       # 모든 GPU의 CUDA 시드 고정 (멀티 GPU 사용 시)
    torch.backends.cudnn.deterministic = True  # CuDNN을 deterministic 모드로 설정
    torch.backends.cudnn.benchmark = False     # CuDNN의 최적화 비활성화 (속도는 느릴 수 있음)


# 1. 데이터 매핑 함수
def map_to_numeric(values):
    mapping = {val: idx for idx, val in enumerate(sorted(values))}
    return mapping

# 2. Custom Dataset 정의
class CustomDataset(Dataset):
    def __init__(self, df):
        self.data = df
        self.labels = self.data['ZDDFRONTMEAN_01_AFS2'].values
        self.quantile_transformer = QuantileTransformer(output_distribution='normal', random_state=42)
        self.labels = self.quantile_transformer.fit_transform(self.labels.reshape(-1, 1)).flatten()
        self.features = self.data.drop(columns=['WAF_ID', 'HST_REG_DTTM', 'SFQR_AFS2', 'ESFQR2_MAX_AFS2', 'ZDDFRONTMEAN_01_AFS2', 'ESFQD_ZONE1MEAN_AFS2', 'ESFQD_ZONE1MAX_AFS2', 'ESFQD2_ZONE1MEAN_AFS2', 'ESFQD2_ZONE1MAX_AFS2',
                     'SFQR_AFS2_SUB', 'ESFQR2_MAX_AFS2_SUB', 'ESFQD_ZONE1MEAN_AFS2_SUB', 'ESFQD_ZONE1MAX_AFS2_SUB', 'ESFQD2_ZONE1MEAN_AFS2_SUB', 'ESFQD2_ZONE1MAX_AFS2_SUB']).values

# exclude_columns = ['SFQR_AFS2', 'ESFQR2_MAX_AFS2', 'ZDDFRONTMEAN_01_AFS2', 'ESFQD_ZONE1MEAN_AFS2', 'ESFQD_ZONE1MAX_AFS2', 'ESFQD2_ZONE1MEAN_AFS2', 'ESFQD2_ZONE1MAX_AFS2',
#                      'SFQR_AFS2_SUB', 'ESFQR2_MAX_AFS2_SUB', 'ZDDFRONTMEAN_01_AFS2_SUB', 'ESFQD_ZONE1MEAN_AFS2_SUB', 'ESFQD_ZONE1MAX_AFS2_SUB', 'ESFQD2_ZONE1MEAN_AFS2_SUB', 'ESFQD2_ZONE1MAX_AFS2_SUB']

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return torch.tensor(self.features[idx], dtype=torch.float32), torch.tensor(self.labels[idx], dtype=torch.float32)

# 3. Transformer 모델 정의
class FullMultiLevelTransformer(nn.Module):
    def __init__(self, input_dim, d_model=64, nhead=4, num_layers=2, dim_feedforward=128, dropout=0.1):
        super(FullMultiLevelTransformer, self).__init__()
        self.d_model = d_model

        self.feature_embedding = nn.Linear(input_dim, d_model)
        self.feature_transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout),
            num_layers=num_layers
        )
        self.fc = nn.Linear(d_model, 1)

    def forward(self, x):
        x = self.feature_embedding(x)
        x = rearrange(x, 'b d -> b 1 d')
        x = self.feature_transformer(x)
        x = reduce(x, 'b 1 d -> b d', 'mean')
        return self.fc(x)

# 5. Accuracy 계산
def calculate_accuracy(output, target, threshold=0.0001):
    correct = torch.abs(output - target) <= threshold
    return correct.sum().item() / len(target)

# 6. Train/Val Split
def train_val_split(dataset, val_ratio=0.2):
    val_size = int(len(dataset) * val_ratio)
    print(val_size)
    train_size = len(dataset) - val_size
    return random_split(dataset, [train_size, val_size])


# 7. 모델 훈련 루프
def train_model_inputs(model, train_loader, val_loader, criterion, optimizer, num_epochs, device, log_dir, save_path):
    writer = SummaryWriter(log_dir)
    model.to(device)

    best_val_loss = float('inf')  # Initialize best validation loss

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        total_accuracy = 0.0

        train_pbar = tqdm(train_loader, desc=f"Training Epoch {epoch + 1}/{num_epochs}")
        for batch_data, batch_labels in train_pbar:
            batch_data, batch_labels = batch_data.to(device), batch_labels.to(device)

            outputs = model(batch_data)

            loss = criterion(outputs.squeeze(), batch_labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            accuracy = calculate_accuracy(outputs.squeeze(), batch_labels)
            total_accuracy += accuracy

            # Update progress bar
            train_pbar.set_postfix(loss=loss.item(), accuracy=accuracy)

        avg_train_loss = running_loss / len(train_loader)
        avg_train_accuracy = total_accuracy / len(train_loader)
        writer.add_scalar("Loss/Train", avg_train_loss, epoch)
        writer.add_scalar("Accuracy/Train", avg_train_accuracy, epoch)
        print(f"Epoch [{epoch + 1}/{num_epochs}], Train Loss: {avg_train_loss:.4f}, Train Accuracy: {avg_train_accuracy:.4f}")

        # Validation Step
        model.eval()
        val_loss = 0.0
        val_accuracy = 0.0
        val_pbar = tqdm(val_loader, desc=f"Validation Epoch {epoch + 1}/{num_epochs}")
        with torch.no_grad():
            for batch_data, batch_labels in val_pbar:
                batch_data, batch_labels = batch_data.to(device), batch_labels.to(device)
                outputs = model(batch_data)
                loss = criterion(outputs.squeeze(), batch_labels)
                val_loss += loss.item()

                accuracy = calculate_accuracy(outputs.squeeze(), batch_labels)
                val_accuracy += accuracy

                # Update progress bar
                val_pbar.set_postfix(loss=loss.item(), accuracy=accuracy)

        avg_val_loss = val_loss / len(val_loader)
        avg_val_accuracy = val_accuracy / len(val_loader)
        writer.add_scalar("Loss/Validation", avg_val_loss, epoch)
        writer.add_scalar("Accuracy/Validation", avg_val_accuracy, epoch)
        print(f"Epoch [{epoch + 1}/{num_epochs}], Validation Loss: {avg_val_loss:.4f}, Validation Accuracy: {avg_val_accuracy:.4f}")

        # Save model weights if validation loss improves
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), save_path)
            print(f"Best model saved with validation loss: {best_val_loss:.4f}")

    writer.close()
    # 모델 가중치 저장
    torch.save(model.state_dict(), save_path)
    print(f"Model weights saved to {save_path}")

# 9. Main 실행
def main():
    RECIPE_ID = {'CAN3_01_CA', 'CAN3_01_CB', 'CIS_CA', 'CIS_CB', 'CIS_P+_CA', 'CIS_P+_CB', 'CIS_P+_CXT5_CB', 'CIS_P+_GLX5_CA', 'CIS_P+_GLX5_CB', 'CIS_P+_HUA4_CA', 'CIS_P+_HUA4_CB',
    'CIS_P+_ICR5_CB', 'CIS_P+_ONS6_CA', 'CIS_P+_ONS6_CB', 'CIS_P+_PSM4_CA', 'CIS_P+_SKH6_CA', 'CIS_P+_SKH6_CB', 'CIS_P+_SKH9_CA', 'CIS_P+_SKH9_CB', 'CIS_P+_SMI4_CA', 'CIS_P+_UMC4_CA',
    'CIS_P+_UMC4_CB', 'CIS_P_SKH6_CA', 'CIS_P_SKH6_CB', 'GF_01_CA', 'GF_01_CB', 'GF_02_CA', 'GF_02_CB', 'GF_03_CA', 'GF_03_CB', 'HUALI_01_CA', 'HUALI_01_CB', 'INTEL10_CA', 'INTEL10_CB',
    'INTEL14_CA', 'INTEL14_CB', 'INTEL2_CA', 'INTEL2_CB', 'INTEL7_CA', 'INTEL7_CB', 'L2_CB', 'LOG_TSM1_CA', 'LOG_TSM1_CB', 'LOG_TSM3_CA', 'LOG_TSM3_CB', 'MIC_01_CA', 'MIC_01_CB', 'MXIC_01_CA',
    'MXIC_01_CB', 'PSMC_02_CA', 'PSMC_02_CB', 'PSMC_FSI_CA', 'S14_CA', 'S14_CB', 'SEC_L58_CA', 'SEC_L58_CB', 'SKH_CIS_CA', 'SKH_CIS_P+_CA', 'SKH_CIS_P+_CB', 'SL_CA', 'SL_CB', 'SMIC2_R0_CA',
    'SMIC2_R0_CB', 'SMIC4_R0_CA', 'SMIC_L7_CA', 'SMIC_L7_CB', 'STM_01_CA', 'STM_01_CB', 'STM_P+_CA', 'STM_P+_CB', 'TIX_R0_CA', 'TIX_R0_CB', 'TIX_R1_CA', 'TIX_R1_CB', 'TSMC2_CA', 'TSMC2_CB',
    'TSMC_CA', 'TSMC_CB', 'UMC_R0_CA', 'UMC_R0_CB'}

    EQP_ID_MODULE_NAME = {'CENC10A', 'CENC10B', 'CENC11A', 'CENC11B', 'CENC12A', 'CENC12B', 'CENC13A', 'CENC13B', 'CENC14A', 'CENC14B', 'CENC15A', 'CENC15B', 'CENC16A', 'CENC16B', 'CENC17A', 'CENC17B', 'CENC31A', 'CENC31B', 'CENC32A',
    'CENC32B', 'CENC33A', 'CENC33B', 'CENC34A', 'CENC34B', 'CENC35A', 'CENC35B', 'CENC36A', 'CENC36B', 'CENC41A', 'CENC41B', 'CENC42A', 'CENC42B', 'CENC43A', 'CENC43B', 'CENC44A', 'CENC44B', 'CENC45A', 'CENC45B',
    'CENC46A', 'CENC46B', 'CENC47A', 'CENC47B', 'CENC48A', 'CENC48B', 'CENC5A', 'CENC5B', 'CENC6A', 'CENC6B', 'CENC7A', 'CENC7B', 'CENC8A', 'CENC8B', 'CENC9A', 'CENC9B', 'ZCENC01A', 'ZCENC01B', 'ZCENC02A', 'ZCENC02B',
    'ZCENC03A', 'ZCENC03B', 'ZCENC04A', 'ZCENC04B'}

    recipe_mapping = map_to_numeric(RECIPE_ID)
    eqp_mapping = map_to_numeric(EQP_ID_MODULE_NAME)

    # 6. Quantile Transformation

    # Load CSV
    csv_file = 'all_minmax.csv'
    df = pd.read_csv(csv_file)

    df = df.dropna(subset=['ZDDFRONTMEAN_01_AFS2', 'ZDDFRONTMEAN_01_AFS2_SUB'])

    df.fillna(0, inplace=True)

    # Ensure HST_REG_DTTM is sorted
    df = df.sort_values("HST_REG_DTTM")

    # Replace RECIPE_ID and EQP_ID_MODULE_NAME with numeric values
    if "RECIPE_ID" in df.columns:
        df["RECIPE_ID"] = df["RECIPE_ID"].map(recipe_mapping)
    if "EQP_ID_MODULE_NAME" in df.columns:
        df["EQP_ID_MODULE_NAME"] = df["EQP_ID_MODULE_NAME"].map(eqp_mapping)

    dataset = CustomDataset(df)

    train_dataset, val_dataset = train_val_split(dataset, val_ratio=0.2)

    train_loader = DataLoader(train_dataset, batch_size=512, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=512, shuffle=False)

    # 모델 및 학습 설정
    # load_path = "model_weights_z.pth"
    model = FullMultiLevelTransformer(input_dim=33, d_model=256, nhead=4, num_layers=4, dim_feedforward=512)
    # model.load_state_dict(torch.load(load_path))
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    save_path = "model_weights_ZDD.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_model_inputs(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        criterion=nn.HuberLoss(delta=1.0),
        optimizer=optimizer,
        num_epochs=20000,
        device=device,
        log_dir="logs",
        save_path=save_path
    )

if __name__ == "__main__":
    set_seed(42)
    main()


이 코드는 EQP_ID_MODULE_NAME를 따로 embedding하지 않고 학습하는 코드인데, 따로 임베딩하는 코드 추가해줘. 왜냐하면 난중에 umap or t-SNE로 EQP_ID_MODULE_NAME을 시각화하고 싶어. 그리고 attention map을 통해 어떤 변수가 중요한지 알고 싶어. 추후에 변수명: 중요도 이런식으로 만들거야. 이 조건에 맞게 코드 다 수정해줘.
