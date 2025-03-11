import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

# 랜덤시드 고정 (재현 가능성 확보용)
np.random.seed(42)

# 1. STEP.csv 데이터 로드
df = pd.read_csv('STEP.csv')

# 필요한 컬럼만 선별 (WAF_ID, EQP_ID, STEP, Target, Feature columns 등)
# 불필요한 컬럼이 있다면 제거합니다. 여기서는 가정적으로 진행합니다.
# (예를 들어 'LOT_ID'나 기타 식별자는 필요 없다고 가정)
# df = df[['WAF_ID', 'EQP_ID', 'STEP', 'Target', ...<feature columns>...]]

# 2. EQP_ID 레이블 인코딩 (임베딩 입력으로 변환)
le = LabelEncoder()
df['EQP_ID_enc'] = le.fit_transform(df['EQP_ID'])

# 3. Wafer별로 9개 공정 스텝씩 그룹화하기 위해 WAF_ID와 STEP 순으로 정렬
df = df.sort_values(['WAF_ID', 'STEP'])

# 4. 그룹화하여 시퀀스 데이터 생성
X_all, eqp_all, y_all = [], [], []
for wafer_id, group in df.groupby('WAF_ID'):
    group = group.sort_values('STEP')
    # 9개 스텝이 모두 존재하는 Wafer만 사용 (길이 체크)
    if len(group) == 9:
        # 장비 ID (레이블 인코딩 값) - Wafer 내 모든 행이 동일한 EQP_ID라고 가정
        eqp_val = group['EQP_ID_enc'].iloc[0]
        # 타겟 값 (예: 마지막 스텝에서의 목표 변수) - 여기서는 마지막 행의 Target을 사용
        target_val = group.iloc[-1]['Target'] if 'Target' in group.columns else group.iloc[-1]['Y']
        # 입력 특징 컬럼들 (ID나 Target 제외)
        feature_cols = [col for col in group.columns 
                        if col not in ['WAF_ID', 'EQP_ID', 'EQP_ID_enc', 'STEP', 'Target', 'Y']]
        # 시퀀스 특징 데이터 (9 x num_features 형태)
        X_seq = group[feature_cols].values  # shape: (9, num_features)
        X_all.append(X_seq)
        eqp_all.append(eqp_val)
        y_all.append(target_val)

# 리스트를 numpy 배열로 변환
X_all = np.array(X_all)
eqp_all = np.array(eqp_all)
y_all = np.array(y_all)

# 5. 학습/검증/테스트 세트 분할 (예: 70%/15%/15%)
num_samples = len(X_all)
indices = np.arange(num_samples)
np.random.shuffle(indices)
train_idx = int(num_samples * 0.7)
val_idx = int(num_samples * 0.85)
train_indices = indices[:train_idx]
val_indices   = indices[train_idx:val_idx]
test_indices  = indices[val_idx:]

X_train, eqp_train, y_train = X_all[train_indices], eqp_all[train_indices], y_all[train_indices]
X_val, eqp_val, y_val       = X_all[val_indices], eqp_all[val_indices], y_all[val_indices]
X_test, eqp_test, y_test    = X_all[test_indices], eqp_all[test_indices], y_all[test_indices]

# 6. 특징 데이터 정규화 (StandardScaler를 사용하여 각 feature 컬럼 z-score 정규화)
scaler = StandardScaler()
# 학습 세트의 feature로 스케일러 학습 (시퀀스 전체를 하나의 feature 집합으로 취급)
X_train_flat = X_train.reshape(-1, X_train.shape[-1])  # (train_samples*9, num_features)
scaler.fit(X_train_flat)
# 학습/검증/테스트에 동일한 스케일 적용
X_train = scaler.transform(X_train_flat).reshape(X_train.shape)
X_val   = scaler.transform(X_val.reshape(-1, X_val.shape[-1])).reshape(X_val.shape) if len(X_val) else X_val
X_test  = scaler.transform(X_test.reshape(-1, X_test.shape[-1])).reshape(X_test.shape)

import torch
from torch.utils.data import Dataset, DataLoader

class WaferDataset(Dataset):
    def __init__(self, X, eqp, y):
        self.X = X
        self.eqp = eqp
        self.y = y
    def __len__(self):
        return len(self.X)
    def __getitem__(self, idx):
        # X: (9, num_features) -> float tensor
        features = torch.tensor(self.X[idx], dtype=torch.float32)
        # EQP ID: -> long tensor (임베딩용)
        eqp_id = torch.tensor(self.eqp[idx], dtype=torch.long)
        # 타겟: -> float tensor (shape (1,))
        target = torch.tensor(self.y[idx], dtype=torch.float32).unsqueeze(-1)
        return features, eqp_id, target

