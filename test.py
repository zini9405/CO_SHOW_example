import torch
from torch.utils.data import random_split

# 데이터셋 예제 (리스트 형식)
data = list(range(100))  # [0, 1, 2, ..., 99]

# 분리 비율 설정
train_size = int(0.8 * len(data))  # 80%는 Train
val_size = len(data) - train_size  # 20%는 Validation

# Generator 생성 (순서를 유지하도록 seed 고정)
generator = torch.Generator()
generator.manual_seed(42)  # 시드 고정으로 순서 재현 가능

# 데이터 섞지 않도록 Generator 사용
train_data, val_data = random_split(data, [train_size, val_size], generator=generator)

# Train과 Validation 확인
print("Train Data:", list(train_data))
print("Validation Data:", list(val_data))



# Train/Validation 크기 계산
train_size = int(0.8 * len(data))
val_size = len(data) - train_size

# 순차적 데이터 분리
train_data = data[:train_size]
val_data = data[train_size:]

print("Train Data:", train_data)
print("Validation Data:", val_data)
