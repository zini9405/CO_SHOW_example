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
import random
import pickle
from sklearn.model_selection import train_test_split

import torch.nn.functional as F

def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

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

        # Linear projections
        Q = self.query(x)  # (batch_size, seq_len, d_model)
        K = self.key(x)    # (batch_size, seq_len, d_model)
        V = self.value(x)  # (batch_size, seq_len, d_model)

        # Reshape for multihead attention
        Q = Q.view(batch_size, seq_len, self.nhead, self.head_dim).transpose(1, 2)  # (batch_size, nhead, seq_len, head_dim)
        K = K.view(batch_size, seq_len, self.nhead, self.head_dim).transpose(1, 2)  # (batch_size, nhead, seq_len, head_dim)
        V = V.view(batch_size, seq_len, self.nhead, self.head_dim).transpose(1, 2)  # (batch_size, nhead, seq_len, head_dim)

        # Scaled dot-product attention
        attn_scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.head_dim ** 0.5)  # (batch_size, nhead, seq_len, seq_len)
        attn_weights = F.softmax(attn_scores, dim=-1)  # (batch_size, nhead, seq_len, seq_len)

        # Weighted sum of values
        attn_output = torch.matmul(attn_weights, V)  # (batch_size, nhead, seq_len, head_dim)

        # Combine heads
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, seq_len, d_model)  # (batch_size, seq_len, d_model)

        # Final linear projection
        output = self.out(attn_output)  # (batch_size, seq_len, d_model)

        return output, attn_weights  # Return attention weights for analysis


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
        # Self-attention
        attn_output, attn_weights = self.self_attention(src)
        src = self.norm1(src + self.dropout1(attn_output))

        # Feedforward
        feedforward_output = self.feedforward(src)
        src = self.norm2(src + self.dropout2(feedforward_output))

        return src, attn_weights  # Return attention weights


# Full Transformer Model
class FullMultiLevelTransformer(nn.Module):
    def __init__(self, input_dim, eqp_vocab_size, d_model=64, nhead=4, num_layers=2, dim_feedforward=128, dropout=0.1):
        super(FullMultiLevelTransformer, self).__init__()
        self.d_model = d_model

        self.eqp_embedding = nn.Embedding(eqp_vocab_size, d_model)  # Embedding for equipment IDs
        self.feature_embedding = nn.Linear(input_dim, d_model)
        self.feature_transformer = nn.ModuleList([
            CustomTransformerEncoderLayer(d_model, nhead, dim_feedforward, dropout)
            for _ in range(num_layers)
        ])
        self.fc = nn.Linear(d_model, 1)

    def forward(self, features, eqp_ids):
        features = features.unsqueeze(2)
        feature_embed = self.feature_embedding(features)

        eqp_embed = self.eqp_embedding(eqp_ids).unsqueeze(1)  # (batch_size, 1, d_model)

        combined_features = feature_embed + eqp_embed  # Combine feature and equipment embeddings

        attention_scores = []

        for layer in self.feature_transformer:
            combined_features, attn_weights = layer(combined_features)
            attention_scores.append(attn_weights)

        # Pooling and final output
        output = combined_features.mean(dim=1)  # Mean pooling
        return self.fc(output), attention_scores  # Return predictions and attention scores


# 중요도 계산 함수
def compute_variable_importance(attention_scores):
    """
    Calculate importance scores for each variable from attention scores.

    Args:
        attention_scores: Tensor of shape (batch_size, nhead, seq_len, seq_len)

    Returns:
        importance_scores: Tensor of shape (seq_len,)
    """
    # 1. 배치와 헤드 차원을 평균
    mean_attention = attention_scores.mean(dim=(0, 1))  # (seq_len, seq_len)

    # 2. Query 기준으로 평균을 내어 변수별 중요도 계산
    variable_importance = mean_attention.mean(dim=0)  # (seq_len,)

    return variable_importance

# Custom Dataset 정의
class CustomDataset(Dataset):
    def __init__(self, df, eqp_mapping):
        self.data = df
        self.labels = self.data['GBIR_AFS2'].values
        self.eqp_mapping = eqp_mapping
        self.quantile_transformer = QuantileTransformer(output_distribution='normal', random_state=42)
        self.labels = self.quantile_transformer.fit_transform(self.labels.reshape(-1, 1)).flatten()
        self.features = self.data.drop(columns=['BASE_DT', 'EQP_ID', 'WAF_ID', 'GBIR_AFS2']).values


        self.eqp_ids = self.data['EQP_ID'].map(self.eqp_mapping).values

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        features = torch.tensor(self.features[idx], dtype=torch.float32)
        label = torch.tensor(self.labels[idx], dtype=torch.float32)
        eqp_id = torch.tensor(self.eqp_ids[idx], dtype=torch.long)
        return features, eqp_id, label


