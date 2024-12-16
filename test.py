# Transformer 모델 정의
class FullMultiLevelTransformer(torch.nn.Module):
    def __init__(self, input_dim, d_model=64, nhead=4, num_layers=6, dim_feedforward=128):
        super(FullMultiLevelTransformer, self).__init__()
        self.feature_embedding = torch.nn.Linear(input_dim, d_model)
        self.feature_transformer = torch.nn.TransformerEncoder(
            torch.nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward),
            num_layers=num_layers,
        )
        self.fc = torch.nn.Linear(d_model, 1)

    def forward(self, x):
        x = self.feature_embedding(x)
        x = x.unsqueeze(1)  # (batch_size, seq_len=1, d_model)
        x = self.feature_transformer(x)
        x = x.mean(dim=1)  # (batch_size, d_model)
        return self.fc(x)
    
model = FullMultiLevelTransformer(input_dim=33, d_model=256, nhead=4, num_layers=4, dim_feedforward=512)

이 모델의 ATTENTION MAP 보고싶어
