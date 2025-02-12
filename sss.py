import pandas as pd
import os
import glob

# 24_01_x 디렉토리 경로
dir_path = "24_01_x"

# 디렉토리 내 모든 parquet 파일 리스트 가져오기
parquet_files = glob.glob(os.path.join(dir_path, "*.parquet"))

# 모든 parquet 파일을 읽어 하나의 DataFrame으로 병합
df_list = [pd.read_parquet(file) for file in parquet_files]
combined_df = pd.concat(df_list, ignore_index=True)

# 결과 확인
print(f"병합된 데이터 개수: {len(combined_df)}")
print(combined_df.head())

# CSV 또는 Parquet로 저장 (선택사항)
combined_df.to_parquet("24_01_x_combined.parquet", index=False)  # Parquet 저장
# combined_df.to_csv("24_01_x_combined.csv", index=False)  # CSV 저장 (필요시)