import os
import pandas as pd
import numpy as np
import torch
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.preprocessing import QuantileTransformer
from torch.utils.data import Dataset, DataLoader, random_split
from sklearn.manifold import TSNE
from sklearn.metrics import r2_score
import torch.nn as nn
from einops import rearrange, reduce

# 데이터 매핑 함수
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
        combined_features = rearrange(combined_features, 'b d -> 1 b d')
        transformed_features = self.feature_transformer(combined_features)
        output = reduce(transformed_features, '1 b d -> b d', 'mean')
        return self.fc(output)

# EQP_ID_MODULE_NAME 임베딩 시각화 함수
def visualize_eqp_embedding(model, eqp_mapping):
    """
    EQP_ID_MODULE_NAME 임베딩 시각화
    """
    # EQP_ID_MODULE_NAME의 임베딩 벡터를 추출
    embedding_weights = model.eqp_embedding.weight.detach().cpu().numpy()

    # t-SNE를 사용하여 2D로 차원 축소
    tsne = TSNE(n_components=2, random_state=42)
    reduced_embeddings = tsne.fit_transform(embedding_weights)

    # EQP_ID_MODULE_NAME 레이블 가져오기
    eqp_labels = list(eqp_mapping.keys())

    # 시각화
    plt.figure(figsize=(12, 8))
    for i, label in enumerate(eqp_labels):
        plt.scatter(reduced_embeddings[i, 0], reduced_embeddings[i, 1], label=label)
        plt.text(reduced_embeddings[i, 0], reduced_embeddings[i, 1], label, fontsize=9)
    
    plt.title("EQP_ID_MODULE_NAME Embedding Visualization")
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

# Train/Validation Split
def train_val_split(dataset, val_ratio=0.2):
    val_size = int(len(dataset) * val_ratio)
    train_size = len(dataset) - val_size
    generator = torch.Generator()
    generator.manual_seed(42)
    return random_split(dataset, [train_size, val_size], generator=generator)

# Main 실행
def main():
    # 데이터 경로 설정
    csv_file = 'all_minmax.csv'  # 실제 CSV 파일 경로로 변경
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 데이터 매핑
    EQP_ID_MODULE_NAME = {'CENC10A', 'CENC10B', 'CENC11A', 'CENC11B', 'CENC12A', 'CENC12B', 'CENC13A', 'CENC13B', 
                          'CENC14A', 'CENC14B', 'CENC15A', 'CENC15B', 'CENC16A', 'CENC16B', 'CENC17A', 'CENC17B'}
    eqp_mapping = map_to_numeric(EQP_ID_MODULE_NAME)

    # 데이터 로드 및 전처리
    df = pd.read_csv(csv_file)
    df = df.dropna(subset=['ZDDFRONTMEAN_01_AFS2', 'ZDDFRONTMEAN_01_AFS2_SUB'])
    df.fillna(0, inplace=True)
    df = df.sort_values("HST_REG_DTTM")
    if "EQP_ID_MODULE_NAME" in df.columns:
        df["EQP_ID_MODULE_NAME"] = df["EQP_ID_MODULE_NAME"].map(eqp_mapping)

    dataset = CustomDataset(df, eqp_mapping)
    train_dataset, val_dataset = train_val_split(dataset, val_ratio=0.2)
    train_loader = DataLoader(train_dataset, batch_size=512, shuffle=True)

    # 모델 초기화
    model = FullMultiLevelTransformer(input_dim=32, eqp_vocab_size=len(eqp_mapping), d_model=256, nhead=4, num_layers=4, dim_feedforward=512)
    model.to(device)

    # EQP_ID_MODULE_NAME 임베딩 시각화
    visualize_eqp_embedding(model, eqp_mapping)

if __name__ == "__main__":
    main()