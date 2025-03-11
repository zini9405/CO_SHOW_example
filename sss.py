import os
import pandas as pd

# 디렉토리 경로 설정
dir_6100 = "6100_process"
dir_6300 = "6300_process"
dir_const = "const_dataset_process"
output_dir = "merged_dataset_process"

# 저장 디렉토리 생성
os.makedirs(output_dir, exist_ok=True)

# 공통된 파일 찾기
files_6100 = set(os.listdir(dir_6100))
files_6300 = set(os.listdir(dir_6300))
files_const = set(os.listdir(dir_const))

common_files = files_6100 & files_6300 & files_const  # 3개 디렉토리에 모두 존재하는 파일명 찾기

for file_name in common_files:
    try:
        # 6300_process 데이터 로드 및 필터링
        df_6300 = pd.read_csv(os.path.join(dir_6300, file_name), encoding="utf-8", low_memory=False)
        df_6300_filtered = df_6300[['WAFER_ID', 'GBIR_AFS2']]

        # 6100_process 데이터 로드
        df_6100 = pd.read_csv(os.path.join(dir_6100, file_name), encoding="utf-8", low_memory=False)

        # 6100_process와 6300_process 병합 (WAF_ID == WAFER_ID)
        com_x = df_6100.merge(df_6300_filtered, left_on="WAF_ID", right_on="WAFER_ID", how="inner")

        # const_dataset_process 데이터 로드
        df_const = pd.read_csv(os.path.join(dir_const, file_name), encoding="utf-8", low_memory=False)

        # 최종 병합 (WAF_ID 기준)
        final_df = com_x.merge(df_const, on="WAF_ID", how="inner")

        # 파일 저장
        output_file = os.path.join(output_dir, file_name)
        final_df.to_csv(output_file, index=False)
        print(f"저장 완료: {output_file}")

    except Exception as e:
        print(f"파일 처리 오류: {file_name} - {e}")

print("모든 파일 병합 완료!")