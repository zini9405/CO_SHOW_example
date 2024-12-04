import pandas as pd
import os
import re
from tqdm import tqdm

# 디렉토리 경로 설정
x_base_dir = 'x'
y_base_dir = 'y'
z_base_dir = 'z'
output_base_dir = 'x/updated_files'  # 결과 저장 경로

# 결과 저장 디렉터리 생성
os.makedirs(output_base_dir, exist_ok=True)

# 날짜 추출 정규식 (예: 24_01_01)
date_pattern = re.compile(r"(\d{2}_\d{2}_\d{2})")

# x 디렉터리 내 모든 하위 디렉터리 검색
x_sub_dirs = [os.path.join(x_base_dir, d) for d in os.listdir(x_base_dir) if os.path.isdir(os.path.join(x_base_dir, d))]

# 모든 x 디렉터리의 파일 처리
for x_sub_dir in tqdm(x_sub_dirs, desc="Processing directories"):
    # y와 z 디렉터리의 동일한 하위 디렉터리 경로 설정
    y_sub_dir = os.path.join(y_base_dir, os.path.basename(x_sub_dir))
    z_sub_dir = os.path.join(z_base_dir, os.path.basename(x_sub_dir))

    # 하위 디렉터리에 파일이 없으면 건너뜀
    if not (os.path.exists(y_sub_dir) and os.path.exists(z_sub_dir)):
        print(f"Skipping {x_sub_dir} (y or z directory missing)")
        continue

    # x 디렉터리에서 처리할 파일 목록 가져오기
    file_list = [f for f in os.listdir(x_sub_dir) if f.endswith('.csv')]

    for file_name in file_list:
        # 날짜 추출
        match = date_pattern.search(file_name)
        if not match:
            print(f"Skipping file {file_name} (no date found)")
            continue
        date_part = match.group(1)

        # 해당 날짜의 y, z 파일 검색
        y_file = next((os.path.join(y_sub_dir, f) for f in os.listdir(y_sub_dir) if date_part in f), None)
        z_file = next((os.path.join(z_sub_dir, f) for f in os.listdir(z_sub_dir) if date_part in f), None)

        # y, z 파일이 존재하지 않으면 건너뜀
        if not (y_file and z_file):
            print(f"Skipping {file_name} (y or z file missing for date {date_part})")
            continue

        # 각 파일의 경로 설정
        x_file = os.path.join(x_sub_dir, file_name)

        # 데이터프레임 읽기
        x_df = pd.read_csv(x_file)
        y_df = pd.read_csv(y_file)
        z_df = pd.read_csv(z_file)

        # y 파일에서 wa 값이 동일한 경우 sf 값을 y_sf 열로 추가
        x_df = x_df.merge(y_df[['wa', 'sf']], on='wa', how='left', suffixes=('', '_y'))
        x_df.rename(columns={'sf_y': 'y_sf'}, inplace=True)

        # z 파일에서 wa 값이 동일한 경우 sf 값을 z_sf 열로 추가
        x_df = x_df.merge(z_df[['wa', 'sf']], on='wa', how='left', suffixes=('', '_z'))
        x_df.rename(columns={'sf_z': 'z_sf'}, inplace=True)

        # 기존 sf 열 이름 조정 (필요 시)
        x_df.rename(columns={'sf': 'x_sf'}, inplace=True)

        # 결과 저장
        output_dir = os.path.join(output_base_dir, os.path.basename(x_sub_dir))
        os.makedirs(output_dir, exist_ok=True)  # 결과 저장 디렉터리 생성
        output_path = os.path.join(output_dir, file_name)
        x_df.to_csv(output_path, index=False)

print(f"모든 파일 처리가 완료되었습니다. 결과는 {output_base_dir}에 저장되었습니다.")