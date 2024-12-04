import pandas as pd
import os
from tqdm import tqdm

# 경로 설정
final_dataset_path = 'C:/Users/SKsiltron/Desktop/SFQR/final_dataset'
output_dir_path = 'C:/Users/SKsiltron/Desktop/SFQR/grouped_datasets'

# 결과 저장 디렉터리 생성
os.makedirs(output_dir_path, exist_ok=True)

# final_dataset 디렉터리에서 모든 CSV 파일 가져오기
csv_files = [os.path.join(final_dataset_path, f) for f in os.listdir(final_dataset_path) if f.endswith('.csv')]

# 모든 CSV 파일 취합
dataframes = []
for csv_file in tqdm(csv_files, desc="Loading CSV files"):
    df = pd.read_csv(csv_file)
    dataframes.append(df)

# 모든 데이터프레임 합치기
combined_df = pd.concat(dataframes, ignore_index=True)

# STEP_ID와 SFQR_AFS2 열에 빈값인 행 제거
cleaned_df = combined_df.dropna(subset=['STEP_ID', 'SFQR_AFS2'])

# 'Unnamed: 0' 열 제거 (존재할 경우)
if 'Unnamed: 0' in cleaned_df.columns:
    cleaned_df = cleaned_df.drop(columns=['Unnamed: 0'])

# EQP_ID로 그룹화하여 각 그룹을 별도 파일로 저장
for eqp_id, group_df in tqdm(cleaned_df.groupby('EQP_ID'), desc="Saving grouped files"):
    # 파일 이름 설정
    output_file_path = os.path.join(output_dir_path, f'group_{eqp_id}.csv')
    # 그룹 데이터 저장
    group_df.to_csv(output_file_path, index=False)

print(f"그룹별 파일 저장이 완료되었습니다. 결과는 {output_dir_path}에 저장되었습니다.")