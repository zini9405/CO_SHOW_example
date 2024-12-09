import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
import glob
import os
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter

from einops import rearrange, reduce, repeat


# Custom Dataset for loading multiple .npy files and applying masking for -9999 values


# Transformer model definition
class FullMultiLevelTransformer(nn.Module):
    def __init__(self, input_dim, d_model=64, nhead=4, num_layers=2, dim_feedforward=128, dropout=0.1):
        super(FullMultiLevelTransformer, self).__init__()
        self.d_model = d_model

        self.feature_embedding = nn.Linear(33, d_model)
        self.feature_transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout),
            num_layers=num_layers
        )

        self.fc = nn.Linear(d_model, 1)

    def forward(self, x):
        batch_size, features = x.size()
        x = self.feature_embedding(x)
        x = rearrange(x, 'b d -> b 1 d')
        x = self.feature_transformer(x)
        x = reduce(x, 'b 1 d -> b d', 'mean')
        # print(x.shape)
        output = self.fc(x)
        # print(output.shape)
        return output


# Masked MSE Loss
def masked_mse_loss(output, target):
    return torch.mean((output - target) ** 2)


# Accuracy calculation
def calculate_accuracy(output, target, threshold=0.5):
    correct = torch.abs(output - target) <= threshold
    return correct.sum().item() / len(target)


# Train/Val split
def train_val_split(dataset, val_ratio=0.2):
    val_size = int(len(dataset) * val_ratio)
    train_size = len(dataset) - val_size
    return random_split(dataset, [train_size, val_size])


