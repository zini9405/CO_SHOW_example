import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 파일 로드
file_path = "x.csv"
df = pd.read_csv(file_path)

# 특정 열 저장 후 제거
columns_to_remove = ['z', 'y', 'a']
df_removed = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors='ignore')
df_reserved = df[columns_to_remove]  # 제거된 열 저장

# 숫자형 데이터만 선택 후 정규화 (Min-Max Scaling)
df_numeric = df_removed.select_dtypes(include=['number'])
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_numeric), columns=df_numeric.columns)

# 분산 및 IQR 계산 (정규화된 데이터 기준)
variance = df_scaled.var()
iqr = df_scaled.quantile(0.75) - df_scaled.quantile(0.25)

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

# 원본 데이터에서 선택된 열만 유지
df_final_changing = df_removed[changing_cols]
df_final_high_changing = df_removed[high_changing_cols]

# 원본 데이터의 z, y, a 열 다시 추가
df_final_changing = pd.concat([df_final_changing, df_reserved], axis=1)
df_final_high_changing = pd.concat([df_final_high_changing, df_reserved], axis=1)

# 결과 저장
df_final_changing.to_csv("changing_columns_with_zya.csv", index=False)
df_final_high_changing.to_csv("high_changing_columns_with_zya.csv", index=False)

# 결과 출력
print(f"변화가 있는 열 (중위값 기준): {changing_cols}")
print(f"변화가 큰 열 (Q3 기준): {high_changing_cols}")