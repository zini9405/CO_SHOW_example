import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('x.csv', low_memory=False)

# **1. 특정 값이 포함된 행만 필터링**
filter_values = [
    "SMNC_L40", "SEC BSI_6_5um_P+", "SEC_L4", 
    "SMIC_L55", "HH wuxi", "GFs_14nm", "SMNC_L55"
]
df_filtered = df[df['ANALYSIS_GROUP'].isin(filter_values)].copy()

# **2. DELTA_SFQR 제외하고 변동성 낮은 열 삭제**
exclude_columns = ["DELTA_SFQR"]
numerical_columns = df_filtered.select_dtypes(include=['number']).columns.tolist()

# 분산이 낮은 열 찾기 (0 또는 거의 0인 경우)
low_variance_columns = [col for col in numerical_columns if col not in exclude_columns and df_filtered[col].var() < 1e-5]

# 변동성이 낮은 열 삭제
df_filtered = df_filtered.drop(columns=low_variance_columns)

# **3. 'DEPO'가 포함된 열만 선택**
depo_columns = [col for col in df_filtered.columns if 'DEPO' in col]
df_depo = df_filtered[depo_columns]

# 최종 결과 확인
print(f"삭제된 낮은 변동성의 열 개수: {len(low_variance_columns)}")
print(f"DEPO 포함 열 개수: {len(depo_columns)}")

# 필요하면 파일 저장
df_depo.to_csv('filtered_x.csv', index=False)