# Training loop
def train_model_with_masked_inputs(model, train_loader, val_loader, criterion, optimizer, num_epochs, device, log_dir):
    writer = SummaryWriter(log_dir)
    model.to(device)

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        total_accuracy = 0.0

        for batch_data, batch_labels in tqdm(train_loader, desc=f"Training Epoch {epoch + 1}/{num_epochs}"):
            batch_data, batch_labels = batch_data.to(device), batch_labels.to(device)

            # Forward pass with masking
            outputs = model(batch_data)
            # print(outputs.squeeze().shape, batch_labels.shape)

            # Compute loss
            loss = criterion(outputs.squeeze(), batch_labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            # Calculate accuracy
            accuracy = calculate_accuracy(outputs.squeeze(), batch_labels)
            total_accuracy += accuracy

        avg_train_loss = running_loss / len(train_loader)
        avg_train_accuracy = total_accuracy / len(train_loader)
        writer.add_scalar("Loss/Train", avg_train_loss, epoch)
        writer.add_scalar("Accuracy/Train", avg_train_accuracy, epoch)
        print(f"Epoch [{epoch + 1}/{num_epochs}], Train Loss: {avg_train_loss:.4f}, Train Accuracy: {avg_train_accuracy:.4f}")

        # Validation step
        model.eval()
        val_loss = 0.0
        val_accuracy = 0.0
        with torch.no_grad():
            for batch_data, batch_labels in val_loader:
                batch_data, batch_labels = batch_data.to(device), batch_labels.to(device)
                outputs = model(batch_data)
                loss = criterion(outputs.squeeze(), batch_labels)
                val_loss += loss.item()

                # Calculate accuracy
                accuracy = calculate_accuracy(outputs.squeeze(), batch_labels)
                val_accuracy += accuracy

        avg_val_loss = val_loss / len(val_loader)
        avg_val_accuracy = val_accuracy / len(val_loader)
        writer.add_scalar("Loss/Validation", avg_val_loss, epoch)
        writer.add_scalar("Accuracy/Validation", avg_val_accuracy, epoch)
        print(f"Epoch [{epoch + 1}/{num_epochs}], Validation Loss: {avg_val_loss:.4f}, Validation Accuracy: {avg_val_accuracy:.4f}")

    writer.close()


import pandas as pd
import os
import numpy as np
import glob
import json

import pandas as pd
from torch.utils.data import DataLoader, Dataset
import torch


# 1. RECIPE_ID와 EQP_ID_MODULE_NAME 매핑
def map_to_numeric(values):
    mapping = {val: idx for idx, val in enumerate(sorted(values))}
    return mapping

RECIPE_ID = {'CAN3_01_CA', 'CAN3_01_CB', 'CIS_CA', 'CIS_CB', 'CIS_P+_CA', 'CIS_P+_CB', 'CIS_P+_CXT5_CB', 'CIS_P+_GLX5_CA', 'CIS_P+_GLX5_CB', 'CIS_P+_HUA4_CA', 'CIS_P+_HUA4_CB', 'CIS_P+_ICR5_CB', 'CIS_P+_ONS6_CA', 'CIS_P+_ONS6_CB', 'CIS_P+_PSM4_CA', 'CIS_P+_SKH6_CA', 'CIS_P+_SKH6_CB', 'CIS_P+_SKH9_CA',
 'CIS_P+_SKH9_CB', 'CIS_P+_SMI4_CA', 'CIS_P+_UMC4_CA', 'CIS_P+_UMC4_CB', 'CIS_P_SKH6_CA', 'CIS_P_SKH6_CB', 'GF_01_CA', 'GF_01_CB', 'GF_02_CA', 'GF_02_CB', 'GF_03_CA', 'GF_03_CB', 'HUALI_01_CA', 'HUALI_01_CB',
 'INTEL10_CA', 'INTEL10_CB', 'INTEL14_CB', 'INTEL2_CA', 'INTEL2_CB', 'INTEL7_CA', 'INTEL7_CB', 'L2_CB', 'LOG_TSM1_CA', 'LOG_TSM1_CB', 'LOG_TSM3_CA', 'LOG_TSM3_CB', 'MIC_01_CA', 'MIC_01_CB', 'MXIC_01_CA', 'MXIC_01_CB', 'PSMC_02_CA', 'PSMC_02_CB', 'PSMC_FSI_CA', 'S14_CA', 'S14_CB', 'SEC_L58_CA', 'SEC_L58_CB',
 'SKH_CIS_CA', 'SKH_CIS_P+_CA', 'SKH_CIS_P+_CB', 'SL_CA', 'SL_CB', 'SMIC2_R0_CA', 'SMIC2_R0_CB', 'SMIC4_R0_CA', 'SMIC_L7_CB', 'STM_01_CA', 'STM_01_CB', 'STM_P+_CA', 'STM_P+_CB', 'TIX_R0_CA', 'TIX_R0_CB', 'TIX_R1_CA', 'TIX_R1_CB', 'TSMC2_CA', 'TSMC2_CB', 'TSMC_CA', 'TSMC_CB', 'UMC_R0_CA', 'UMC_R0_CB'}

EQP_ID_MODULE_NAME = {'CENC10A', 'CENC10B', 'CENC11A', 'CENC11B', 'CENC12A', 'CENC12B', 'CENC13A', 'CENC13B', 'CENC14A', 'CENC14B', 'CENC15A', 'CENC15B', 'CENC16A', 'CENC16B', 'CENC17A', 'CENC17B', 'CENC31A', 'CENC31B', 'CENC32A',
 'CENC32B', 'CENC33A', 'CENC33B', 'CENC34A', 'CENC34B', 'CENC35A', 'CENC35B', 'CENC36A', 'CENC36B', 'CENC41A', 'CENC41B', 'CENC42A', 'CENC42B', 'CENC43A', 'CENC43B', 'CENC44A', 'CENC44B', 'CENC45A', 'CENC45B',
 'CENC46A', 'CENC46B', 'CENC47A', 'CENC47B', 'CENC48A', 'CENC48B', 'CENC5A', 'CENC5B', 'CENC6A', 'CENC6B', 'CENC7A', 'CENC7B', 'CENC8A', 'CENC8B', 'CENC9A', 'CENC9B', 'ZCENC01A', 'ZCENC01B', 'ZCENC02A', 'ZCENC02B',
 'ZCENC03A', 'ZCENC03B', 'ZCENC04A', 'ZCENC04B'}

recipe_mapping = map_to_numeric(RECIPE_ID)
eqp_mapping = map_to_numeric(EQP_ID_MODULE_NAME)

# Load CSV
csv_file = 'grouped_datasets/CENC5A.csv'
df = pd.read_csv(csv_file)

df = df.dropna(axis=0)

# Ensure HST_REG_DTTM is sorted
df = df.sort_values("HST_REG_DTTM")

# Replace RECIPE_ID and EQP_ID_MODULE_NAME with numeric values
if "RECIPE_ID" in df.columns:
    df["RECIPE_ID"] = df["RECIPE_ID"].map(recipe_mapping)
if "EQP_ID_MODULE_NAME" in df.columns:
    df["EQP_ID_MODULE_NAME"] = df["EQP_ID_MODULE_NAME"].map(eqp_mapping)

# CSV 파일 로드 및 데이터 필터링
class CustomDataset(Dataset):
    def __init__(self, df):
        self.data = df
        self.filtered_data = self.data[self.data['STEP_NAME'] == 'DEPO']
        self.labels = self.filtered_data['SFQR_AFS2'].values
        self.features = self.filtered_data.drop(columns=['SFQR_AFS2', 'STEP_NAME', "WAF_ID", "HST_REG_DTTM", 'STEP_ID']).values

    def __len__(self):
        return len(self.filtered_data)

    def __getitem__(self, idx):
        return torch.tensor(self.features[idx], dtype=torch.float32), torch.tensor(self.labels[idx], dtype=torch.float32)


# Main
batch_size = 512
num_epochs = 100
learning_rate = 1e-3
log_dir = "logs"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

dataset = CustomDataset(df)

train_dataset, val_dataset = train_val_split(dataset, val_ratio=0.2)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

model = FullMultiLevelTransformer(input_dim=33, d_model=64, nhead=4, num_layers=6, dim_feedforward=128)
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

train_model_with_masked_inputs(
    model=model,
    train_loader=train_loader,
    val_loader=val_loader,
    criterion=masked_mse_loss,
    optimizer=optimizer,
    num_epochs=num_epochs,
    device=device,
    log_dir=log_dir,
)

이 코드 정리해주고 test할 수있게 weight 저장해서 test 하는 코드도 구현해줘
