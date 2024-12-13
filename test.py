import pandas as pd

# CSV 파일 경로
csv1_path = "file1.csv"  # 첫 번째 CSV 파일 경로
csv2_path = "file2.csv"  # 두 번째 CSV 파일 경로

# CSV 파일 읽기
df1 = pd.read_csv(csv1_path)
df2 = pd.read_csv(csv2_path)

# 병합을 위한 기준 열 지정 (공통 열이 있다고 가정)
# 예: 'id' 또는 'timestamp' 등
merge_column = "id"  # 공통 기준 열 이름으로 변경 필요

# 병합 (공통 열을 기준으로 결합)
merged_df = pd.merge(df1, df2[['pred', merge_column]], on=merge_column, how='left')

# 결과 확인
print(merged_df.head())

# 병합된 데이터 저장
merged_df.to_csv("merged_file.csv", index=False)
print("Merged file saved as 'merged_file.csv'.")