# Dataset 객체 생성
train_dataset = WaferDataset(X_train, eqp_train, y_train)
val_dataset   = WaferDataset(X_val, eqp_val, y_val)
test_dataset  = WaferDataset(X_test, eqp_test, y_test)

# DataLoader 정의 (배치 크기 32)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader   = DataLoader(val_dataset, batch_size=32, shuffle=False)
test_loader  = DataLoader(test_dataset, batch_size=32, shuffle=False)


import torch.nn as nn
import torch.nn.functional as F

class WaferTransformer(nn.Module):
    def __init__(self, num_features, num_eqp,
                 d_model=256, nhead=4, num_layers=4, dim_feedforward=512):
        super(WaferTransformer, self).__init__()
        self.d_model = d_model
        # 입력 특징을 d_model 차원으로 투영하는 선형층
        self.input_proj = nn.Linear(num_features, d_model)
        # EQP_ID 임베딩 (임베딩 차원을 d_model로 설정하여 더하기 연산이 가능하게 함)
        self.eqp_embedding = nn.Embedding(num_eqp, d_model)
        # Transformer Encoder 구성
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, 
                                                  dim_feedforward=dim_feedforward, 
                                                  batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        # 최종 출력 레이어 (d_model -> 1)
        self.fc_out = nn.Linear(d_model, 1)
    
    def forward(self, x, eqp_id):
        # x: (B, 9, num_features), eqp_id: (B,)
        # 입력 특징 투영
        x = self.input_proj(x)  # shape: (B, 9, d_model)
        # EQP 임베딩 벡터 추출
        eqp_vec = self.eqp_embedding(eqp_id)  # shape: (B, d_model)
        # EQP 임베딩을 시퀀스 길이에 맞게 확장하여 각 스텝 특징에 더함
        eqp_vec = eqp_vec.unsqueeze(1).expand(-1, x.size(1), -1)  # (B, 9, d_model)
        # 특징 + EQP임베딩 결합
        x = x + eqp_vec  # shape: (B, 9, d_model)
        # (필요 시 위치 인코딩 추가 가능하지만 여기서는 생략)
        # Transformer Encoder 통해 특징 추출
        x_enc = self.transformer(x)  # shape: (B, 9, d_model)
        # 시퀀스 마지막 스텝의 출력만 사용 (최종 결과 추정)
        x_last = x_enc[:, -1, :]     # shape: (B, d_model)
        out = self.fc_out(x_last)    # shape: (B, 1)
        return out

# 모델 생성 (특징 개수와 EQP 종류 개수 지정)
num_features = X_train.shape[2]  # 입력 특징 차원 수 (예: 27)
num_eqp = len(le.classes_)       # EQP_ID 종류 개수
model = WaferTransformer(num_features, num_eqp).to(torch.device('cpu'))  # 필요시 GPU 사용

# GPU 사용 가능하면 모델을 GPU로 이동
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)


import torch.optim as optim

criterion = nn.HuberLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-5)
num_epochs = 50
best_val_loss = float('inf')
best_model_path = "best_model.pth"

for epoch in range(1, num_epochs+1):
    model.train()
    train_loss_sum = 0.0
    # 4-1. 학습 단계
    for X_batch, eqp_batch, y_batch in train_loader:
        X_batch = X_batch.to(device)
        eqp_batch = eqp_batch.to(device)
        y_batch = y_batch.to(device)
        optimizer.zero_grad()
        # 예측
        preds = model(X_batch, eqp_batch)
        # 손실 계산 (Huber Loss)
        loss = criterion(preds, y_batch)
        # 역전파 및 가중치 업데이트
        loss.backward()
        optimizer.step()
        train_loss_sum += loss.item() * X_batch.size(0)
    train_loss = train_loss_sum / len(train_loader.dataset)
    
    # 4-2. 검증 단계 (평가 모드로 설정하고 기울기 계산 비활성화)
    model.eval()
    val_loss_sum = 0.0
    with torch.no_grad():
        for X_batch, eqp_batch, y_batch in val_loader:
            X_batch = X_batch.to(device)
            eqp_batch = eqp_batch.to(device)
            y_batch = y_batch.to(device)
            preds = model(X_batch, eqp_batch)
            loss = criterion(preds, y_batch)
            val_loss_sum += loss.item() * X_batch.size(0)
    val_loss = val_loss_sum / (len(val_loader.dataset) if len(val_loader.dataset)>0 else 1)
    
    # 검증 loss 기반으로 모델 저장
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        torch.save(model.state_dict(), best_model_path)
    
    # Epoch별 학습/검증 손실 출력
    print(f"Epoch {epoch:02d}: Train Loss = {train_loss:.6f}, Val Loss = {val_loss:.6f}")


