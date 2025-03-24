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
        self.fc = nn.Linear(d_model, 2)

    def forward(self, features, eqp_ids):
        features = features.unsqueeze(2)
        feature_embed = self.feature_embedding(features)

        eqp_embed = self.eqp_embedding(eqp_ids).unsqueeze(1)  # (batch_size, 1, d_model)

        combined_features = feature_embed + eqp_embed  # Combine feature and equipment embeddings

        attention_scores = []

        for layer in self.feature_transformer:
            combined_features, attn_weights = layer(combined_features)
            attention_scores.append(attn_weights)

        pooled = combined_features.mean(dim=1)  # (batch, d_model)
        logits = self.fc(pooled)  # (batch, 2)
        return logits, attention_scores



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

class CustomDataset(Dataset):
    def __init__(self, df, eqp_mapping):
        self.data = df
        self.eqp_mapping = eqp_mapping
        self.labels = self.data['SFQR_AFS2'].values
        # 정규 분포로 변환
        # self.quantile_transformer = QuantileTransformer(output_distribution='normal', random_state=42)
        # transformed_labels = self.quantile_transformer.fit_transform(self.labels.reshape(-1, 1)).flatten()

        # 0.5 기준으로 이진 분류 라벨 생성
        self.labels = (self.labels > 0.5).astype(np.int64)

        # Feature 추출
        self.features = self.data.drop(columns=[
            'WAF_ID', 'HST_REG_DTTM', 'SFQR_AFS2', 'ESFQR2_MAX_AFS2', 'ZDDFRONTMEAN_01_AFS2',
            'ESFQD_ZONE1MEAN_AFS2', 'ESFQD2_ZONE1MEAN_AFS2', 'SFQR_AFS2_SUB', 'ESFQR2_MAX_AFS2_SUB', 'ESFQD_ZONE1MEAN_AFS2_SUB',
            'ESFQD2_ZONE1MEAN_AFS2_SUB', 'EQP_ID_MODULE_NAME'
        ]).values
        # Equipment ID 인코딩
        self.eqp_ids = self.data['EQP_ID_MODULE_NAME'].map(self.eqp_mapping).values

    def __len__(self):
        return len(self.data)

    # def __getitem__(self, idx):
    #     features = torch.tensor(self.features[idx], dtype=torch.float32)
    #     label = torch.tensor(self.labels[idx], dtype=torch.long)
    #     print(label.shape)
    #     eqp_id = torch.tensor(self.eqp_ids[idx], dtype=torch.long)
    #     return features, eqp_id, label
    
    def __getitem__(self, idx):
        features = torch.tensor(self.features[idx], dtype=torch.float32)
        eqp_id = torch.tensor(self.eqp_ids[idx], dtype=torch.long)
        label = torch.tensor(self.labels[idx].squeeze(), dtype=torch.long)

        # 디버깅 출력
        print("features.shape:", features.shape)
        print("eqp_id:", eqp_id)
        print("label:", label)

        return features, eqp_id, label

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

    # EQP_ID_MODULE_NAME 레이블 가져오기
    eqp_labels = list(eqp_mapping.keys())

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

# 새 데이터에 대해 동일한 scaler 사용
def standardize_new_data(new_df, scaler_path):
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    exclude_columns = ['SFQR_AFS2', 'ESFQR2_MAX_AFS2', 'ZDDFRONTMEAN_01_AFS2', 'ESFQD_ZONE1MEAN_AFS2', 'ESFQD2_ZONE1MEAN_AFS2', 'SFQR_AFS2_SUB', 
                       'ESFQR2_MAX_AFS2_SUB', 'ZDDFRONTMEAN_01_AFS2_SUB', 'ESFQD_ZONE1MEAN_AFS2_SUB', 'ESFQD2_ZONE1MEAN_AFS2_SUB',
                       'ESFQD2_ZONE1MAX_AFS2', 'ESFQD2_ZONE1MAX_AFS2_SUB', 'ESFQD_ZONE1MAX_AFS2', 'ESFQD_ZONE1MAX_AFS2_SUB']

    # 숫자형 열 중 제외할 열 제외
    numerical_columns = [col for col in new_df.select_dtypes(include=['number']).columns if col not in exclude_columns]
    
    new_df_standardized = new_df.copy()
    new_df_standardized[numerical_columns] = scaler.transform(new_df[numerical_columns])
    
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
            # loss = criterion(outputs.squeeze(), batch_labels)
            loss = criterion(outputs, batch_labels)
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
                # loss = criterion(outputs.squeeze(), batch_labels)
                loss = criterion(outputs, batch_labels)
                val_loss += loss.item()

        avg_val_loss = val_loss / len(val_loader)

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), save_path)
            print(f"Best model saved with validation loss: {best_val_loss:.4f}")


