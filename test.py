
import pandas as pd

# CSV 파일 경로
csv1_path = "file1.csv"
csv2_path = "file2.csv"

# CSV 파일 읽기
df1 = pd.read_csv(csv1_path)
df2 = pd.read_csv(csv2_path)

# 기준 열 확인
merge_column = "id"  # 공통 기준 열 설정

# 중복 제거 (필요시)
df1 = df1.drop_duplicates(subset=[merge_column])
df2 = df2.drop_duplicates(subset=[merge_column])

# 병합 수행
merged_df = pd.merge(df1, df2[['pred', merge_column]], on=merge_column, how='left')

# 병합 후 행 수 확인
print(f"Before merge: {len(df1)} rows")
print(f"After merge: {len(merged_df)} rows")

# 병합 결과 저장
merged_df.to_csv("merged_file.csv", index=False)
print("Merged file saved as 'merged_file.csv'.")