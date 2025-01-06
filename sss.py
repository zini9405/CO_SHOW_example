# 정규화 
import pandas as pd
from sklearn.preprocessing import StandardScaler


df = cleaned_df

# 표준화 제외할 열 정의
exclude_columns = ['SFQR_AFS2', 'ESFQR2_MAX_AFS2', 'ZDDFRONTMEAN_01_AFS2', 'ESFQD_ZONE1MEAN_AFS2', 'ESFQD_ZONE1MAX_AFS2', 'ESFQD2_ZONE1MEAN_AFS2', 'ESFQD2_ZONE1MAX_AFS2',
                     'SFQR_AFS2_SUB', 'ESFQR2_MAX_AFS2_SUB', 'ZDDFRONTMEAN_01_AFS2_SUB', 'ESFQD_ZONE1MEAN_AFS2_SUB', 'ESFQD_ZONE1MAX_AFS2_SUB', 'ESFQD2_ZONE1MEAN_AFS2_SUB', 'ESFQD2_ZONE1MAX_AFS2_SUB']

# 숫자형 열 중 제외할 열 제외
numerical_columns = [col for col in df.select_dtypes(include=['number']).columns if col not in exclude_columns]

df.replace(-20, float('nan'), inplace=True)

# 표준화 수행
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

# 표준화 적용
for col in numerical_columns:
    expanded_min = expanded_ranges[col]['min']
    expanded_max = expanded_ranges[col]['max']
    
    # 범위 내에서만 표준화 수행
    mask = (df[col] >= expanded_min) & (df[col] <= expanded_max)
    standardized_values = scaler.fit_transform(df.loc[mask, [col]])
    df_standardized.loc[mask, col] = standardized_values

# 결과 저장
df_standardized.to_csv('all_minmax.csv', index=False)

# 출력: 최대/최소값과 확장된 범위
print("열별 최대값, 최소값 및 확장된 범위:")
for col in numerical_columns:
    print(f"{col}:")
    print(f"  원래 최소값: {max_min_values.loc['min', col]:.2f}, 최대값: {max_min_values.loc['max', col]:.2f}")
    print(f"  확장된 최소값: {expanded_ranges[col]['min']:.2f}, 확장된 최대값: {expanded_ranges[col]['max']:.2f}")
