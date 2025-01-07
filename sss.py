        import torch
from torch import nn
from einops import rearrange


# Custom Transformer Encoder Layer for extracting attention scores
class CustomTransformerEncoderLayer(nn.TransformerEncoderLayer):
    def __init__(self, *args, **kwargs):
        super(CustomTransformerEncoderLayer, self).__init__(*args, **kwargs)
        self.attention_scores = None  # Store attention scores

    def forward(self, src, src_mask=None, src_key_padding_mask=None):
        # Extract attention scores
        src2, self.attention_scores = self.self_attn(
            src, src, src, attn_mask=src_mask, key_padding_mask=src_key_padding_mask
        )
        src = src + self.dropout1(src2)
        src = self.norm1(src)

        src2 = self.linear2(self.dropout(self.activation(self.linear1(src))))
        src = src + self.dropout2(src2)
        src = self.norm2(src)

        return src


# Transformer Model with Custom Attention Extraction
class FullMultiLevelTransformerWithAttention(nn.Module):
    def __init__(self, input_dim, eqp_vocab_size, d_model=64, nhead=4, num_layers=2, dim_feedforward=128, dropout=0.1):
        super(FullMultiLevelTransformerWithAttention, self).__init__()
        self.d_model = d_model

        self.eqp_embedding = nn.Embedding(eqp_vocab_size, d_model)
        self.feature_embedding = nn.Linear(input_dim, d_model)

        # Use CustomTransformerEncoderLayer for extracting attention scores
        encoder_layers = [CustomTransformerEncoderLayer(
            d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout
        ) for _ in range(num_layers)]
        self.feature_transformer = nn.TransformerEncoder(nn.ModuleList(encoder_layers), num_layers=num_layers)

        self.fc = nn.Linear(d_model, 1)

    def forward(self, features, eqp_ids):
        feature_embed = self.feature_embedding(features)
        eqp_embed = self.eqp_embedding(eqp_ids)

        combined_features = feature_embed + eqp_embed
        combined_features = rearrange(combined_features, 'b d -> 1 b d')

        transformed_features = self.feature_transformer(combined_features)

        # Flatten and reduce dimensions
        output = transformed_features.mean(dim=0)  # Mean pooling over time
        return self.fc(output)

    def get_attention_scores(self):
        # Extract attention scores from each layer
        scores = [layer.attention_scores for layer in self.feature_transformer.layers]
        return scores


# 모델 초기화
eqp_vocab_size = 100  # Example vocab size
input_dim = 32  # Example input dimension
model = FullMultiLevelTransformerWithAttention(
    input_dim=input_dim, eqp_vocab_size=eqp_vocab_size, d_model=256, nhead=4, num_layers=4, dim_feedforward=512
)

# Dummy Input for Testing
features = torch.randn(16, 32)  # Batch of 16, 32 features
eqp_ids = torch.randint(0, eqp_vocab_size, (16,))  # Batch of 16 equipment IDs

# Forward Pass
output = model(features, eqp_ids)

# Attention Scores Extraction
attention_scores = model.get_attention_scores()
print("Attention Scores for Each Layer:", attention_scores)