from sklearn.preprocessing import MinMaxScaler

# 데이터 매핑 함수
def map_to_numeric(values):
    mapping = {val: idx for idx, val in enumerate(sorted(values))}
    return mapping

def train_val_split(dataset, val_ratio=0.2):
    val_size = int(len(dataset) * val_ratio)
    train_size = len(dataset) - val_size
    
    train_dataset = dataset[:train_size]  # 앞부분을 train으로
    val_dataset = dataset[train_size:]  # 뒷부분을 val로
    
    return train_dataset, val_dataset

# 정확도 계산 함수
def calculate_accuracy(output, target, threshold=0.001):
    correct = torch.abs(output - target) <= threshold
    return correct.sum().item() / len(target)

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

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_embeddings = scaler.fit_transform(reduced_embeddings)

    # EQP_ID_MODULE_NAME 레이블 가져오기
    eqp_labels = list(eqp_mapping.keys())


        # 5. 결과를 데이터프레임으로 저장
    embedding_df = pd.DataFrame({
        "EQP_ID": eqp_labels,
        "X": scaled_embeddings[:, 0],
        "Y": scaled_embeddings[:, 1]
    })

    # 시각화
    plt.figure(figsize=(12, 8))
    for i, label in enumerate(eqp_labels):
        print(reduced_embeddings[i, 0], reduced_embeddings[i, 1], label)
        plt.scatter(reduced_embeddings[i, 0], reduced_embeddings[i, 1], label=label)
        plt.text(reduced_embeddings[i, 0], reduced_embeddings[i, 1], label, fontsize=9)
    
    plt.title("EQP_ID_MODULE_NAME Embedding Visualization")
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

    return embedding_df

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

def standardize_new_data(new_df, scaler_path):
    # 저장된 스케일러 불러오기 (dict 형태)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    # 표준화 제외할 열
    exclude_columns = ['BASE_DT', 'EQP_ID', 'WAF_ID', 'GBIR_AFS2']

    # 숫자형 열 중 제외할 열을 제외한 리스트
    numerical_columns = [col for col in new_df.select_dtypes(include=['number']).columns if col not in exclude_columns]
    
    # 표준화 적용 (X_scaled = (X - mean) / scale)
    new_df_standardized = new_df.copy()
    
    for col in numerical_columns:
        if col in scaler:
            mean = scaler[col]['mean']
            scale = scaler[col]['scale']
            new_df_standardized[col] = (new_df[col] - mean) / scale  # 직접 표준화 수식 적용

    return new_df_standardized


# 모델 훈련 루프
def train_model_inputs(model, train_loader, val_loader, criterion, optimizer, num_epochs, device, save_path):
    model.to(device)
    best_val_loss = float('inf')

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        train_pbar = tqdm(train_loader, desc=f"Training Epoch {epoch + 1}/{num_epochs}")
        for batch_features, batch_eqp_ids, batch_labels in train_pbar:
            batch_features, batch_eqp_ids, batch_labels = (
                batch_features.to(device), batch_eqp_ids.to(device), batch_labels.to(device)
            )
            outputs, attention_scores = model(batch_features, batch_eqp_ids)
            # print('batch_labels', batch_labels)
            loss = criterion(outputs.squeeze(), batch_labels)
            # print(loss)
            # print(batch_features)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            train_pbar.set_postfix(loss=loss.item())

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            val_pbar = tqdm(val_loader, desc=f"Validation Epoch {epoch + 1}/{num_epochs}")
            for batch_features, batch_eqp_ids, batch_labels in val_pbar:
                batch_features, batch_eqp_ids, batch_labels = (
                    batch_features.to(device), batch_eqp_ids.to(device), batch_labels.to(device)
                )
                outputs, attention_scores = model(batch_features, batch_eqp_ids)
                loss = criterion(outputs.squeeze(), batch_labels)
                val_loss += loss.item()

        avg_val_loss = val_loss / len(val_loader)

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), save_path)
            print(f"Best model saved with validation loss: {best_val_loss:.4f}")


  # 테스트 함수
