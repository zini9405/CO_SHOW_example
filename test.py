from torch.utils.data import Subset

# 전체 데이터 길이
n_total = len(dataset)

# Train/Validation 분리 비율 설정 (예: Train 80%, Validation 20%)
train_ratio = 0.8
split_idx = int(n_total * train_ratio)

# 인덱스 생성 (섞지 않음)
train_indices = range(0, split_idx)
val_indices = range(split_idx, n_total)

# Subset으로 Train/Validation 데이터셋 생성
train_dataset = Subset(dataset, train_indices)
val_dataset = Subset(dataset, val_indices)

print(f"Train dataset size: {len(train_dataset)}")
print(f"Validation dataset size: {len(val_dataset)}")