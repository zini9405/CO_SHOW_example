import torch
from torch import nn
from torch.utils.data import Dataset
from sklearn.preprocessing import QuantileTransformer
from einops import rearrange, reduce
import pandas as pd


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
        self.attention_layer = nn.MultiheadAttention(embed_dim=d_model, num_heads=nhead, dropout=dropout)

    def forward(self, features, eqp_ids):
        feature_embed = self.feature_embedding(features)
        eqp_embed = self.eqp_embedding(eqp_ids)

        combined_features = feature_embed + eqp_embed
        combined_features = rearrange(combined_features, 'b d -> 1 b d')

        # Attention 처리
        transformed_features, attention_scores = self.attention_layer(
            combined_features, combined_features, combined_features
        )

        # Flatten and reduce dimensions
        output = reduce(transformed_features, '1 b d -> b d', 'mean')
        return self.fc(output), attention_scores

    def get_feature_importance(self, attention_scores):
        # Attention Score 기반 변수 중요도 계산
        attention_mean = attention_scores.mean(dim=1).squeeze(0)  # 평균 계산
        importance = attention_mean / attention_mean.sum()  # 중요도 계산
        return importance


# 모델 초기화
eqp_mapping = map_to_numeric(df['EQP_ID_MODULE_NAME'].unique())
model = FullMultiLevelTransformer(input_dim=32, eqp_vocab_size=len(eqp_mapping), d_model=256, nhead=4, num_layers=4, dim_feedforward=512)

# 데이터 로드
csv_file = 'all_minmax.csv'
df = pd.read_csv(csv_file)

# 데이터셋 정의
dataset = CustomDataset(df, eqp_mapping)

# 예제 데이터 추출
sample_features, sample_eqp_ids, _ = dataset[0]  # 임의 데이터 샘플
sample_features = sample_features.unsqueeze(0)  # Batch Dimension 추가
sample_eqp_ids = sample_eqp_ids.unsqueeze(0)

# 모델 출력 및 Attention Score 추출
model.eval()
with torch.no_grad():
    output, attention_scores = model(sample_features, sample_eqp_ids)

# 변수 중요도 계산
feature_importance = model.get_feature_importance(attention_scores)
feature_names = df.drop(columns=[
    'WAF_ID', 'HST_REG_DTTM', 'SFQR_AFS2', 'ESFQR2_MAX_AFS2', 'ZDDFRONTMEAN_01_AFS2',
    'ESFQD_ZONE1MEAN_AFS2', 'ESFQD_ZONE1MAX_AFS2', 'ESFQD2_ZONE1MEAN_AFS2', 'ESFQD2_ZONE1MAX_AFS2',
    'SFQR_AFS2_SUB', 'ESFQR2_MAX_AFS2_SUB', 'ESFQD_ZONE1MEAN_AFS2_SUB', 'ESFQD_ZONE1MAX_AFS2_SUB',
    'ESFQD2_ZONE1MEAN_AFS2_SUB', 'ESFQD2_ZONE1MAX_AFS2_SUB', 'EQP_ID_MODULE_NAME'
]).columns

# 변수별 중요도 출력
feature_importance_dict = {feature: importance.item() for feature, importance in zip(feature_names, feature_importance)}
print("Feature Importance:", feature_importance_dict)