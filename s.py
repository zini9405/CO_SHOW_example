import pandas as pd
import numpy as np
from sklearn.preprocessing import QuantileTransformer

# 데이터 준비 (예제 데이터)
data = {
    'MAIN_RUNTIME': np.random.rand(100),
    'DD_USE_NUM': np.random.rand(100),
    'SLURRY_USE_NUM': np.random.rand(100),
    'PAD_COUNT': np.random.rand(100),
    'CARRIER_MTL_USE_NUM': np.random.rand(100),
    'GBIR': np.random.rand(100),
}

df = pd.DataFrame(data)

# QuantileTransformer 초기화
quantile_transformer = QuantileTransformer(output_distribution='normal', random_state=42)

# 변환 및 복구 작업
transformed_data = {}
recovered_data = {}

for column in df.columns:
    # 각 열에 QuantileTransformer 적용
    transformed = quantile_transformer.fit_transform(df[[column]])
    transformed_data[column] = transformed.flatten()

    # 원래 값으로 복구
    recovered = quantile_transformer.inverse_transform(transformed)
    recovered_data[column] = recovered.flatten()

# 변환된 데이터프레임 생성
transformed_df = pd.DataFrame(transformed_data)
recovered_df = pd.DataFrame(recovered_data)

# 결과 확인
print("원본 데이터:")
print(df.head())
print("\nQuantileTransformer 변환 데이터:")
print(transformed_df.head())
print("\n복구된 데이터:")
print(recovered_df.head())

# 원본 데이터와 복구된 데이터 비교
print("\n원본 데이터와 복구된 데이터 비교:")
print(np.allclose(df.values, recovered_df.values))