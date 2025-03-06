import os
import pandas as pd
from collections import defaultdict

# 파일이 있는 디렉토리 경로 설정
directory = "your_directory_path_here"  # 여기에 실제 디렉토리 경로 입력

# 날짜별 파일을 저장할 딕셔너리
files_grouped = defaultdict(list)

# 디렉토리에서 파일 목록 가져오기
for file in os.listdir(directory):
    if file.endswith(".csv"):  # CSV 파일만 처리
        prefix = "_".join(file.split("_")[:2])  # 날짜 부분 추출 (예: 24_01)
        files_grouped[prefix].append(file)

# 파일 병합 및 저장
for date_prefix, files in files_grouped.items():
    dataframes = []
    
    for file in files:
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)
        dataframes.append(df)

    # 데이터 병합
    merged_df = pd.concat(dataframes, ignore_index=True)

    # 병합된 파일 저장
    output_file = os.path.join(directory, f"{date_prefix}.csv")
    merged_df.to_csv(output_file, index=False)
    print(f"저장 완료: {output_file}")

print("모든 파일 병합 완료!")