import pandas as pd
from torch.utils.data import DataLoader, Dataset
import torch

# CSV 파일 로드 및 데이터 필터링
class CustomDataset(Dataset):
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)
        self.filtered_data = self.data[self.data['step_name'] == 'Depo']
        self.labels = self.filtered_data['sfqr_afs2'].values
        self.features = self.filtered_data.drop(columns=['sfqr_afs2', 'step_name']).values

    def __len__(self):
        return len(self.filtered_data)

    def __getitem__(self, idx):
        return torch.tensor(self.features[idx], dtype=torch.float32), torch.tensor(self.labels[idx], dtype=torch.float32)

# 데이터셋과 DataLoader 생성
def create_dataloader(csv_file, batch_size):
    dataset = CustomDataset(csv_file)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    return dataloader