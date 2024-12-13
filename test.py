import os
import pandas as pd

# 디렉토리 경로 설정
directory_path = "path_to_your_directory"

# 대상 파일 리스트
target_files = [
    "CENC11B.csv", "CENC16B.csv", "CENC43B.csv", "CENC46B.csv", "CENC48B.csv",
    "CENC5A.csv", "ZCENC01A.csv", "ZCENC01B.csv", "ZCENC02A.csv", "ZCENC02B.csv",
    "ZCENC03A.csv", "ZCENC03B.csv", "ZCENC04A.csv", "ZCENC04B.csv"
]

# 디렉토리 내 대상 파일만 처리
for file_name in os.listdir(directory_path):
    if file_name in target_files:
        file_path = os.path.join(directory_path, file_name)
        print(f"Processing file: {file_name}")
        
        # 파일 읽기
        try:
            df = pd.read_csv(file_path)
            # 여기서 추가 작업을 수행할 수 있습니다.
            print(df.head())  # 데이터 확인
        except Exception as e:
            print(f"Error reading file {file_name}: {e}")