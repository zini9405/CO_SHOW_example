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
        self.feature_names = self.data.drop(columns=[
            'WAF_ID', 'HST_REG_DTTM', 'SFQR_AFS2', 'ESFQR2_MAX_AFS2', 'ZDDFRONTMEAN_01_AFS2',
            'ESFQD_ZONE1MEAN_AFS2', 'ESFQD_ZONE1MAX_AFS2', 'ESFQD2_ZONE1MEAN_AFS2', 'ESFQD2_ZONE1MAX_AFS2',
            'SFQR_AFS2_SUB', 'ESFQR2_MAX_AFS2_SUB', 'ESFQD_ZONE1MEAN_AFS2_SUB', 'ESFQD_ZONE1MAX_AFS2_SUB',
            'ESFQD2_ZONE1MEAN_AFS2_SUB', 'ESFQD2_ZONE1MAX_AFS2_SUB', 'EQP_ID_MODULE_NAME'
        ]).columns

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
        self.transformer_layers = nn.ModuleList([
            nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout)
            for _ in range(num_layers)
        ])
        self.fc = nn.Linear(d_model, 1)
        self.attention_weights = []  # Attention Weights 저장

    def forward(self, features, eqp_ids):
        feature_embed = self.feature_embedding(features)
        eqp_embed = self.eqp_embedding(eqp_ids)
        combined_features = feature_embed + eqp_embed

        combined_features = rearrange(combined_features, 'b d -> 1 b d')

        self.attention_weights = []
        for layer in self.transformer_layers:
            attn_output, attn_weights = layer.self_attn(
                combined_features, combined_features, combined_features, need_weights=True, attn_mask=None
            )
            combined_features = layer.norm1(combined_features + attn_output)
            combined_features = layer.norm2(combined_features + layer.linear2(nn.functional.relu(layer.linear1(combined_features))))
            self.attention_weights.append(attn_weights)

        combined_features = reduce(combined_features, '1 b d -> b d', 'mean')
        return self.fc(combined_features)

    def get_attention_maps(self):
        return self.attention_weights

# Attention Score 시각화 함수
def visualize_attention_scores(model, feature_names):
    """
    Attention Weights를 시각화하여 변수별 중요도 출력
    """
    attention_maps = model.get_attention_maps()
    avg_attention = torch.mean(attention_maps[-1], dim=1).squeeze().detach().cpu().numpy()  # 마지막 레이어 사용
    sorted_indices = np.argsort(-avg_attention)  # 중요도 순서대로 정렬

    print("\nFeature Importance:")
    for idx in sorted_indices:
        print(f"{feature_names[idx]}: {avg_attention[idx]:.4f}")

    # 시각화
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(feature_names)), avg_attention[sorted_indices], tick_label=[feature_names[i] for i in sorted_indices])
    plt.xticks(rotation=45, ha='right')
    plt.title("Feature Importance (Attention Scores)")
    plt.ylabel("Attention Score")
    plt.tight_layout()
    plt.show()

# Main 실행
def main():
    csv_file = 'all_minmax.csv'  # 실제 CSV 파일 경로로 변경
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    EQP_ID_MODULE_NAME = {'CENC10A', 'CENC10B', 'CENC11A', 'CENC11B', 'CENC12A', 'CENC12B', 'CENC13A', 'CENC13B',
                          'CENC14A', 'CENC14B', 'CENC15A', 'CENC15B', 'CENC16A', 'CENC16B', 'CENC17A', 'CENC17B'}
    eqp_mapping = map_to_numeric(EQP_ID_MODULE_NAME)

    df = pd.read_csv(csv_file)
    df = df.dropna(subset=['ZDDFRONTMEAN_01_AFS2', 'ZDDFRONTMEAN_01_AFS2_SUB'])
    df.fillna(0, inplace=True)
    df = df.sort_values("HST_REG_DTTM")
    df["EQP_ID_MODULE_NAME"] = df["EQP_ID_MODULE_NAME"].map(eqp_mapping)

    dataset = CustomDataset(df, eqp_mapping)
    train_dataset, val_dataset = train_val_split(dataset, val_ratio=0.2)
    train_loader = DataLoader(train_dataset, batch_size=512, shuffle=True)

    model = FullMultiLevelTransformer(input_dim=32, eqp_vocab_size=len(eqp_mapping), d_model=256, nhead=4, num_layers=4, dim_feedforward=512)
    model.to(device)

    # Attention Scores 시각화
    visualize_attention_scores(model, dataset.feature_names)

if __name__ == "__main__":
    main()