# Main 실행
def main():
    csv_file = 'all.csv'
    scaler_path = 'scaler_params.pkl'
    df = pd.read_csv(csv_file)

    # RECIPE_ID = {'MIC_01_CA', 'SL_CA', 'MIC_01_CB', 'CIS_P_SKH6_CB', 'INTEL14_CA', 'SEC_L58_CA', 'CIS_P+_GLX5_CB', 'LOG_TSM3_CB', 'SL_CB', 'CIS_P+_SKH9_CA', 'MXIC_01_CB', 'CIS_P_SKH6_CA', 'TSMC_CB', 'CIS_CB', 'STM_P+_CB', 'S14_CB', 'SMIC4_R0_CA', 'INTEL7_CA', 'GF_01_CA', 'CIS_P+_SMI4_CA', 'GF_02_CB', 'SKH_CIS_P+_CB', 'GF_01_CB', 'CIS_P+_HUA4_CA', 'CIS_P+_CXT5_CB', 'GF_03_CB', 'TSMC2_CB', 'CIS_P+_CA', 'S14_CA', 'CIS_P+_SKH6_CA', 'SKH_CIS_P+_CA', 'L2_CB', 'HUALI_01_CB', 'GF_02_CA', 'CIS_P+_HUA4_CB', 'INTEL2_CB', 'INTEL10_CA', 'TSMC2_CA', 'PSMC_02_CB', 'CIS_P+_ONS6_CB', 'GF_03_CA', 'CAN3_01_CB', 'CIS_P+_SKH9_CB', 'SMIC2_R0_CB', 'PSMC_FSI_CA', 'TSMC_CA', 'CIS_P+_SKH6_CB', 'CIS_P+_PSM4_CA', 'UMC_R0_CA', 'STM_P+_CA', 
    #           'STM_01_CB', 'HUALI_01_CA', 'UMC_R0_CB', 'CIS_P+_ICR5_CB', 'TIX_R1_CB', 'LOG_TSM1_CA', 'TIX_R1_CA', 'INTEL14_CB', 'TIX_R0_CA', 'PSMC_02_CA', 'CIS_P+_UMC4_CB', 'SEC_L58_CB', 'SMIC2_R0_CA', 'SMIC_L7_CA', 'TIX_R0_CB', 'MXIC_01_CA', 'CIS_P+_GLX5_CA', 'CIS_P+_CB', 'STM_01_CA', 'LOG_TSM3_CA', 'CIS_P+_ONS6_CA', 'CIS_CA', 'SKH_CIS_CA', 'CIS_P+_UMC4_CA', 'INTEL7_CB', 'INTEL2_CA', 'SMIC_L7_CB', 'CAN3_01_CA', 'INTEL10_CB', 'LOG_TSM1_CB'}
    

    RECIPE_ID = {'L2_CB', 'GF_03_CA', 'TSMC_CB', 'CIS_P+_PSM4_CA', 'GF_02_CB', 'MXIC_01_CB', 'UMC_R0_CB', 'CIS_P+_SKH6_CA', 'CAN3_01_CA', 'CIS_P+_CB', 'HUALI_01_CA', 'TSMC2_CA', 
                'GF_01_CB', 'SKH_CIS_P+_CA', 'CIS_P+_SKH9_CB', 'CIS_P+_ONS6_CB', 'CIS_P+_ONS6_CA', 'STM_P+_CB', 'SKH_CIS_P+_CB', 'LOG_TSM3_CB', 'LOG_TSM3_CA', 'PSMC_02_CB', 'SL_CA',
                'STM_P+_CA', 'GF_03_CB', 'INTEL7_CB', 'LOG_TSM1_CB', 'CIS_P+_GLX5_CA', 'SEC_L58_CA', 'SMIC2_R0_CA', 'PSMC_FSI_CA', 'CAN3_01_CB', 'PSMC_02_CA', 'MIC_01_CB', 'CIS_P_SKH6_CA', 
                'TIX_R1_CB', 'LOG_TSM1_CA', 'MXIC_01_CA', 'CIS_P+_SKH6_CB', 'CIS_P+_SKH9_CA', 'SMIC4_R0_CA', 'GF_01_CA', 'INTEL14_CA', 'INTEL10_CB', 'GF_02_CA', 'SMIC_L7_CA', 'CIS_P+_UMC4_CA',
                'TIX_R0_CB', 'SL_CB', 'TIX_R1_CA', 'CIS_P_SKH6_CB', 'CIS_P+_GLX5_CB', 'HUALI_01_CB', 'TSMC2_CB', 'CIS_P+_SMI4_CA', 'CIS_P+_HUA4_CA', 'INTEL10_CA', 'SMIC_L7_CB', 'CIS_P+_CA', 
                'CIS_P+_ICR5_CB', 'TSMC_CA', 'SKH_CIS_CA', 'SEC_L58_CB', 'INTEL14_CB', 'CIS_P+_HUA4_CB', 'MIC_01_CA', 'CIS_P+_CXT5_CB', 'STM_01_CB', 'S14_CA', 'CIS_P+_UMC4_CB', 'INTEL2_CB', 'STM_01_CA', 
                'INTEL2_CA', 'CIS_CB', 'SMIC2_R0_CB', 'TIX_R0_CA', 'UMC_R0_CA', 'INTEL7_CA', 'CIS_CA', 'S14_CB'}

    # EQP_ID_MODULE_NAME = {'CENC10A', 'CENC10B', 'CENC11A', 'CENC11B', 'CENC12A', 'CENC12B', 'CENC13A', 'CENC13B', 'CENC14A', 'CENC14B', 'CENC15A', 'CENC15B', 'CENC16A', 'CENC16B', 'CENC17A', 'CENC17B', 'CENC31A', 'CENC31B', 'CENC32A',
    # 'CENC32B', 'CENC33A', 'CENC33B', 'CENC34A', 'CENC34B', 'CENC35A', 'CENC35B', 'CENC36A', 'CENC36B', 'CENC41A', 'CENC41B', 'CENC42A', 'CENC42B', 'CENC43A', 'CENC43B', 'CENC44A', 'CENC44B', 'CENC45A', 'CENC45B',
    # 'CENC46A', 'CENC46B', 'CENC47A', 'CENC47B', 'CENC48A', 'CENC48B', 'CENC5A', 'CENC5B', 'CENC6A', 'CENC6B', 'CENC7A', 'CENC7B', 'CENC8A', 'CENC8B', 'CENC9A', 'CENC9B', 'ZCENC01A', 'ZCENC01B', 'ZCENC02A', 'ZCENC02B',
    # 'ZCENC03A', 'ZCENC03B', 'ZCENC04A', 'ZCENC04B'}

    EQP_ID_MODULE_NAME = {'CENC42B', 'ZCENC04A', 'CENC33B', 'CENC12A', 'CENC10A', 'CENC13A', 'CENC8B', 'CENC48A', 'CENC41B', 'ZCENC02A', 'CENC17B', 'CENC34A', 'CENC48B', 'CENC14B', 'CENC46B', 
                          'ZCENC03A', 'CENC8A', 'CENC14A', 'CENC15B', 'CENC16B', 'CENC33A', 'CENC31B', 'CENC47B', 'CENC43B', 'CENC17A', 'ZCENC01B', 'CENC11B', 'ZCENC03B', 'ZCENC04B', 'CENC35B', 
                          'CENC35A', 'CENC11A', 'CENC9B', 'CENC34B', 'CENC44B', 'CENC42A', 'CENC36A', 'CENC16A', 'CENC31A', 'CENC32A', 'CENC10B', 'CENC45A', 'CENC43A', 'CENC44A', 'CENC7B', 'CENC36B', 
                          'CENC12B', 'CENC7A', 'CENC15A', 'CENC46A', 'CENC6B', 'CENC6A', 'CENC13B', 'CENC9A', 'CENC41A', 'ZCENC01A', 'CENC5A', 'CENC5B', 'CENC45B', 'ZCENC02B', 'CENC32B', 'CENC47A'}

    recipe_mapping = map_to_numeric(RECIPE_ID)
    eqp_mapping = map_to_numeric(EQP_ID_MODULE_NAME)

    df = standardize_new_data(df, scaler_path)
    
    # df = df.dropna(subset=['SFQR_AFS2', 'SFQR_AFS2_SUB'])
    df = df.dropna(subset=['ZDDFRONTMEAN_01_AFS2', 'ZDDFRONTMEAN_01_AFS2_SUB'])

    df.fillna(0, inplace=True)

    # print(df.isnull().sum())
    
    df = df.sort_values("HST_REG_DTTM")

    df = df.drop(columns=['ESFQD2_ZONE1MAX_AFS2', 'ESFQD2_ZONE1MAX_AFS2_SUB', 'ESFQD_ZONE1MAX_AFS2', 'ESFQD_ZONE1MAX_AFS2_SUB'])

    df.dropna(axis=0)

    # print(set(df['RECIPE_ID']))

    if "RECIPE_ID" in df.columns:
        df["RECIPE_ID"] = df["RECIPE_ID"].map(recipe_mapping)

    dataset = CustomDataset(df, eqp_mapping)

    train_dataset, val_dataset = train_val_split(dataset, val_ratio=0.2)
    
    train_loader = DataLoader(train_dataset, batch_size=512, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=512, shuffle=False)

    model = FullMultiLevelTransformer(input_dim=1, eqp_vocab_size=len(eqp_mapping), d_model=256, nhead=4, num_layers=4, dim_feedforward=512)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    save_path = "model_weights_epi_250324.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    criterion = nn.CrossEntropyLoss()

    train_model_inputs(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        criterion=criterion,
        optimizer=optimizer,
        num_epochs=2000,
        device=device,
        save_path=save_path
    )

