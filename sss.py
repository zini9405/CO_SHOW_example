import pandas as pd
from sklearn.preprocessing import StandardScaler

# 표준화 제외할 열 정의
exclude_columns = ['SFQR_AFS2', 'ESFQR2_MAX_AFS2', 'ZDDFRONTMEAN_01_AFS2', 'ESFQD_ZONE1MEAN_AFS2', 'ESFQD_ZONE1MAX_AFS2', 'ESFQD2_ZONE1MEAN_AFS2', 'ESFQD2_ZONE1MAX_AFS2',
                     'SFQR_AFS2_SUB', 'ESFQR2_MAX_AFS2_SUB', 'ZDDFRONTMEAN_01_AFS2_SUB', 'ESFQD_ZONE1MEAN_AFS2_SUB', 'ESFQD_ZONE1MAX_AFS2_SUB', 'ESFQD2_ZONE1MEAN_AFS2_SUB', 'ESFQD2_ZONE1MAX_AFS2_SUB']

# 숫자형 열 중 제외할 열 제외
numerical_columns = [col for col in df.select_dtypes(include=['number']).columns if col not in exclude_columns]

# 정규화 수행
df.replace(-20, float('nan'), inplace=True)
df_standardized = df.copy()
scaler = StandardScaler()

# 열별로 최대/최소값 계산 및 10% 확장
max_min_values = df.agg(['min', 'max'])
expanded_ranges = {
    col: {
        "min": max_min_values.loc['min', col] - (max_min_values.loc['min', col]) * 0.1,
        "max": max_min_values.loc['max', col] + (max_min_values.loc['max', col]) * 0.1,
    }
    for col in numerical_columns
}

# 표준화 적용 및 원본 범위 저장
scalers = {}
for col in numerical_columns:
    expanded_min = expanded_ranges[col]['min']
    expanded_max = expanded_ranges[col]['max']
    
    # 범위 내에서만 표준화 수행
    mask = (df[col] >= expanded_min) & (df[col] <= expanded_max)
    scalers[col] = StandardScaler()  # 각 열에 대해 scaler 저장
    standardized_values = scalers[col].fit_transform(df.loc[mask, [col]])
    df_standardized.loc[mask, col] = standardized_values

# 원본값으로 복원
df_restored = df_standardized.copy()
for col in numerical_columns:
    expanded_min = expanded_ranges[col]['min']
    expanded_max = expanded_ranges[col]['max']
    
    # 범위 내에서만 역변환 수행
    mask = (df[col] >= expanded_min) & (df[col] <= expanded_max)
    restored_values = scalers[col].inverse_transform(df_standardized.loc[mask, [col]])
    df_restored.loc[mask, col] = restored_values

# 결과 저장
df_restored.to_csv('restored_values.csv', index=False)

print("정규화된 값을 원본값으로 복원 완료!")