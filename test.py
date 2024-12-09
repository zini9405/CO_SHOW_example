import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import glob
import os


# Custom Dataset for loading multiple .npy files and applying masking for -9999 values
class MaskedWaferDataset(Dataset):
    def __init__(self, data_dir, window_size=3, mask_value=-9999):
        """
        Args:
            data_dir: Directory containing .npy files (both data and labels).
            window_size: Number of overlapping sequences to include in each sample.
            mask_value: Value to be masked in the dataset.
        """
        self.data_files = sorted(glob.glob(os.path.join(data_dir, "*_data.npy")))
        self.label_files = sorted(glob.glob(os.path.join(data_dir, "*_labels.npy")))
        self.window_size = window_size
        self.mask_value = mask_value

        # Load all data and labels into memory
        self.data = []
        self.labels = []

        for data_file, label_file in zip(self.data_files, self.label_files):
            data = np.load(data_file)  # Shape: [Num Sequences, Steps, Features]
            labels = np.load(label_file)  # Shape: [Num Sequences]
            self.data.append(data)
            self.labels.append(labels)

        # Concatenate all data and labels
        self.data = np.concatenate(self.data, axis=0)
        self.labels = np.concatenate(self.labels, axis=0)

    def __len__(self):
        # Ensure we have enough sequences for the window size
        return len(self.data) - self.window_size + 1

    def __getitem__(self, idx):
        # Extract overlapping window of sequences
        data_window = self.data[idx:idx + self.window_size]  # Shape: [Window Size, Steps, Features]
        label_window = self.labels[idx:idx + self.window_size]  # Shape: [Window Size]

        # Apply masking
        mask = data_window != self.mask_value  # Create mask for valid values
        masked_data_window = data_window * mask  # Zero out invalid values

        # Use the label of the last sequence in the window as the target
        return (
            torch.tensor(masked_data_window, dtype=torch.float32),
            torch.tensor(label_window[-1], dtype=torch.float32),
            torch.tensor(mask, dtype=torch.bool),  # Include the mask for further processing if needed
        )


# Example usage with a directory containing .npy files
data_dir = "processed"  # Directory with *_data.npy and *_labels.npy
window_size = 3
batch_size = 8

# Create Dataset and DataLoader
dataset = MaskedWaferDataset(data_dir, window_size=window_size, mask_value=-9999)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Test DataLoader
for batch_data, batch_labels, batch_masks in dataloader:
    print("Batch data shape:", batch_data.shape)  # [Batch Size, Window Size, Steps, Features]
    print("Batch labels shape:", batch_labels.shape)  # [Batch Size]
    print("Batch masks shape:", batch_masks.shape)  # [Batch Size, Window Size, Steps, Features]
    break  # Print one batch and stop

print(f"DataLoader created successfully with {len(dataset)} samples.")