def test_model(model, test_loader, device, load_path):
    model.load_state_dict(torch.load(load_path))
    model.to(device)
    model.eval()
    predictions = []
    true_labels = []
    att_scores = []
    with torch.no_grad():
        for batch_features, batch_eqp_ids, batch_labels in tqdm(test_loader, desc="Testing"):
            batch_features, batch_eqp_ids, batch_labels = (
            batch_features.to(device), batch_eqp_ids.to(device), batch_labels.to(device)
        )
            outputs, attention_scores = model(batch_features, batch_eqp_ids)
            outputs = outputs.squeeze()

            predictions.extend(outputs.cpu().numpy())
            true_labels.extend(batch_labels.cpu().numpy())
            att_scores.append(attention_scores)
    return predictions, true_labels, att_scores


# Main 실행
def main():
    csv_file = 'STEP_6_all.csv'
    scaler_path = 'scalers_all.pkl'
    df = pd.read_csv(csv_file)

    EQP_ID_MODULE_NAME = {'TPDPS47', 'BPDPD113', 'BPDPS06', 'BPDPD97', 'BPDPD87', 'BPDPS22', 'BPDPS72', 'BPDPD91', 'BPDPS13', 'BPDPD89', 'BPDPD82', 'BPDPD94', 'TPDPD67', 'BPDPD88', 'BPDPS18', 'TPDPS54', 
                          'BPDPD103', 'BPDPS23', 'BPDPS71', 'BPDPD116', 'BPDPS49', 'BPDPS43', 'TPDPS49', 'BPDPD85', 'BPDPD119', 'BPDPD117', 'BPDPD108', 'BPDPD112', 'TPDPS27', 'TPDPD65', 'BPDPD96', 'TPDPD72',
                           'BPDPL79', 'BPDPD102', 'TPDPD68', 'TPDPD70', 'BPDPS15', 'BPDPD118', 'BPDPD99', 'TPDPS46', 'BPDPS34', 'BPDPD106', 'BPDPD80', 'TPDPS48', 'BPDPS25', 'BPDPD115', 'BPDPD107', 'BPDPD86', 'TPDPD69',
                             'BPDPD109', 'BPDPD98', 'BPDPD81', 'BPDPD100', 'BPDPS73', 'TPDPD66', 'TPDPS16', 'BPDPS70', 'BPDPS65', 'BPDPD104', 
                          'BPDPD84', 'BPDPD92', 'BPDPD93', 'BPDPD83', 'BPDPD101', 'BPDPD111', 'BPDPD114', 'BPDPD90', 'TPDPS26', 'BPDPS33', 'BPDPS62', 'BPDPD95', 'BPDPD74', 'BPDPD105', 'TPDPD71'}

    eqp_mapping = map_to_numeric(EQP_ID_MODULE_NAME)

    df = standardize_new_data(df, scaler_path)

    df = df.sort_values(by=["BASE_DT", "WAF_ID"], ascending=[True, True])
    
    df = df.dropna(subset=['GBIR_AFS2'])

    df.fillna(0, inplace=True)

    df.dropna(axis=0)

    waf_ids = df["WAF_ID"].unique()
    train_ids, val_ids = train_test_split(waf_ids, test_size=0.1, shuffle=False)  # 순서 유지
    train_datasaet = df[df["WAF_ID"].isin(train_ids)]
    val_datasaet = df[df["WAF_ID"].isin(val_ids)]

    train_loader = CustomDataset(train_datasaet, eqp_mapping)
    val_loader = CustomDataset(val_datasaet, eqp_mapping)

    
    train_loader = DataLoader(train_loader, batch_size=512, shuffle=True)
    val_loader = DataLoader(val_loader, batch_size=512, shuffle=False)

    model = FullMultiLevelTransformer(input_dim=1, eqp_vocab_size=len(eqp_mapping), d_model=512, nhead=8, num_layers=6, dim_feedforward=512)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    save_path = "model_weights_GBIR_25312_6_all.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_model_inputs(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        criterion=nn.HuberLoss(delta=1.0),
        optimizer=optimizer,
        num_epochs=2000,
        device=device,
        save_path=save_path
    )

if __name__ == "__main__":
    set_seed(42)
    main()
