import pandas as pd

# 파일 로드
file_path = "x.csv"  # 파일 경로
df = pd.read_csv(file_path)

# 특정 열 제거
columns_to_remove = ['z', 'y', 'a']
df_filtered = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors='ignore')

# 숫자형 데이터만 선택
df_numeric = df_filtered.select_dtypes(include=['number'])

# 분산(Variance) 및 사분위 범위(IQR) 계산
variance = df_numeric.var()
iqr = df_numeric.quantile(0.75) - df_numeric.quantile(0.25)

# 분산 기준으로 변화가 적은 열 정렬
variance_sorted = variance.sort_values()
iqr_sorted = iqr.sort_values()

# 결과 출력
print("분산 기준으로 변화가 적은 열 (오름차순 정렬):")
print(variance_sorted)

print("\nIQR 기준으로 변화가 적은 열 (오름차순 정렬):")
print(iqr_sorted)

# CSV로 저장 (선택 사항)
variance_sorted.to_csv("variance_sorted.csv")
iqr_sorted.to_csv("iqr_sorted.csv")