import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pickle

# 표준화 수행 시 사용한 scaler 저장할 딕셔너리
scalers = {}

# 원본 데이터 읽기
df = pd.read_csv('processed_X_grouped.csv')

# 표준화 제외할 열 정의
exclude_columns = ['ANALYSIS_GROUP', 'SUBLOT', 'WAFER_ID', 'DATE', 'EQP_NM', 'Delta_SFQR', 'CL_HST_REG_DTTM']

# 숫자형 열 중 제외할 열 제외
numerical_columns = [col for col in df.select_dtypes(include=['number']).columns if col not in exclude_columns]

# 숫자형 열만 대상으로 min/max 계산
max_min_values = df[numerical_columns].agg(['min', 'max'])

# 열별 최대/최소값 계산 및 10% 확장
expanded_ranges = {
    col: {
        "min": max_min_values.loc['min', col] - (max_min_values.loc['min', col]) * 0.1,
        "max": max_min_values.loc['max', col] + (max_min_values.loc['max', col]) * 0.1,
    }
    for col in numerical_columns
}

# 정규화(Normalization) 적용
df_normalized = df.copy()
for col in numerical_columns:
    expanded_min = expanded_ranges[col]['min']
    expanded_max = expanded_ranges[col]['max']
    
    # 범위 내에서만 정규화 수행
    mask = (df[col] >= expanded_min) & (df[col] <= expanded_max)
    
    scaler = MinMaxScaler(feature_range=(0, 1))  # 0~1 범위로 변환
    normalized_values = scaler.fit_transform(df.loc[mask, [col]])
    df_normalized.loc[mask, col] = normalized_values
    
    # 열별로 사용한 scaler 저장
    scalers[col] = {"min": scaler.data_min_[0], "max": scaler.data_max_[0]}

# Scaler 정보 저장 (복원을 위해 사용)
with open('scalers_SFQR_all.pkl', 'wb') as f:
    pickle.dump(scalers, f)

# 결과 출력
print("스케일러 저장 완료: scalers_SFQR_all.pkl")