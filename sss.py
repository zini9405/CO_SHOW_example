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
            print(f"Best model saved with validation loss: {best_val_loss:.4f}").


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
    csv_file = 'STEP_6.csv'
    scaler_path = 'scalers.pkl'
    df = pd.read_csv(csv_file)

    EQP_ID_MODULE_NAME = {"BPDPD100", "BPDPD101", "BPDPD102", "BPDPD103", "BPDPD104", "BPDPD105", "BPDPD106", "BPDPD107", 
    "BPDPD108", "BPDPD109", "BPDPD111", "BPDPD112", "BPDPD113", "BPDPD114", "BPDPD115", "BPDPD116", 
    "BPDPD117", "BPDPD118", "BPDPD119", "BPDPD74", "BPDPD80", "BPDPD81", "BPDPD82", "BPDPD83", 
    "BPDPD84", "BPDPD85", "BPDPD86", "BPDPD87", "BPDPD88", "BPDPD89", "BPDPD90", "BPDPD91", 
    "BPDPD92", "BPDPD93", "BPDPD94", "BPDPD95", "BPDPD96", "BPDPD97", "BPDPD98", "BPDPD99"
}

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

    model = FullMultiLevelTransformer(input_dim=1, eqp_vocab_size=len(eqp_mapping), d_model=256, nhead=4, num_layers=4, dim_feedforward=512)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    save_path = "model_weights_GBIR_25311.pth"
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


이 코드는 input (B, 변수 수), eqp (B), label (B)에 대한 transformer encoder 모델이야. 그런데 나는


import os
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# === 1. STEP.csv 불러오기 ===
file_path = "STEP.csv"  # 파일 경로 설정
df = pd.read_csv(file_path, encoding="utf-8")

# === 2. BASE_DT, WAF_ID, STEP_ID 정렬 ===
df = df.sort_values(by=["BASE_DT", "WAF_ID", "STEP_ID"], ascending=[True, True, True])

# === 3. EQP_ID를 숫자로 변환 (임베딩할 예정) ===
if "EQP_ID" in df.columns:
    eqp_encoder = LabelEncoder()
    df["EQP_ID"] = eqp_encoder.fit_transform(df["EQP_ID"])
else:
    eqp_encoder = None

# === 4. 필요없는 열 제거 (batch_data에서는 EQP_ID도 제거) ===
drop_columns = ["GBIR_AFS2", "WAF_ID", "BASE_DT", "PAD_TEMP_STEP_MEAN", "EQP_ID"]  # EQP_ID 제거
feature_columns = [col for col in df.columns if col not in drop_columns]

# === 5. 90:10 비율로 train/test 데이터 분할 ===
waf_ids = df["WAF_ID"].unique()
train_ids, val_ids = train_test_split(waf_ids, test_size=0.1, shuffle=False)  # 순서 유지
train_df = df[df["WAF_ID"].isin(train_ids)]
val_df = df[df["WAF_ID"].isin(val_ids)]

# === 6. PyTorch Dataset 클래스 정의 ===
class WaferDataset(Dataset):
    def __init__(self, dataframe, eqp_encoder, window_size=9):
        self.window_size = window_size
        self.groups = dataframe.groupby("WAF_ID")  # WAF_ID별 그룹화
        self.waf_ids = list(self.groups.groups.keys())  # WAF_ID 목록
        self.feature_columns = feature_columns
        self.eqp_encoder = eqp_encoder
        self.data_windows = self.create_windows()  # 9개씩 묶은 데이터 생성

    def create_windows(self):
        """
        WAF_ID별 STEP_ID를 정렬한 후 9개씩 묶어서 데이터를 만듦.
        """
        data_windows = []
        labels = []
        eqp_ids = []
        
        for waf_id in self.waf_ids:
            group_df = self.groups.get_group(waf_id).sort_values(by="STEP_ID")  # STEP_ID 정렬
            
            # 9개씩 슬라이딩 윈도우 생성
            for i in range(len(group_df) - self.window_size + 1):
                window = group_df.iloc[i : i + self.window_size]
                
                # Feature 값 추출 (L, feature 수), EQP_ID는 제외
                data = window[self.feature_columns].values
                data = torch.tensor(data, dtype=torch.float32)  # (9, feature 수)

                # Label 값 (마지막 row의 GBIR_AFS2 값 사용, 소수점 9자리 유지)
                label = torch.tensor(float(f"{window['GBIR_AFS2'].iloc[-1]:.9f}"), dtype=torch.float32)

                # EQP_ID 값 (첫 번째 row 기준, 임베딩용)
                eqp_id = torch.tensor(window["EQP_ID"].iloc[0], dtype=torch.long)

                data_windows.append((data, eqp_id, label))

        return data_windows

    def __len__(self):
        return len(self.data_windows)

    def __getitem__(self, idx):
        return self.data_windows[idx]

# === 7. Dataset 및 DataLoader 생성 ===
train_dataset = WaferDataset(train_df, eqp_encoder)
val_dataset = WaferDataset(val_df, eqp_encoder)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=False, collate_fn=lambda x: x)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, collate_fn=lambda x: x)

# === 8. nn.Embedding 생성 ===
num_eqp_ids = len(eqp_encoder.classes_) if eqp_encoder else 1  # EQP_ID가 없으면 1로 설정
embedding_dim = 256  # 원하는 임베딩 차원 설정
eqp_embedding = torch.nn.Embedding(num_eqp_ids, embedding_dim)

# === 9. 데이터 로더 테스트 ===
for batch in train_loader:
    batch_data, batch_eqp_ids, batch_labels = zip(*batch)  # 데이터 분리
    batch_data = torch.stack(batch_data)  # (B, 9, feature 수)
    batch_eqp_ids = torch.stack(batch_eqp_ids)
    batch_labels = torch.stack(batch_labels)

    # EQP_ID를 임베딩 벡터로 변환
    eqp_embedded = eqp_embedding(batch_eqp_ids)

    print(f"입력 데이터 크기: {batch_data.shape}")  # (B, 9, feature 수)
    print(f"임베딩 크기: {eqp_embedded.shape}")  # (B, embedding_dim)
    print(f"Label 크기: {batch_labels.shape}")  # (B, 1)
    print(f"Label 예시 (소수점 9자리 유지): {batch_labels[:5]}")
    break  # 한 batch만 확인

WaferDataset에 맞는 transformer encoder 코드로 변경해줘.
