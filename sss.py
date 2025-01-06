import os
import pandas as pd
import numpy as np
import torch
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.preprocessing import QuantileTransformer
from torch.utils.data import Dataset, DataLoader, random_split
from torch.utils.data import Subset
from sklearn.metrics import r2_score


# 1. 데이터 매핑 함수
def map_to_numeric(values):
    mapping = {val: idx for idx, val in enumerate(sorted(values))}
    return mapping

# Custom Dataset 정의
class CustomDataset(Dataset):
    def __init__(self, df, eqp_mapping):
        self.data = df
        self.labels = self.data['ZDDFRONTMEAN_01_AFS2'].values
        self.eqp_mapping = eqp_mapping
        self.quantile_transformer = QuantileTransformer(output_distribution='normal', random_state=42)
        self.labels = self.quantile_transformer.fit_transform(self.labels.reshape(-1, 1)).flatten()
        self.features = self.data.drop(columns=[
            'WAF_ID', 'HST_REG_DTTM', 'SFQR_AFS2', 'ESFQR2_MAX_AFS2', 'ZDDFRONTMEAN_01_AFS2',
            'ESFQD_ZONE1MEAN_AFS2', 'ESFQD_ZONE1MAX_AFS2', 'ESFQD2_ZONE1MEAN_AFS2', 'ESFQD2_ZONE1MAX_AFS2',
            'SFQR_AFS2_SUB', 'ESFQR2_MAX_AFS2_SUB', 'ESFQD_ZONE1MEAN_AFS2_SUB', 'ESFQD_ZONE1MAX_AFS2_SUB',
            'ESFQD2_ZONE1MEAN_AFS2_SUB', 'ESFQD2_ZONE1MAX_AFS2_SUB', 'EQP_ID_MODULE_NAME'
        ]).values
        self.eqp_ids = self.data['EQP_ID_MODULE_NAME'].map(self.eqp_mapping).values

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        features = torch.tensor(self.features[idx], dtype=torch.float32)
        label = torch.tensor(self.labels[idx], dtype=torch.float32)
        eqp_id = torch.tensor(self.eqp_ids[idx], dtype=torch.long)
        return features, eqp_id, label

# Transformer 모델 정의
class FullMultiLevelTransformer(nn.Module):
    def __init__(self, input_dim, eqp_vocab_size, d_model=64, nhead=4, num_layers=2, dim_feedforward=128, dropout=0.1):
        super(FullMultiLevelTransformer, self).__init__()
        self.d_model = d_model

        self.eqp_embedding = nn.Embedding(eqp_vocab_size, d_model)
        self.feature_embedding = nn.Linear(input_dim, d_model)
        self.feature_transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout),
            num_layers=num_layers
        )
        self.fc = nn.Linear(d_model, 1)

    def forward(self, features, eqp_ids):
        feature_embed = self.feature_embedding(features)
        eqp_embed = self.eqp_embedding(eqp_ids)

        combined_features = feature_embed + eqp_embed

        # print(feature_embed.shape, eqp_embed.shape, combined_features.shape)

        combined_features = rearrange(combined_features, 'b d -> 1 b d')
        transformed_features = self.feature_transformer(combined_features)
        output = reduce(transformed_features, '1 b d -> b d', 'mean')
        return self.fc(output)

# 정확도 계산 함수
def calculate_accuracy(output, target, threshold=0.001):
    correct = torch.abs(output - target) <= threshold
    return correct.sum().item() / len(target)


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
        for batch_features, batch_eqp_ids, batch_labels in tqdm(test_loader, desc="Testing"):
            batch_features, batch_eqp_ids, batch_labels = (
            batch_features.to(device), batch_eqp_ids.to(device), batch_labels.to(device)
        )
            outputs = model(batch_features, batch_eqp_ids)
            outputs = outputs.squeeze()

            predictions.extend(outputs.cpu().numpy())
            true_labels.extend(batch_labels.cpu().numpy())
    return predictions, true_labels


def calculate_correlation(predictions, true_labels, quantile_transformer):
    """
    정답값과 예측값의 상관관계를 계산
    """
    # 예측값 및 정답값 복원
    predictions = torch.tensor(predictions).detach().cpu().numpy().reshape(-1, 1)
    predictions = quantile_transformer.inverse_transform(predictions).flatten()
    true_labels = torch.tensor(true_labels).detach().cpu().numpy().reshape(-1, 1)
    true_labels = quantile_transformer.inverse_transform(true_labels).flatten()

    # 상관계수 계산
    correlation = np.corrcoef(true_labels, predictions)[0, 1]
    print(f"Correlation Coefficient (True Labels vs Predictions): {correlation:.4f}")
    return correlation, predictions, true_labels


# Main 실행
def main():
    # 데이터 경로 설정
    csv_file = 'all_minmax.csv'  # 실제 CSV 파일 경로로 변경하세요
    save_path = "model_weights_ZDD1111.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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

    df = pd.read_csv(csv_file)

    df = df.dropna(subset=['ZDDFRONTMEAN_01_AFS2', 'ZDDFRONTMEAN_01_AFS2_SUB'])

    df.fillna(0, inplace=True)

    df = df.sort_values("HST_REG_DTTM")

    # # 데이터셋 로드 및 전처리
    # df = pd.read_csv(csv_file).dropna()
    # df = df.sort_values("HST_REG_DTTM")


    if "RECIPE_ID" in df.columns:
        df["RECIPE_ID"] = df["RECIPE_ID"].map(recipe_mapping)
    # if "EQP_ID_MODULE_NAME" in df.columns:
    #     df["EQP_ID_MODULE_NAME"] = df["EQP_ID_MODULE_NAME"].map(eqp_mapping)

    
    dataset = CustomDataset(df, eqp_mapping)

    train_dataset, val_dataset = train_val_split(dataset, val_ratio=1)

    test_loader = DataLoader(val_dataset, batch_size=512, shuffle=False)


    # 모델 및 테스트 실행

    model = FullMultiLevelTransformer(input_dim=32, eqp_vocab_size=len(eqp_mapping), d_model=256, nhead=4, num_layers=4, dim_feedforward=512)
    predictions, true_labels = test_model(model, test_loader, device, save_path, dataset.quantile_transformer)

    # 그래프 출력
    correlation, predictions, true_labels = calculate_correlation(predictions, true_labels, dataset.quantile_transformer)
    print(correlation)
    print(predictions)
    print(true_labels)
    print(r2_score(true_labels, predictions))


if __name__ == "__main__":
    main()

이 코드는 EQP_ID_MODULE_NAME을 따로 임베딩해서 test하는 코드야. self.eqp_embedding = nn.Embedding(eqp_vocab_size, d_model)의 임베딩을 시각화해줘. 표시는 EQP_ID_MODULE_NAME으로 표시해줘.
