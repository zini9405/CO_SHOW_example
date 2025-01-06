import os
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter
from einops import rearrange, reduce
from sklearn.preprocessing import QuantileTransformer
import numpy as np
import random

# 1. 시드 고정 함수
def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

# 2. 데이터셋 정의
class CustomDataset(Dataset):
    def __init__(self, df, eqp_mapping):
        self.data = df
        self.eqp_mapping = eqp_mapping

        # Labels
        self.labels = self.data['ZDDFRONTMEAN_01_AFS2'].values
        self.quantile_transformer = QuantileTransformer(output_distribution='normal', random_state=42)
        self.labels = self.quantile_transformer.fit_transform(self.labels.reshape(-1, 1)).flatten()

        # Features
        self.features = self.data.drop(columns=['WAF_ID', 'HST_REG_DTTM', 'SFQR_AFS2', 'ESFQR2_MAX_AFS2', 'ZDDFRONTMEAN_01_AFS2', 'ESFQD_ZONE1MEAN_AFS2', 'ESFQD_ZONE1MAX_AFS2',
                                                'ESFQD2_ZONE1MEAN_AFS2', 'ESFQD2_ZONE1MAX_AFS2', 'EQP_ID_MODULE_NAME']).values

        # EQP_ID_MODULE_NAME 인코딩
        self.eqp_ids = self.data['EQP_ID_MODULE_NAME'].map(self.eqp_mapping).values

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        features = torch.tensor(self.features[idx], dtype=torch.float32)
        label = torch.tensor(self.labels[idx], dtype=torch.float32)
        eqp_id = torch.tensor(self.eqp_ids[idx], dtype=torch.long)  # 임베딩에 사용될 ID
        return features, eqp_id, label

# 3. Transformer 모델 정의
class FullMultiLevelTransformer(nn.Module):
    def __init__(self, input_dim, num_eqp_ids, eqp_embed_dim=16, d_model=64, nhead=4, num_layers=2, dim_feedforward=128, dropout=0.1):
        super(FullMultiLevelTransformer, self).__init__()
        self.d_model = d_model

        # EQP_ID_MODULE_NAME 임베딩
        self.eqp_embedding = nn.Embedding(num_eqp_ids, eqp_embed_dim)
        
        # Feature 임베딩
        self.feature_embedding = nn.Linear(input_dim + eqp_embed_dim, d_model)
        
        # Transformer Encoder
        self.feature_transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout),
            num_layers=num_layers
        )
        
        # 최종 예측 레이어
        self.fc = nn.Linear(d_model, 1)

        # Attention Map 저장을 위한 변수
        self.attention_map = None

    def forward(self, x, eqp_ids):
        # EQP_ID_MODULE_NAME 임베딩
        eqp_embed = self.eqp_embedding(eqp_ids)
        eqp_embed = rearrange(eqp_embed, 'b d -> b 1 d')  # 배치 차원 정렬
        
        # Feature + EQP_ID 통합
        x = torch.cat((x, eqp_embed.squeeze(1)), dim=1)  # Feature에 임베딩 추가
        x = self.feature_embedding(x)

        # Transformer 통과
        x = rearrange(x, 'b d -> b 1 d')
        x = self.feature_transformer(x)
        self.attention_map = x.clone().detach()  # Attention Map 저장
        x = reduce(x, 'b 1 d -> b d', 'mean')

        # 최종 출력
        return self.fc(x)

# 4. Train/Val Split
def train_val_split(dataset, val_ratio=0.2):
    val_size = int(len(dataset) * val_ratio)
    train_size = len(dataset) - val_size
    return random_split(dataset, [train_size, val_size])

# 5. 학습 루프
def train_model_inputs(model, train_loader, val_loader, criterion, optimizer, num_epochs, device, log_dir, save_path):
    writer = SummaryWriter(log_dir)
    model.to(device)

    best_val_loss = float('inf')  # Best Validation Loss 초기화

    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0

        for features, eqp_ids, labels in tqdm(train_loader, desc=f"Training Epoch {epoch + 1}/{num_epochs}"):
            features, eqp_ids, labels = features.to(device), eqp_ids.to(device), labels.to(device)

            outputs = model(features, eqp_ids)

            loss = criterion(outputs.squeeze(), labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        avg_train_loss = train_loss / len(train_loader)
        writer.add_scalar("Loss/Train", avg_train_loss, epoch)

        # Validation
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for features, eqp_ids, labels in tqdm(val_loader, desc=f"Validation Epoch {epoch + 1}/{num_epochs}"):
                features, eqp_ids, labels = features.to(device), eqp_ids.to(device), labels.to(device)
                outputs = model(features, eqp_ids)
                loss = criterion(outputs.squeeze(), labels)
                val_loss += loss.item()

        avg_val_loss = val_loss / len(val_loader)
        writer.add_scalar("Loss/Validation", avg_val_loss, epoch)

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), save_path)
            print(f"Best model saved with validation loss: {best_val_loss:.4f}")

    writer.close()

# 6. Main 실행
def main():
    RECIPE_ID = {...}  # 생략
    EQP_ID_MODULE_NAME = {...}  # 생략

    recipe_mapping = map_to_numeric(RECIPE_ID)
    eqp_mapping = map_to_numeric(EQP_ID_MODULE_NAME)

    # Load CSV
    df = pd.read_csv('all_minmax.csv')
    df = df.dropna(subset=['ZDDFRONTMEAN_01_AFS2', 'ZDDFRONTMEAN_01_AFS2_SUB'])
    df.fillna(0, inplace=True)

    # Replace IDs with numeric mappings
    df["RECIPE_ID"] = df["RECIPE_ID"].map(recipe_mapping)
    df["EQP_ID_MODULE_NAME"] = df["EQP_ID_MODULE_NAME"].map(eqp_mapping)

    dataset = CustomDataset(df, eqp_mapping)

    train_dataset, val_dataset = train_val_split(dataset)
    train_loader = DataLoader(train_dataset, batch_size=512, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=512, shuffle=False)

    num_eqp_ids = len(eqp_mapping)
    model = FullMultiLevelTransformer(input_dim=32, num_eqp_ids=num_eqp_ids, eqp_embed_dim=16, d_model=256, num_layers=4, dim_feedforward=512)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    criterion = nn.HuberLoss(delta=1.0)
    save_path = "model_weights_ZDD.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_model_inputs(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        criterion=criterion,
        optimizer=optimizer,
        num_epochs=100,
        device=device,
        log_dir="logs",
        save_path=save_path
    )

if __name__ == "__main__":
    set_seed(42)
    main()