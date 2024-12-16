import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
import pickle

# 표준화 수행 시 사용한 scaler 저장할 딕셔너리
scalers = {}

# 원본 데이터 읽기
df = data

# 표준화 제외할 열 정의
exclude_columns = ['SFQR_AFS2', 'SFQR_AFS2_SUB']

# 숫자형 열 중 제외할 열 제외
numerical_columns = [col for col in df.select_dtypes(include=['number']).columns if col not in exclude_columns]

# 결측값 처리
df.replace(-20, float('nan'), inplace=True)

# 열별 최대/최소값 계산 및 10% 확장
max_min_values = df.agg(['min', 'max'])
expanded_ranges = {
    col: {
        "min": max_min_values.loc['min', col] - (max_min_values.loc['min', col]) * 0.1,
        "max": max_min_values.loc['max', col] + (max_min_values.loc['max', col]) * 0.1,
    }
    for col in numerical_columns
}

# 표준화 적용
df_standardized = df.copy()
for col in numerical_columns:
    expanded_min = expanded_ranges[col]['min']
    expanded_max = expanded_ranges[col]['max']
    
    # 범위 내에서만 표준화 수행
    mask = (df[col] >= expanded_min) & (df[col] <= expanded_max)
    
    scaler = StandardScaler()
    standardized_values = scaler.fit_transform(df.loc[mask, [col]])
    df_standardized.loc[mask, col] = standardized_values
    
    # 열별로 사용한 scaler 저장
    scalers[col] = {"mean": scaler.mean_[0], "scale": scaler.scale_[0]}

# 표준화된 데이터 저장
df_standardized.to_csv('final.csv', index=False)

# Scaler 정보 저장 (복원을 위해 사용)
with open('scalers.pkl', 'wb') as f:
    pickle.dump(scalers, f)

# 결과 출력
print("스케일러 저장 완료: scalers.pkl")

# 복원 코드
def restore_original_values(standardized_df, scalers):
    restored_df = standardized_df.copy()
    for col in numerical_columns:
        if col in scalers:
            mean = scalers[col]["mean"]
            scale = scalers[col]["scale"]
            restored_df[col] = restored_df[col] * scale + mean
    return restored_df

# 복원 예제
with open('scalers.pkl', 'rb') as f:
    loaded_scalers = pickle.load(f)

restored_df = restore_original_values(df_standardized, loaded_scalers)
restored_df.to_csv('restored.csv', index=False)
print("복원된 데이터 저장 완료: restored.csv")