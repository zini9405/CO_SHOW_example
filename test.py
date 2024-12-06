import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('파일명.csv')

# 각 열의 최대값과 최소값 계산 (텍스트 제외)
numerical_columns = df.select_dtypes(include=['number']).columns  # 숫자형 데이터만 선택
max_min_values = df[numerical_columns].agg(['min', 'max'])

# 정규화 (Min-Max Scaling)
df_normalized = df.copy()  # 원본 유지
for col in numerical_columns:
    df_normalized[col] = (df[col] - max_min_values.loc['min', col]) / (max_min_values.loc['max', col] - max_min_values.loc['min', col])

# 최대/최소 값 확인
print("최대/최소 값 범위:")
print(max_min_values)

# 정규화된 데이터 저장
df_normalized.to_csv('정규화된_파일명.csv', index=False)