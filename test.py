import torch
import pandas as pd
import shap
import matplotlib.pyplot as plt

# CSV 파일 경로
csv_path = "your_input_file.csv"  # CSV 파일 경로 지정

# CSV 데이터 읽기
data = pd.read_csv(csv_path)

# 33개의 열 이름 (CSV의 컬럼 이름 사용)
feature_names = list(data.columns)

# 입력 데이터 (numpy 배열로 변환)
input_data = data.to_numpy()

# 모델 정의
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

# 모델 초기화 (입력 차원은 33으로 설정)
model = FullMultiLevelTransformer(input_dim=33, d_model=256, nhead=4, num_layers=4, dim_feedforward=512)

# 모델을 평가 모드로 전환
model.eval()

# SHAP Explainer 정의
explainer = shap.Explainer(
    lambda x: model(torch.tensor(x, dtype=torch.float32)).detach().numpy(),
    input_data
)

# SHAP 값 계산
shap_values = explainer(input_data)

# SHAP 시각화: 전체 데이터에 대한 중요도
shap.summary_plot(shap_values, input_data, feature_names=feature_names)

# 특정 샘플에 대한 SHAP Force Plot
sample_index = 0  # 예: 첫 번째 샘플
shap.force_plot(
    explainer.expected_value[0],
    shap_values[sample_index],
    input_data[sample_index],
    feature_names=feature_names
)