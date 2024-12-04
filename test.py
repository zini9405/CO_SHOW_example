import pandas as pd
import os
import re
from tqdm import tqdm

# 경로 설정
epi_b_base_path = 'C:/Users/SKsiltron/Desktop/SFQR/epi_before_process'
epi_a_base_path = 'C:/Users/SKsiltron/Desktop/SFQR/epi_after_process'
x_para_base_path = 'C:/Users/SKsiltron/Desktop/SFQR/x_para_process'
save_path = 'C:/Users/SKsiltron/Desktop/SFQR/final_dataset'

# 결과 저장 디렉터리 생성
os.makedirs(save_path, exist_ok=True)

# 날짜 추출 정규식
date_pattern = re.compile(r"(\d{4}_\d{2}_\d{2})")

# x_para_base_path에서 처리할 파일 목록 가져오기
x_file_list = [f for f in os.listdir(x_para_base_path) if f.endswith('.csv')]

# 최종 데이터를 저장할 리스트
final_dataframes = []

# 파일 처리
for x_file_name in tqdm(x_file_list, desc="Processing files"):
    # 날짜 추출
    match = date_pattern.search(x_file_name)
    if not match:
        print(f"Skipping file {x_file_name} (no date found)")
        continue
    date_part = match.group(1)

    # 해당 날짜의 epi_a와 epi_b 파일 검색
    epi_a_file = next((os.path.join(epi_a_base_path, f) for f in os.listdir(epi_a_base_path) if date_part in f), None)
    epi_b_file = next((os.path.join(epi_b_base_path, f) for f in os.listdir(epi_b_base_path) if date_part in f), None)

    # epi_a 또는 epi_b 파일이 없으면 건너뜀
    if not (epi_a_file and epi_b_file):
        print(f"Skipping {x_file_name} (matching epi_a or epi_b file missing for date {date_part})")
        continue

    # 파일 경로 설정
    x_file_path = os.path.join(x_para_base_path, x_file_name)

    # 데이터프레임 읽기
    x_df = pd.read_csv(x_file_path)
    epi_a_df = pd.read_csv(epi_a_file)
    epi_b_df = pd.read_csv(epi_b_file)

    # WAF_ID와 WAFER_ID를 기준으로 SFQR_AFS2 열 붙이기 (epi_a)
    x_df = x_df.merge(epi_a_df[['WAFER_ID', 'SFQR_AFS2']], left_on='WAF_ID', right_on='WAFER_ID', how='left', suffixes=('', '_A'))
    x_df.rename(columns={'SFQR_AFS2': 'SFQR_AFS2_A'}, inplace=True)
    x_df.drop(columns=['WAFER_ID'], inplace=True)  # 중간에 생성된 열 삭제

    # WAF_ID와 WAFER_ID를 기준으로 SFQR_AFS2 열 붙이기 (epi_b)
    x_df = x_df.merge(epi_b_df[['WAFER_ID', 'SFQR_AFS2']], left_on='WAF_ID', right_on='WAFER_ID', how='left', suffixes=('', '_B'))
    x_df.rename(columns={'SFQR_AFS2': 'SFQR_AFS2_B'}, inplace=True)
    x_df.drop(columns=['WAFER_ID'], inplace=True)  # 중간에 생성된 열 삭제

    # 처리된 데이터 저장
    final_dataframes.append(x_df)

# 모든 데이터를 하나의 데이터프레임으로 병합
final_df = pd.concat(final_dataframes, ignore_index=True)

# 최종 결과 저장
final_output_path = os.path.join(save_path, 'final_dataset.csv')
final_df.to_csv(final_output_path, index=False)

print(f"모든 파일 처리가 완료되었습니다. 결과는 {final_output_path}에 저장되었습니다.")