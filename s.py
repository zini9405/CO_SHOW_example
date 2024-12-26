from torch.utils.data import Dataset
import pandas as pd
from sklearn.preprocessing import StandardScaler, QuantileTransformer, MinMaxScaler

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import numpy as np
from einops import rearrange, repeat
import random
from pathlib import Path 
from sklearn.metrics import r2_score
from sklearn.preprocessing import QuantileTransformer
import numpy as np



def set_seed(seed: int):
    """
    학습의 재현 가능성을 위해 시드를 고정합니다.
    Args:
        seed (int): 고정할 시드 값
    """
    random.seed(seed)                      # Python의 random 모듈 시드 고정
    np.random.seed(seed)                   # NumPy 시드 고정
    torch.manual_seed(seed)                # PyTorch CPU 시드 고정
    torch.cuda.manual_seed(seed)           # PyTorch CUDA 시드 고정
    torch.cuda.manual_seed_all(seed)       # 모든 GPU의 CUDA 시드 고정 (멀티 GPU 사용 시)
    torch.backends.cudnn.deterministic = True  # CuDNN을 deterministic 모드로 설정
    torch.backends.cudnn.benchmark = False


class MyDataset(Dataset):
    def __init__(self, file, is_train=True, scaler=None):
        df = pd.read_csv(file)
        df = df[['MAIN_RUNTIME', 'DD_USE_NUM', 'SLURRY_USE_NUM', 'PAD_COUNT', 'CARRIER_MTL_USE_NUM', 'GBIR']]
        df = df[df['GBIR']<1.0]

        num_train = int(len(df) * 0.8)
        if is_train:
            data = df.iloc[:num_train]
        else:
            data = df.iloc[num_train:]

        self.X = data[['MAIN_RUNTIME', 'DD_USE_NUM', 'SLURRY_USE_NUM', 'PAD_COUNT', 'CARRIER_MTL_USE_NUM']].values
        self.Y = data['GBIR'].values

        # self.scaler = scaler
        # if scaler: 
        #     if is_train:
        #         self.X = scaler.fit_transform(self.X)
        #     else:
        #         self.X = scaler.transform(self.X)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, index):
        x = self.X[index]
        y = self.Y[index]

        x = torch.tensor(x, dtype=torch.float32)
        y = torch.tensor(y, dtype=torch.float32) 
        
        return x, y


import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import numpy as np
from einops import rearrange, repeat, reduce
import random
from pathlib import Path 
from sklearn.metrics import r2_score
from sklearn.preprocessing import QuantileTransformer




set_seed(1234)
scaler = StandardScaler()
trainset = MyDataset('transformed_df.csv')
testset = MyDataset('transformed_df.csv', is_train=False)

class FullMultiLevelTransformer(nn.Module):
    def __init__(self, input_dim, d_model=64, nhead=4, num_layers=2, dim_feedforward=128, dropout=0.1):
        super(FullMultiLevelTransformer, self).__init__()
        self.d_model = d_model

        self.feature_embedding = nn.Linear(input_dim, d_model)
        self.feature_transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, batch_first=True, dropout=dropout),
            num_layers=num_layers
        )
        self.fc = nn.Linear(d_model, 1)

    def forward(self, x):
        # print(x.shape)
        x = self.feature_embedding(x)
        x = rearrange(x, 'b d -> b 1 d')
        x = self.feature_transformer(x)
        x = reduce(x, 'b 1 d -> b d', 'mean')
        return self.fc(x)


# 하이퍼파라미터 및 데이터셋 준비
seq_len = 40
input_dim = 22  # 예시 데이터 컬럼 수
batch_size = 256
epochs = 2000
learning_rate = 1e-5
set_seed(1234)



dataloader = DataLoader(trainset, batch_size=batch_size, shuffle=True)

test_dataloader = DataLoader(testset, batch_size=batch_size, shuffle=False)



# print(dataset[0][0].shape)
# 모델 초기화
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = FullMultiLevelTransformer(input_dim=5, d_model=256, nhead=4, num_layers=4, dim_feedforward=512)

model.to(device)

# 손실 함수 및 옵티마이저
criterion = nn.HuberLoss()
optimizer = optim.AdamW(model.parameters(), lr=learning_rate)
scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(optimizer, T_0=50)
                                                     

# 학습 루프
model.train()
for epoch in range(epochs):
    total_loss = 0
    model.train()
    for idx, batch in enumerate(dataloader):

        inputs, targets = batch

        inputs, targets = inputs.to(device), targets.to(device)
        # print(targets)
        # print(torch.isnan(inputs).sum())
        # print(torch.isnan(targets).sum())
        optimizer.zero_grad()
        outputs = model(inputs).squeeze()
        
        # print(outputs.shape, targets.shape)
        loss = criterion(outputs, targets)
        # print(loss.item())
        loss.backward()
        optimizer.step()
        scheduler.step(epoch + idx / len(dataloader))
        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(dataloader):.8f}")
    if epoch % 10 == 0  or epoch == (epochs - 1):
        model.eval()
        total_loss = 0
        target_list = []
        pred_list = []
        with torch.no_grad():
            for batch in test_dataloader:
                inputs, targets = batch
                inputs, targets = inputs.to(device), targets.to(device)

                outputs = model(inputs).squeeze()
                pred_list.extend(outputs.cpu().detach().tolist())
                target_list.extend(targets.cpu().detach().tolist())
                loss = criterion(outputs, targets)
                total_loss += loss.item()

        print(f"Epoch {epoch+1}/{epochs} Val Loss: {total_loss/len(test_dataloader):.4f}")
        print(f'r2 score: {r2_score(target_list, pred_list)}')

print("Training Complete.")
