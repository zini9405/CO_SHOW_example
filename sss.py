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

# === 3. 90:10 비율로 데이터 분할 ===
waf_ids = df["WAF_ID"].unique()
train_ids, val_ids = train_test_split(waf_ids, test_size=0.1, shuffle=False)  # 순서 유지
train_df = df[df["WAF_ID"].isin(train_ids)]
val_df = df[df["WAF_ID"].isin(val_ids)]

# === 4. 데이터 전처리 ===
# 제거할 열 목록 (label 및 불필요한 열)
drop_columns = ["GBIR_AFS2", "WAF_ID", "BASE_DT", "PAD_TEMP_STEP_MEAN"]
if "EQP_ID" in df.columns:
    drop_columns.remove("EQP_ID")  # EQP_ID는 변환해야 하므로 제거 X

# EQP_ID를 숫자로 변환 (임베딩할 예정)
eqp_encoder = LabelEncoder()
df["EQP_ID"] = eqp_encoder.fit_transform(df["EQP_ID"])

# 최종 사용할 입력 변수 목록
feature_columns = [col for col in df.columns if col not in drop_columns]

# === 5. PyTorch Dataset 클래스 정의 ===
class WaferDataset(Dataset):
    def __init__(self, dataframe, eqp_encoder):
        self.groups = dataframe.groupby("WAF_ID")
        self.waf_ids = list(self.groups.groups.keys())  # WAF_ID 목록
        self.feature_columns = feature_columns
        self.eqp_encoder = eqp_encoder

    def __len__(self):
        return len(self.waf_ids)

    def __getitem__(self, idx):
        waf_id = self.waf_ids[idx]
        group_df = self.groups.get_group(waf_id)  # WAF_ID별 데이터 가져오기

        # EQP_ID 추출 (임베딩용)
        eqp_id = group_df["EQP_ID"].iloc[0]  # 동일한 WAF_ID 내 EQP_ID는 같다고 가정

        # feature 값만 추출하여 tensor로 변환
        data = group_df[self.feature_columns].values
        data = torch.tensor(data, dtype=torch.float32)  # (L, 변수 개수)

        # Label (GBIR_AFS2) 값 가져오기
        label = torch.tensor(group_df["GBIR_AFS2"].iloc[0], dtype=torch.float32)  # (1)

        return data, torch.tensor(eqp_id, dtype=torch.long), label  # (L, 변수 개수), EQP_ID, (1)

# === 6. Dataset 및 DataLoader 생성 ===
train_dataset = WaferDataset(train_df, eqp_encoder)
val_dataset = WaferDataset(val_df, eqp_encoder)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, collate_fn=lambda x: x)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, collate_fn=lambda x: x)

# === 7. nn.Embedding 생성 ===
num_eqp_ids = len(eqp_encoder.classes_)
embedding_dim = 16  # 원하는 임베딩 차원 설정
eqp_embedding = torch.nn.Embedding(num_eqp_ids, embedding_dim)

# === 8. 데이터 로더 테스트 ===
for batch in train_loader:
    batch_data, batch_eqp_ids, batch_labels = zip(*batch)  # 데이터 분리
    batch_data = torch.nn.utils.rnn.pad_sequence(batch_data, batch_first=True)  # 패딩 적용
    batch_eqp_ids = torch.stack(batch_eqp_ids)
    batch_labels = torch.stack(batch_labels)

    # EQP_ID를 임베딩 벡터로 변환
    eqp_embedded = eqp_embedding(batch_eqp_ids)

    print(f"입력 데이터 크기: {batch_data.shape}")  # (B, L, 변수 개수)
    print(f"임베딩 크기: {eqp_embedded.shape}")  # (B, embedding_dim)
    print(f"Label 크기: {batch_labels.shape}")  # (B, 1)
    break  # 한 batch만 확인