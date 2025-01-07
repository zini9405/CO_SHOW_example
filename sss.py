import torch
import torch.nn as nn

class SelfAttention(nn.Module):
    def __init__(self, input_dim, num_heads):
        super(SelfAttention, self).__init__()
        self.multihead_attn = nn.MultiheadAttention(embed_dim=input_dim, num_heads=num_heads)
    
    def forward(self, x):
        # x: (seq_len, batch_size, input_dim)
        attn_output, attn_weights = self.multihead_attn(x, x, x)
        # attn_weights: (batch_size, num_heads, seq_len, seq_len)
        return attn_weights

# Example parameters
input_dim = 33  # Number of features
seq_len = 33    # Sequence length (e.g., each variable treated as a sequence position)
batch_size = 1  # Single batch for simplicity
num_heads = 1   # Number of attention heads

# Generate random input tensor
x = torch.rand(seq_len, batch_size, input_dim)

# Define and apply Self-Attention
self_attention = SelfAttention(input_dim=input_dim, num_heads=num_heads)
attn_weights = self_attention(x)  # Shape: (batch_size, num_heads, seq_len, seq_len)

# Extract attention scores for the first head
attn_scores = attn_weights[0, 0]  # Shape: (seq_len, seq_len)

# Calculate average attention score for each variable
avg_scores = attn_scores.mean(dim=0).detach().numpy()

# Sort variables by attention scores in descending order
sorted_indices = avg_scores.argsort()[::-1]
sorted_scores = avg_scores[sorted_indices]

# Print results
print("Variables sorted by attention scores:")
for i, idx in enumerate(sorted_indices):
    print(f"Rank {i+1}: Variable {idx}, Score: {sorted_scores[i]}")