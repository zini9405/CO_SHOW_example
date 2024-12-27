import torch
import torch.nn as nn
import torch.nn.functional as F

class AdaptiveHierarchicalModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, num_steps, num_heads):
        """
        Initialize the model.

        Args:
        - input_dim: Number of input features for each step (e.g., 33).
        - hidden_dim: Number of hidden dimensions for embeddings.
        - output_dim: Output dimension (e.g., 1 for regression).
        - num_steps: Number of time steps (e.g., 12).
        - num_heads: Number of attention heads.
        """
        super(AdaptiveHierarchicalModel, self).__init__()
        
        # Parameters
        self.num_steps = num_steps
        self.hidden_dim = hidden_dim
        self.num_heads = num_heads
        
        # Latent Graph Construction (Multi-Head Attention)
        self.mha = nn.MultiheadAttention(embed_dim=hidden_dim, num_heads=num_heads, batch_first=True)
        self.input_projection = nn.Linear(input_dim, hidden_dim)
        
        # GNN Layers for local relationships
        self.gnn_layers = nn.ModuleList([nn.Linear(hidden_dim, hidden_dim) for _ in range(3)])
        
        # Local Attention (for step importance within subgraphs)
        self.local_attention = nn.MultiheadAttention(embed_dim=hidden_dim, num_heads=num_heads, batch_first=True)
        
        # Global Attention (for subgraph relationships)
        self.global_attention = nn.MultiheadAttention(embed_dim=hidden_dim, num_heads=num_heads, batch_first=True)
        
        # Step Selection Attention
        self.step_attention = nn.MultiheadAttention(embed_dim=hidden_dim, num_heads=num_heads, batch_first=True)
        
        # Regression Layer
        self.regressor = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),  # Combine local & global
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )
    
    def forward(self, X):
        """
        Forward pass through the model.

        Args:
        - X: Input tensor of shape (batch_size, num_steps, input_dim).
        
        Returns:
        - y: Predicted output of shape (batch_size, output_dim).
        - step_scores: Attention scores for each step (batch_size, num_steps).
        """
        # Step 1: Latent Graph Construction
        H_projected = self.input_projection(X)  # Project input to hidden_dim
        H_latent, latent_scores = self.compute_latent_graph(H_projected)  # Apply Multi-Head Attention
        
        # Step 2: Local Relationship Learning (GNN + Attention)
        H_local = self.local_relationships(H_latent)  # Shape: (batch_size, num_steps, hidden_dim)
        
        # Step 3: Global Relationship Learning (Subgraph Aggregation)
        H_global = self.global_relationships(H_local)  # Shape: (batch_size, hidden_dim)
        
        # Step 4: Step Selection
        H_selected, step_scores = self.step_selection(H_local, H_global)  # Select important steps
        
        # Step 5: Regression
        y = self.regressor(H_selected)  # Predict the output
        
        return y, step_scores

    def compute_latent_graph(self, X):
        """
        Compute latent graph using Multi-Head Attention.

        Args:
        - X: Input tensor of shape (batch_size, num_steps, hidden_dim).

        Returns:
        - H_latent: Latent graph embeddings (batch_size, num_steps, hidden_dim).
        - latent_scores: Attention scores (batch_size, num_heads, num_steps, num_steps).
        """
        H_latent, latent_scores = self.mha(X, X, X, need_weights=True)
        return H_latent, latent_scores

    def local_relationships(self, H):
        """
        Learn local relationships using GNN layers.

        Args:
        - H: Input embeddings of shape (batch_size, num_steps, hidden_dim).

        Returns:
        - H_local: Hidden embeddings for each step (batch_size, num_steps, hidden_dim).
        """
        for gnn_layer in self.gnn_layers:
            H = F.relu(gnn_layer(H))  # GNN propagation
        return H

    def global_relationships(self, H_local):
        """
        Learn global relationships using global attention.

        Args:
        - H_local: Hidden embeddings for each step (batch_size, num_steps, hidden_dim).

        Returns:
        - H_global: Aggregated global embedding (batch_size, hidden_dim).
        """
        H_global, _ = self.global_attention(H_local, H_local, H_local)
        return torch.mean(H_global, dim=1)  # Aggregate over all steps

    def step_selection(self, H_local, H_global):
        """
        Select important steps using step-level Multi-Head Attention and combine with global information.

        Args:
        - H_local: Hidden embeddings for each step (batch_size, num_steps, hidden_dim).
        - H_global: Global embedding for the entire sequence (batch_size, hidden_dim).

        Returns:
        - H_selected: Combined embedding of important steps and global information (batch_size, hidden_dim * 2).
        - step_scores: Attention scores for each step (batch_size, num_steps).
        """
        # Step-level attention
        H_step, step_scores = self.step_attention(H_local, H_local, H_local, need_weights=True)
        
        # Combine selected steps with global embedding
        H_selected = torch.cat([H_global, torch.sum(step_scores.unsqueeze(-1) * H_local, dim=1)], dim=-1)
        return H_selected, step_scores
        
        
        # 모델 초기화
input_dim = 33  # 33개의 변수
hidden_dim = 64  # 히든 레이어 크기
output_dim = 1  # 예측값 (회귀)
num_steps = 12  # 12개의 step
num_heads = 4   # Multi-Head Attention의 head 수
model = AdaptiveHierarchicalModel(input_dim, hidden_dim, output_dim, num_steps, num_heads)

# 가상 데이터 생성
batch_size = 8
X = torch.rand(batch_size, num_steps, input_dim)  # 입력 데이터

# 모델 실행
y, step_scores = model(X)

# 결과 출력
print("Predicted Output (y):", y)  # (batch_size, output_dim)
print("Step Importance Scores:", step_scores)  # (batch_size, num_steps)
        