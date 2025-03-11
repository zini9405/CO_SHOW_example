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
                label = torch.tensor(float(f"{window['GBIR_AFS2'].iloc[-1]:.9f}"), dtype=torch.float64)

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

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, collate_fn=lambda x: x)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, collate_fn=lambda x: x)

# === 8. nn.Embedding 생성 ===
num_eqp_ids = len(eqp_encoder.classes_) if eqp_encoder else 1  # EQP_ID가 없으면 1로 설정
embedding_dim = 16  # 원하는 임베딩 차원 설정
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