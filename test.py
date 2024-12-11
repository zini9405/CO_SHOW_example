from torch.utils.data import random_split
import pickle

# 예제 데이터셋 (PyTorch Dataset 사용)
class CustomDataset:
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

# 예제 데이터 (텐서로 구성)
import torch
data = [(torch.tensor([i, i+1, i+2]), torch.tensor(i % 2)) for i in range(100)]
dataset = CustomDataset(data)

# Train/Validation 비율 설정
train_size = int(len(dataset) * 0.8)
val_size = len(dataset) - train_size

# Train/Validation 분리
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

# Pickle 파일로 저장
with open("train_dataset.pkl", "wb") as train_file:
    pickle.dump(train_dataset, train_file)

with open("val_dataset.pkl", "wb") as val_file:
    pickle.dump(val_dataset, val_file)

print("Train/Validation 데이터셋이 Pickle 파일로 저장되었습니다.")


# Pickle 파일 불러오기
with open("train_dataset.pkl", "rb") as train_file:
    loaded_train_dataset = pickle.load(train_file)

with open("val_dataset.pkl", "rb") as val_file:
    loaded_val_dataset = pickle.load(val_file)

print(f"Train Dataset Size: {len(loaded_train_dataset)}")
print(f"Validation Dataset Size: {len(loaded_val_dataset)}")

