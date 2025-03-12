import pandas as pd

# 파일 로드
file_path = "x.csv"  # 파일 경로 지정
df = pd.read_csv(file_path)

# 특정 열 제거
columns_to_remove = ['z', 'y', 'a']
df_filtered = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors='ignore')

# 분산(Variance) 및 사분위 범위(IQR) 계산
variance = df_filtered.var()
iqr = df_filtered.quantile(0.75) - df_filtered.quantile(0.25)

# 변화가 적은 열을 찾기 위해 정렬
low_variance_cols = variance.nsmallest(10).index.tolist()  # 분산이 작은 10개 열
low_iqr_cols = iqr.nsmallest(10).index.tolist()  # IQR이 작은 10개 열

# 두 기준에 모두 해당하는 열 선택
selected_cols = list(set(low_variance_cols) & set(low_iqr_cols))

# 결과 출력
print("분산 기준 변화가 적은 열:", low_variance_cols)
print("IQR 기준 변화가 적은 열:", low_iqr_cols)
print("최종 선택된 변화가 적은 열:", selected_cols)

# 변화가 적은 열의 데이터 저장 (선택 사항)
df_filtered[selected_cols].to_csv("low_variability_columns.csv", index=False)