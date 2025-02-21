def train_val_split_sequential(dataset, val_ratio=0.2):
    val_size = int(len(dataset) * val_ratio)
    train_size = len(dataset) - val_size
    
    train_dataset = dataset[:train_size]  # 앞부분을 train으로
    val_dataset = dataset[train_size:]  # 뒷부분을 val로
    
    return train_dataset, val_dataset