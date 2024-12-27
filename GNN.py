import torch
import torch.nn as nn
import torch.nn.functional as F

class AdaptiveHierarchicalModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, num_steps):
        """
        Initialize the model.

        Args:
        - input_dim: Number of input features for each step (e.g., 33).
        - hidden_dim: Number of hidden dimensions for embeddings.
        - output_dim: Output dimension (e.g., 1 for regression).
        - num_steps: Number of time steps (e.g., 12).
        """
        super(AdaptiveHierarchicalModel, self).__init__()
        
        # Parameters
        self.num_steps = num_steps
        
        # Latent Graph Construction
        self.query_layer = nn.Linear(input_dim, hidden_dim)  # For Q
        self.key_layer = nn.Linear(input_dim, hidden_dim)    # For K
        
        # GNN Layers for local relationships
        self.gnn_layers = nn.ModuleList([nn.Linear(hidden_dim, hidden_dim) for _ in range(3)])
        
        # Local Attention (for step importance within subgraphs)
        self.local_attention = nn.Linear(hidden_dim, 1)
        
        # Global Attention (for subgraph relationships)
        self.global_attention = nn.Linear(hidden_dim, 1)
        
        # Step Selection Attention
        self.step_attention = nn.Linear(hidden_dim, 1)
        
        # Regression Layer
        self.regressor = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
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
        S = self.compute_similarity(X)  # Graph adjacency matrix (batch_size, num_steps, num_steps)
        sparse_S = self.apply_sparsity(S)  # Apply sparsity to reduce weak relationships
        
        # Step 2: Local Relationship Learning (GNN + Attention)
        H_local = self.local_relationships(X, sparse_S)  # Shape: (batch_size, num_steps, hidden_dim)
        
        # Step 3: Global Relationship Learning (Subgraph Aggregation)
        H_global = self.global_relationships(H_local)  # Shape: (batch_size, hidden_dim)
        
        # Step 4: Step Selection
        step_scores = torch.softmax(self.step_attention(H_local), dim=1)  # Step importance scores
        H_selected = torch.sum(step_scores * H_local, dim=1)  # Weighted sum of steps
        
        # Step 5: Regression
        y = self.regressor(H_selected)  # Predict the output
        
        return y, step_scores

    def compute_similarity(self, X):
        """
        Compute similarity matrix S for step relationships.

        Args:
        - X: Input tensor of shape (batch_size, num_steps, input_dim).

        Returns:
        - S: Similarity matrix of shape (batch_size, num_steps, num_steps).
        """
        Q = self.query_layer(X)  # Query vector (batch_size, num_steps, hidden_dim)
        K = self.key_layer(X)    # Key vector (batch_size, num_steps, hidden_dim)
        S = torch.matmul(Q, K.transpose(-2, -1)) / torch.sqrt(torch.tensor(Q.size(-1), dtype=torch.float32))  # Scaled dot-product
        return torch.softmax(S, dim=-1)

    def apply_sparsity(self, S, threshold=0.1):
        """
        Apply sparsity to the similarity matrix.

        Args:
        - S: Similarity matrix of shape (batch_size, num_steps, num_steps).
        - threshold: Minimum value to keep a connection.

        Returns:
        - sparse_S: Sparse similarity matrix of the same shape.
        """
        return (S > threshold).float() * S  # Retain values above the threshold

    def local_relationships(self, X, S):
        """
        Learn local relationships using GNN layers.

        Args:
        - X: Input tensor of shape (batch_size, num_steps, input_dim).
        - S: Sparse similarity matrix (batch_size, num_steps, num_steps).

        Returns:
        - H_local: Hidden embeddings for each step (batch_size, num_steps, hidden_dim).
        """
        H = X
        for gnn_layer in self.gnn_layers:
            H = F.relu(gnn_layer(torch.matmul(S, H)))  # GNN propagation
        return H

    def global_relationships(self, H_local):
        """
        Learn global relationships using global attention.

        Args:
        - H_local: Hidden embeddings for each step (batch_size, num_steps, hidden_dim).

        Returns:
        - H_global: Aggregated global embedding (batch_size, hidden_dim).
        """
        scores = torch.softmax(self.global_attention(H_local), dim=1)  # Subgraph importance scores
        H_global = torch.sum(scores * H_local, dim=1)  # Weighted sum of subgraph embeddings
        return H_global
        
        
        
        # 모델 초기화
input_dim = 33  # 33개의 변수
hidden_dim = 64  # 히든 레이어 크기
output_dim = 1  # 예측값 (회귀)
num_steps = 12  # 12개의 step
model = AdaptiveHierarchicalModel(input_dim, hidden_dim, output_dim, num_steps)

# 가상 데이터 생성
batch_size = 8
X = torch.rand(batch_size, num_steps, input_dim)  # 입력 데이터

# 모델 실행
y, step_scores = model(X)

# 결과 출력
print("Predicted Output (y):", y)  # (batch_size, output_dim)
print("Step Importance Scores:", step_scores)  # (batch_size, num_steps)
        
