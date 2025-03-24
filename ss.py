from torch.utils.data import Subset

indices = list(range(len(dataset)))
train_indices = indices[:train_size]
val_indices = indices[train_size:]

train_dataset = Subset(dataset, train_indices)
val_dataset = Subset(dataset, val_indices)