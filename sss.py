# Train/Val Split
def train_val_split(dataset, val_ratio=0.2):
    val_size = int(len(dataset) * val_ratio)
    train_size = len(dataset) - val_size
    return random_split(dataset, [train_size, val_size])
