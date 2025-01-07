import torch
import torch.nn as nn
import torch.nn.functional as F


# Custom Multihead Self-Attention Layer
class CustomMultiheadAttention(nn.Module):
    def __init__(self, d_model, nhead):
        super(CustomMultiheadAttention, self).__init__()
        self.d_model = d_model
        self.nhead = nhead
        self.head_dim = d_model // nhead

        assert d_model % nhead == 0, "d_model must be divisible by nhead"

        self.query = nn.Linear(d_model, d_model)
        self.key = nn.Linear(d_model, d_model)
        self.value = nn.Linear(d_model, d_model)
        self.out = nn.Linear(d_model, d_model)

    def forward(self, x):
        batch_size, seq_len, d_model = x.size()

        # Linear projections
        Q = self.query(x)  # (batch_size, seq_len, d_model)
        K = self.key(x)    # (batch_size, seq_len, d_model)
        V = self.value(x)  # (batch_size, seq_len, d_model)

        # Reshape for multihead attention
        Q = Q.view(batch_size, seq_len, self.nhead, self.head_dim).transpose(1, 2)  # (batch_size, nhead, seq_len, head_dim)
        K = K.view(batch_size, seq_len, self.nhead, self.head_dim).transpose(1, 2)  # (batch_size, nhead, seq_len, head_dim)
        V = V.view(batch_size, seq_len, self.nhead, self.head_dim).transpose(1, 2)  # (batch_size, nhead, seq_len, head_dim)

        # Scaled dot-product attention
        attn_scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.head_dim ** 0.5)  # (batch_size, nhead, seq_len, seq_len)
        attn_weights = F.softmax(attn_scores, dim=-1)  # (batch_size, nhead, seq_len, seq_len)

        # Weighted sum of values
        attn_output = torch.matmul(attn_weights, V)  # (batch_size, nhead, seq_len, head_dim)

        # Combine heads
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, seq_len, d_model)  # (batch_size, seq_len, d_model)

        # Final linear projection
        output = self.out(attn_output)  # (batch_size, seq_len, d_model)

        return output, attn_weights  # Return attention weights for analysis


# Custom Transformer Encoder Layer
class CustomTransformerEncoderLayer(nn.Module):
    def __init__(self, d_model, nhead, dim_feedforward, dropout=0.1):
        super(CustomTransformerEncoderLayer, self).__init__()
        self.self_attention = CustomMultiheadAttention(d_model, nhead)
        self.dropout1 = nn.Dropout(dropout)
        self.norm1 = nn.LayerNorm(d_model)

        self.feedforward = nn.Sequential(
            nn.Linear(d_model, dim_feedforward),
            nn.ReLU(),
            nn.Linear(dim_feedforward, d_model),
        )
        self.dropout2 = nn.Dropout(dropout)
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, src):
        # Self-attention
        attn_output, attn_weights = self.self_attention(src)
        src = self.norm1(src + self.dropout1(attn_output))

        # Feedforward
        feedforward_output = self.feedforward(src)
        src = self.norm2(src + self.dropout2(feedforward_output))

        return src, attn_weights  # Return attention weights


# Full Transformer Model
class FullMultiLevelTransformer(nn.Module):
    def __init__(self, input_dim, eqp_vocab_size, d_model=64, nhead=4, num_layers=2, dim_feedforward=128, dropout=0.1):
        super(FullMultiLevelTransformer, self).__init__()
        self.d_model = d_model

        self.eqp_embedding = nn.Embedding(eqp_vocab_size, d_model)  # Embedding for equipment IDs
        self.feature_embedding = nn.Linear(input_dim, d_model)
        self.feature_transformer = nn.ModuleList([
            CustomTransformerEncoderLayer(d_model, nhead, dim_feedforward, dropout)
            for _ in range(num_layers)
        ])
        self.fc = nn.Linear(d_model, 1)

    def forward(self, features, eqp_ids):
        feature_embed = self.feature_embedding(features)  # (batch_size, seq_len, d_model)
        eqp_embed = self.eqp_embedding(eqp_ids).unsqueeze(1)  # (batch_size, 1, d_model)

        combined_features = feature_embed + eqp_embed  # Combine feature and equipment embeddings
        attention_scores = []

        for layer in self.feature_transformer:
            combined_features, attn_weights = layer(combined_features)
            attention_scores.append(attn_weights)

        # Pooling and final output
        output = combined_features.mean(dim=1)  # Mean pooling
        return self.fc(output), attention_scores  # Return predictions and attention scores


# 중요도 계산 함수
def compute_variable_importance(attention_scores):
    """
    Calculate importance scores for each variable from attention scores.

    Args:
        attention_scores: Tensor of shape (batch_size, nhead, seq_len, seq_len)

    Returns:
        importance_scores: Tensor of shape (seq_len,)
    """
    # 어텐션 점수 평균
    head_mean_scores = attention_scores.mean(dim=1)  # (batch_size, seq_len, seq_len)
    batch_mean_scores = head_mean_scores.mean(dim=0)  # (seq_len, seq_len)
    variable_importance = batch_mean_scores.mean(dim=0)  # (seq_len,)
    return variable_importance


# 실행 코드
if __name__ == "__main__":
    batch_size = 16
    input_dim = 32  # Number of variables (features)
    eqp_vocab_size = 10  # Example size of equipment IDs
    d_model = 64
    nhead = 4
    num_layers = 2
    dim_feedforward = 128

    # 더미 데이터 생성
    features = torch.randn(batch_size, input_dim)  # (batch_size, input_dim)
    eqp_ids = torch.randint(0, eqp_vocab_size, (batch_size,))  # (batch_size,)

    # 모델 초기화 및 실행
    model = FullMultiLevelTransformer(input_dim, eqp_vocab_size, d_model, nhead, num_layers, dim_feedforward)
    predictions, attention_scores = model(features, eqp_ids)

    # 마지막 레이어의 Attention Scores 사용
    final_layer_attention_scores = attention_scores[-1]  # 마지막 레이어
    variable_importance = compute_variable_importance(final_layer_attention_scores)

    # 변수 중요도 출력
    feature_names = [f"Variable {i+1}" for i in range(input_dim)]
    importance_dict = {name: importance.item() for name, importance in zip(feature_names, variable_importance)}

    print("Variable Importance:", importance_dict)