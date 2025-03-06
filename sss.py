import os

# 특정 디렉토리 경로 설정
directory = "your_directory_path_here"  # 불러올 디렉토리 경로로 변경하세요

# 디렉토리에서 .txt 파일만 필터링하여 리스트 생성
txt_files = [f for f in os.listdir(directory) if f.endswith(".txt")]

# 결과 출력
print(txt_files)