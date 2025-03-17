import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('x.csv', low_memory=False)

# **1. 특정 값이 포함된 행만 필터링**
filter_values = [
    "SMNC_L40", "SEC BSI_6_5um_P+", "SEC_L4", 
    "SMIC_L55", "HH wuxi", "GFs_14nm", "SMNC_L55"
]
df_filtered = df[df['ANALYSIS_GROUP'].isin(filter_values)].copy()

# **2. DELTA_SFQR 제외하고 변동성이 낮은 열 삭제**
exclude_columns = ["DELTA_SFQR"]
numerical_columns = df_filtered.select_dtypes(include=['number']).columns.tolist()

# **각 열의 값 범위(최대 - 최소) 계산**
value_ranges = df_filtered[numerical_columns].max() - df_filtered[numerical_columns].min()

# **값 범위에 따른 분산 임계값 설정**
def determine_variance_threshold(value_range):
    if value_range <= 0.001:
        return 1e-8
    elif value_range <= 0.01:
        return 1e-6
    elif value_range <= 0.1:
        return 1e-4
    elif value_range <= 1:
        return 1e-3
    elif value_range <= 10:
        return 1e-2
    elif value_range <= 100:
        return 1e-1
    elif value_range <= 1000:
        return 1
    else:
        return 10  # 값이 매우 크다면 비교적 높은 분산값을 허용

# **각 열의 분산 임계값을 결정하고 제거할 열 찾기**
low_variance_columns = [
    col for col in numerical_columns 
    if col not in exclude_columns and df_filtered[col].var() < determine_variance_threshold(value_ranges[col])
]

# **낮은 변동성의 열 제거**
df_filtered = df_filtered.drop(columns=low_variance_columns)

# **3. 'DEPO'가 포함된 열만 선택**
depo_columns = [col for col in df_filtered.columns if 'DEPO' in col]
df_depo = df_filtered[depo_columns]

# **결과 출력**
print(f"삭제된 낮은 변동성의 열 개수: {len(low_variance_columns)}")
print(f"DEPO 포함 열 개수: {len(depo_columns)}")

# **필요하면 파일 저장**
df_depo.to_csv('filtered_x.csv', index=False)