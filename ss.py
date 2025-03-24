
from torch.utils.data import Dataset
import torch
from sklearn.preprocessing import QuantileTransformer
import numpy as np

class CustomDataset(Dataset):
    def __init__(self, df, eqp_mapping):
        self.data = df
        self.eqp_mapping = eqp_mapping

        # 원래 연속형 라벨
        raw_labels = self.data['6900_GBIR_AFS2'].values

        # 정규 분포로 변환
        self.quantile_transformer = QuantileTransformer(output_distribution='normal', random_state=42)
        transformed_labels = self.quantile_transformer.fit_transform(raw_labels.reshape(-1, 1)).flatten()

        # 0.5 기준으로 이진 분류 라벨 생성
        self.labels = (transformed_labels > 0.5).astype(np.int64)

        # Feature 추출
        self.features = self.data.drop(columns=['BASE_DT', 'EQP_ID', 'WAF_ID', '6900_GBIR_AFS2']).values

        # Equipment ID 인코딩
        self.eqp_ids = self.data['EQP_ID'].map(self.eqp_mapping).values

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        features = torch.tensor(self.features[idx], dtype=torch.float32)
        label = torch.tensor(self.labels[idx], dtype=torch.long)  # CrossEntropyLoss에 맞게 long type
        eqp_id = torch.tensor(self.eqp_ids[idx], dtype=torch.long)
        return features, eqp_id, label
        
        
        
import torch
import torch.nn as nn
import torch.nn.functional as F

# Custom Multihead Self-Attention Layer
class CustomMultiheadAttention(nn.Module):
    def __init__(self, d_model, nhead):
        super(CustomMultiheadAttention, self).__init__()
        self.d_model = d_model
        self.nhead = nhead
        self.head_dim = d_model // nhead
        assert d_model % nhead == 0, "d_model must be divisible by nhead"

        self.query = nn.Linear(d_model, d_model)
        self.key = nn.Linear(d_model, d_model)
        self.value = nn.Linear(d_model, d_model)
        self.out = nn.Linear(d_model, d_model)

    def forward(self, x):
        batch_size, seq_len, d_model = x.size()
        Q = self.query(x)
        K = self.key(x)
        V = self.value(x)

        Q = Q.view(batch_size, seq_len, self.nhead, self.head_dim).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.nhead, self.head_dim).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.nhead, self.head_dim).transpose(1, 2)

        attn_scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.head_dim ** 0.5)
        attn_weights = F.softmax(attn_scores, dim=-1)

        attn_output = torch.matmul(attn_weights, V)
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, seq_len, d_model)
        output = self.out(attn_output)
        return output, attn_weights


# Custom Transformer Encoder Layer
class CustomTransformerEncoderLayer(nn.Module):
    def __init__(self, d_model, nhead, dim_feedforward, dropout=0.1):
        super(CustomTransformerEncoderLayer, self).__init__()
        self.self_attention = CustomMultiheadAttention(d_model, nhead)
        self.dropout1 = nn.Dropout(dropout)
        self.norm1 = nn.LayerNorm(d_model)

        self.feedforward = nn.Sequential(
            nn.Linear(d_model, dim_feedforward),
            nn.ReLU(),
            nn.Linear(dim_feedforward, d_model),
        )
        self.dropout2 = nn.Dropout(dropout)
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, src):
        attn_output, attn_weights = self.self_attention(src)
        src = self.norm1(src + self.dropout1(attn_output))
        feedforward_output = self.feedforward(src)
        src = self.norm2(src + self.dropout2(feedforward_output))
        return src, attn_weights


# Full Transformer Model (2-class classifier)
class FullMultiLevelTransformer(nn.Module):
    def __init__(self, input_dim, eqp_vocab_size, d_model=64, nhead=4, num_layers=2, dim_feedforward=128, dropout=0.1):
        super(FullMultiLevelTransformer, self).__init__()
        self.d_model = d_model

        self.eqp_embedding = nn.Embedding(eqp_vocab_size, d_model)
        self.feature_embedding = nn.Linear(input_dim, d_model)

        self.feature_transformer = nn.ModuleList([
            CustomTransformerEncoderLayer(d_model, nhead, dim_feedforward, dropout)
            for _ in range(num_layers)
        ])
        self.fc = nn.Linear(d_model, 2)  # 2-class classification

    def forward(self, features, eqp_ids):
        features = features.unsqueeze(2)  # (batch, seq_len, 1)
        feature_embed = self.feature_embedding(features)  # (batch, seq_len, d_model)
        eqp_embed = self.eqp_embedding(eqp_ids).unsqueeze(1)  # (batch, 1, d_model)

        combined_features = feature_embed + eqp_embed

        attention_scores = []
        for layer in self.feature_transformer:
            combined_features, attn_weights = layer(combined_features)
            attention_scores.append(attn_weights)

        pooled = combined_features.mean(dim=1)  # (batch, d_model)
        logits = self.fc(pooled)  # (batch, 2)
        return logits, attention_scores


# 변수 중요도 계산
def compute_variable_importance(attention_scores):
    mean_attention = attention_scores.mean(dim=(0, 1))  # (seq_len, seq_len)
    variable_importance = mean_attention.mean(dim=0)
    return variable_importance


# 학습 코드 예시 (2-class)
model = FullMultiLevelTransformer(
    input_dim=INPUT_DIM,
    eqp_vocab_size=EQP_VOCAB_SIZE,
    d_model=64,
    nhead=4,
    num_layers=2,
    dim_feedforward=128
)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
criterion = nn.CrossEntropyLoss()  # 2-class classification용
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 학습 함수 호출 예시
train_model_inputs(
    model=model,
    train_loader=train_loader,
    val_loader=val_loader,
    criterion=criterion,
    optimizer=optimizer,
    num_epochs=2000,
    device=device,
    save_path="model_weights_binary_2class.pth"
)