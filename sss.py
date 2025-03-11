import os
import pandas as pd

# 처리할 디렉토리 설정
input_dir = "merged_dataset_process"
output_dir = "merged_dataset_process_cleaned"
os.makedirs(output_dir, exist_ok=True)

# 유지할 장비 ID 목록
valid_eqp_ids = {
    "BPDPD100", "BPDPD101", "BPDPD102", "BPDPD103", "BPDPD104", "BPDPD105", "BPDPD106", "BPDPD107", 
    "BPDPD108", "BPDPD109", "BPDPD111", "BPDPD112", "BPDPD113", "BPDPD114", "BPDPD115", "BPDPD116", 
    "BPDPD117", "BPDPD118", "BPDPD119", "BPDPD74", "BPDPD80", "BPDPD81", "BPDPD82", "BPDPD83", 
    "BPDPD84", "BPDPD85", "BPDPD86", "BPDPD87", "BPDPD88", "BPDPD89", "BPDPD90", "BPDPD91", 
    "BPDPD92", "BPDPD93", "BPDPD94", "BPDPD95", "BPDPD96", "BPDPD97", "BPDPD98", "BPDPD99"
}

# 유지할 컬럼 목록
columns_to_keep = [
    "BASE_DT", "EQP_ID_x", "WAF_ID", "SLOT_NO_x", "RECIPE_ID",
    "INTERNLA_GEAR_RPM_ACTUAL_STEP_MEAN", "PAD_TEMP_STEP_MEAN",
    "RING_GEAR_MOTOR_CURRENT_STEP_MEAN", "SLURRY_1_FLOW_STEP_MEAN",
    "SLURRY_IN_TEMP_STEP_MEAN", "SUN_GEAR_MOTOR_CURRENT_STEP_MEAN",
    "SUN_GEAR_RPM_ACTUAL_STEP_MEAN", "SURFACTANT_FLOW_ACTUAL_STEP_MEAN",
    "PRS_PRES_ACTUAL__STEP_MEAN", "UPPER_COOLING_IN_TEMP_STEP_MEAN",
    "UPPER_COOLING_OUT_TEMP_STEP_MEAN", "UPPER_COOLING_FLOW_STEP_MEAN",
    "UPPER_MOTOR_CURRENT_STEP_MEAN", "UPPER_RPM_ACTUAL_STEP_MEAN",
    "LOWER_COOLING_IN_TEMP_STEP_MEAN", "LOWER_COOLING_OUT_TEMP_STEP_MEAN",
    "LOWER_COOLING_FLOW_STEP_MEAN", "LOWER_MOTOR_CURRENT_STEP_MEAN",
    "LOWER_RPM_ACTUAL_STEP_MEAN", "PRS_PRES_ACTUAL__STEP_COUNT",
    "PAD_COUNT", "SLURRY_USE_NUM", "DD_USE_NUM", "MAIN_RUNTIME",
    "CARRIER_MTL_USE_NUM", "GBIR_AFS2"
]

# 파일 처리
for file_name in os.listdir(input_dir):
    if file_name.endswith(".csv"):
        try:
            file_path = os.path.join(input_dir, file_name)
            df = pd.read_csv(file_path, encoding="utf-8", low_memory=False)

            # CREATE_CODE == 'FS' 필터링
            df = df[df['CREATE_CODE'] == 'FS']

            # 6300_GBIR_AFS2 열에서 NaN 값 제거
            df = df.dropna(subset=['GBIR_AFS2'])

            # EQP_ID_x 값이 지정된 리스트에 포함된 경우만 유지
            df = df[df['EQP_ID_x'].isin(valid_eqp_ids)]

            # 필요한 컬럼만 선택
            df = df[columns_to_keep]

            # 컬럼명 변경
            df = df.rename(columns={'EQP_ID_x': 'EQP_ID', 'SLOT_NO_x': 'SLOT_NO'})

            # WAF_ID 기준 중복 제거
            df = df.drop_duplicates(subset=['WAF_ID'], keep=False)

            # 파일 저장
            output_file = os.path.join(output_dir, file_name)
            df.to_csv(output_file, index=False)
            print(f"저장 완료: {output_file}")

        except Exception as e:
            print(f"파일 처리 오류: {file_name} - {e}")

print("모든 파일 정제 완료!")