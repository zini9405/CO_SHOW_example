import os
import pandas as pd

# WAF_ID 디렉토리 경로 지정
directory = "waf_id"  # 디렉토리 이름 수정 필요

# 디렉토리 내 모든 .csv 파일 리스트 가져오기
csv_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]

# 파일 합치기
combined_df = pd.DataFrame()

for file in csv_files:
    # 각 파일 읽기
    df = pd.read_csv(file)
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# 결과 출력
print(combined_df)

# 합친 결과를 CSV 파일로 저장 (필요한 경우)
combined_df.to_csv("combined_waf_id.csv", index=False)