if __name__ == "__main__":
    set_seed(42)
    main()


features.shape: torch.Size([1249244, 32])
eqp_id: tensor([24,  8, 11,  ..., 52, 37, 41])
label: tensor([0, 0, 0,  ..., 0, 0, 0])
features.shape: torch.Size([312310, 32])
eqp_id: tensor([13, 20, 39,  ..., 40, 35, 35])
label: tensor([0, 0, 0,  ..., 0, 0, 0])
Training Epoch 1/2000:   0%|          | 0/1 [00:00<?, ?it/s]
---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
Cell In[44], line 78
     76 if __name__ == "__main__":
     77     set_seed(42)
---> 78     main()

Cell In[44], line 65
     62 device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
     63 criterion = nn.CrossEntropyLoss()
---> 65 train_model_inputs(
     66     model=model,
     67     train_loader=train_loader,
     68     val_loader=val_loader,
     69     criterion=criterion,
     70     optimizer=optimizer,
     71     num_epochs=2000,
     72     device=device,
     73     save_path=save_path
     74 )

Cell In[42], line 10
      8 running_loss = 0.0
      9 train_pbar = tqdm(train_loader, desc=f"Training Epoch {epoch + 1}/{num_epochs}")
---> 10 for batch_features, batch_eqp_ids, batch_labels in train_pbar:
...
    211     storage = elem._typed_storage()._new_shared(numel, device=elem.device)
    212     out = elem.new(storage).resize_(len(batch), *list(elem.size()))
--> 213 return torch.stack(batch, 0, out=out)

RuntimeError: stack expects each tensor to be equal size, but got [1249244, 32] at entry 0 and [1249244] at entry 1
