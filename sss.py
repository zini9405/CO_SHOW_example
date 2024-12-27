import torch
import torch.nn as nn
import torch.nn.functional as F

class DynamicGraphModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, num_steps, num_heads, num_subgraphs):
        """
        Initialize the model.

        Args:
        - input_dim: Number of input features for each step (e.g., 33).
        - hidden_dim: Number of hidden dimensions for embeddings.
        - output_dim: Output dimension (e.g., 1 for regression).
        - num_steps: Number of time steps (e.g., 12).
        - num_heads: Number of attention heads.
        - num_subgraphs: Number of dynamically constructed subgraphs.
        """
        super(DynamicGraphModel, self).__init__()
        
        # Parameters
        self.num_steps = num_steps
        self.num_subgraphs = num_subgraphs
        
        # Latent Graph Construction
        self.query_layer = nn.Linear(input_dim, hidden_dim)
        self.key_layer = nn.Linear(input_dim, hidden_dim)
        self.value_layer = nn.Linear(input_dim, hidden_dim)
        
        # Local Graph Learning (per subgraph)
        self.local_gnn = nn.ModuleList([nn.Linear(hidden_dim, hidden_dim) for _ in range(3)])
        
        # Global Graph Learning
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
        S = self.compute_similarity(X)  # Graph adjacency matrix (batch_size, num_steps, num_steps)
        subgraphs = self.create_subgraphs(S)  # Dynamically create subgraphs
        
        # Step 2: Local Graph Learning
        H_local = self.local_graph_learning(X, subgraphs)  # Local embeddings
        
        # Step 3: Global Graph Learning
        H_global = self.global_graph_learning(H_local)  # Global embedding
        
        # Step 4: Step Selection
        H_selected, step_scores = self.step_selection(H_local, H_global)  # Select important steps
        
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
        Q = self.query_layer(X)  # Query vector
        K = self.key_layer(X)    # Key vector
        S = torch.matmul(Q, K.transpose(-2, -1)) / torch.sqrt(torch.tensor(Q.size(-1), dtype=torch.float32))  # Scaled dot-product
        return torch.softmax(S, dim=-1)

    def create_subgraphs(self, S):
        """
        Dynamically create subgraphs based on the similarity matrix.

        Args:
        - S: Similarity matrix of shape (batch_size, num_steps, num_steps).

        Returns:
        - subgraphs: List of subgraph masks (batch_size, num_subgraphs, num_steps, num_steps).
        """
        batch_size, num_steps, _ = S.size()
        subgraphs = []
        
        for _ in range(self.num_subgraphs):
            mask = torch.zeros_like(S)
            for b in range(batch_size):
                # Select top-k steps based on similarity scores
                top_indices = torch.topk(S[b].sum(dim=0), k=self.num_steps // self.num_subgraphs).indices
                for idx in top_indices:
                    mask[b, idx, idx] = 1
            subgraphs.append(mask)
        
        return subgraphs

    def local_graph_learning(self, X, subgraphs):
        """
        Learn local relationships within dynamically constructed subgraphs.

        Args:
        - X: Input tensor of shape (batch_size, num_steps, input_dim).
        - subgraphs: List of subgraph masks (batch_size, num_subgraphs, num_steps, num_steps).

        Returns:
        - H_local: Local embeddings for each step (batch_size, num_steps, hidden_dim).
        """
        H = self.value_layer(X)  # Project input to hidden_dim
        for gnn_layer in self.local_gnn:
            H_new = torch.zeros_like(H)
            for mask in subgraphs:
                # Apply the subgraph mask to aggregate local information
                H_new += torch.relu(gnn_layer(torch.matmul(mask, H)))
            H = H_new / len(subgraphs)  # Normalize by the number of subgraphs
        return H

    def global_graph_learning(self, H_local):
        """
        Learn global relationships using global attention.

        Args:
        - H_local: Local embeddings of shape (batch_size, num_steps, hidden_dim).

        Returns:
        - H_global: Aggregated global embedding (batch_size, hidden_dim).
        """
        H_global, _ = self.global_attention(H_local, H_local, H_local)
        return torch.mean(H_global, dim=1)  # Aggregate over all steps

    def step_selection(self, H_local, H_global):
        """
        Select important steps using step-level Multi-Head Attention.

        Args:
        - H_local: Local embeddings for each step (batch_size, num_steps, hidden_dim).
        - H_global: Global embedding for the entire sequence (batch_size, hidden_dim).

        Returns:
        - H_selected: Combined embedding of important steps and global information (batch_size, hidden_dim * 2).
        - step_scores: Attention scores for each step (batch_size, num_steps).
        """
        H_step, step_scores = self.step_attention(H_local, H_local, H_local, need_weights=True)
        H_selected = torch.cat([H_global, torch.sum(step_scores.unsqueeze(-1) * H_local, dim=1)], dim=-1)
        return H_selected, step_scores
        
        
        
        # 모델 초기화
input_dim = 33  # 33개의 변수
hidden_dim = 64  # 히든 레이어 크기
output_dim = 1  # 예측값 (회귀)
num_steps = 12  # 12개의 step
num_heads = 4   # Multi-Head Attention의 head 수
num_subgraphs = 3  # 서브그래프 개수
model = DynamicGraphModel(input_dim, hidden_dim, output_dim, num_steps, num_heads, num_subgraphs)

# 가상 데이터 생성
batch_size = 8
X = torch.rand(batch_size, num_steps, input_dim)  # 입력 데이터

# 모델 실행
y, step_scores = model(X)

# 결과 출력
print("Predicted Output (y):", y)  # (batch_size, output_dim)
print("Step Importance Scores:", step_scores)  # (batch_size, num_steps)