import pandas as pd

# 파일 로드
file_path = "x.csv"
df = pd.read_csv(file_path)

# 특정 열 제거
columns_to_remove = ['z', 'y', 'a']
df_filtered = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors='ignore')

# 숫자형 데이터만 선택
df_numeric = df_filtered.select_dtypes(include=['number'])

# 분산 및 IQR 계산
variance = df_numeric.var()
iqr = df_numeric.quantile(0.75) - df_numeric.quantile(0.25)

# 중위값(Median) 및 75% 이상(Q3) 계산
variance_median = variance.median()
variance_q3 = variance.quantile(0.75)

iqr_median = iqr.median()
iqr_q3 = iqr.quantile(0.75)

# 변화가 있는 열 선택 (중위값 이상)
changing_variance_cols = variance[variance >= variance_median].index.tolist()
changing_iqr_cols = iqr[iqr >= iqr_median].index.tolist()

# 변화가 큰 열 선택 (Q3 이상)
high_variance_cols = variance[variance >= variance_q3].index.tolist()
high_iqr_cols = iqr[iqr >= iqr_q3].index.tolist()

# 변화가 있는 열 (중위값 이상 중 하나라도 해당)
changing_cols = list(set(changing_variance_cols) | set(changing_iqr_cols))

# 변화가 큰 열 (Q3 이상 중 하나라도 해당)
high_changing_cols = list(set(high_variance_cols) | set(high_iqr_cols))

# 결과 출력
print(f"변화가 있는 열 (분산 ≥ {variance_median} 또는 IQR ≥ {iqr_median}): {changing_cols}")
print(f"변화가 큰 열 (분산 ≥ {variance_q3} 또는 IQR ≥ {iqr_q3}): {high_changing_cols}")

# 변화가 있는 열을 새로운 CSV로 저장 (선택 사항)
df_numeric[changing_cols].to_csv("changing_columns.csv", index=False)
df_numeric[high_changing_cols].to_csv("high_changing_columns.csv", index=False)