from sklearn.metrics import r2_score

# 최적 모델 로드
model.load_state_dict(torch.load(best_model_path, map_location=device))
model.to(device)
model.eval()

# 테스트 세트에 대한 예측 수행
all_preds = []
all_targets = []
with torch.no_grad():
    for X_batch, eqp_batch, y_batch in test_loader:
        X_batch = X_batch.to(device)
        eqp_batch = eqp_batch.to(device)
        y_batch = y_batch.to(device)
        preds = model(X_batch, eqp_batch)  # 모델 예측 (B,1)
        # CPU로 이동하여 numpy 변환
        all_preds.append(preds.cpu().numpy())
        all_targets.append(y_batch.cpu().numpy())

# 리스트를 단일 배열로 결합
all_preds = np.vstack(all_preds).ravel()
all_targets = np.vstack(all_targets).ravel()

# R^2 스코어 및 상관계수 계산
r2 = r2_score(all_targets, all_preds)
corr = np.corrcoef(all_targets, all_preds)[0, 1]
print(f"Test R^2 Score: {r2:.4f}")
print(f"Test Pearson Correlation: {corr:.4f}")


import matplotlib.pyplot as plt

# 6-1. Transformer 어텐션 가중치 시각화 (예: 첫 번째 테스트 샘플, 첫 번째 인코더 레이어)
sample_X, sample_eqp, sample_y = test_dataset[0]  # 첫 번째 테스트 샘플
sample_X = sample_X.unsqueeze(0).to(device)   # (1, 9, num_features)
sample_eqp = sample_eqp.unsqueeze(0).to(device)  # (1,)
model.eval()
with torch.no_grad():
    # 모델의 첫 번째 TransformerEncoderLayer의 MultiheadAttention 모듈에 접근
    first_layer = model.transformer.layers[0]
    # 입력에 EQP 임베딩과 투영 적용 (transformer에 들어가는 값 계산)
    x_proj = model.input_proj(sample_X)                           # (1, 9, d_model)
    eqp_embed = model.eqp_embedding(sample_eqp).unsqueeze(1)      # (1, 1, d_model)
    eqp_embed = eqp_embed.expand(-1, x_proj.size(1), -1)          # (1, 9, d_model)
    x_input = x_proj + eqp_embed                                  # (1, 9, d_model)
    # 멀티헤드 어텐션 계산 (어텐션 가중치 반환 요청)
    attn_output, attn_weights = first_layer.self_attn(x_input, x_input, x_input, need_weights=True)
    # attn_weights: 어텐션 가중치 텐서 (shape: [1, 9, 9] - 모든 헤드 평균된 가중치)
    attn_matrix = attn_weights.squeeze(0).cpu().numpy()  # (9, 9)

# 어텐션 가중치 행렬 히트맵 시각화
plt.figure(figsize=(6,5))
plt.imshow(attn_matrix, origin='lower', cmap='viridis')
plt.colorbar(label="Attention Weight")
plt.title("Attention Weights (Encoder Layer 1)")
plt.xticks(ticks=range(9), labels=[f"Step{i+1}" for i in range(9)])
plt.yticks(ticks=range(9), labels=[f"Step{i+1}" for i in range(9)])
plt.xlabel("Key (Step)")
plt.ylabel("Query (Step)")
plt.show()

# 6-2. 예측 값 vs 실제 값 비교 그래프 (산점도)
plt.figure(figsize=(6,5))
plt.scatter(all_targets, all_preds, alpha=0.6, color='blue', edgecolors='white')
# y = x 대각선 표시
min_val = min(all_targets.min(), all_preds.min())
max_val = max(all_targets.max(), all_preds.max())
plt.plot([min_val, max_val], [min_val, max_val], 'r--')
plt.xlabel("Actual Value")
plt.ylabel("Predicted Value")
plt.title("Actual vs Predicted")
plt.show()
