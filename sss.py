import os
import pandas as pd
from tqdm import tqdm  # 진행률 표시

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
    "CARRIER_MTL_USE_NUM", "GBIR_AFS2", "step"
]

# 필터링할 step 값
valid_steps = {2, 3, 4, 6, 7}

# 파일 처리
for file_name in tqdm(os.listdir(input_dir), desc="파일 처리 진행"):
    if file_name.endswith(".csv"):
        try:
            file_path = os.path.join(input_dir, file_name)
            df = pd.read_csv(file_path, encoding="utf-8", dtype=str, low_memory=False)

            # 실제 존재하는 컬럼 확인
            actual_columns = df.columns.tolist()

            # CREATE_CODE == 'FS' 필터링
            if "CREATE_CODE" in df.columns:
                df = df[df['CREATE_CODE'] == 'FS']

            # 6300_GBIR_AFS2 열에서 NaN 값 제거
            if "GBIR_AFS2" in df.columns:
                df = df.dropna(subset=['GBIR_AFS2'])

            # EQP_ID_x 값이 지정된 리스트에 포함된 경우만 유지
            if "EQP_ID_x" in df.columns:
                df = df[df['EQP_ID_x'].isin(valid_eqp_ids)]
            else:
                print(f"[경고] {file_name}: 'EQP_ID_x' 컬럼 없음, 필터링 건너뜀.")

            # step 값이 문자이므로 숫자로 변환
            if "step" in df.columns:
                df["step"] = pd.to_numeric(df["step"], errors="coerce")  # 변환 불가능한 값 NaN 처리
            else:
                print(f"[경고] {file_name}: 'step' 컬럼 없음, 필터링 건너뜀.")

            # WAF_ID별 step 값이 {2, 3, 4, 6, 7}만 포함하는 경우만 유지
            if "WAF_ID" in df.columns and "step" in df.columns:
                waf_group = df.groupby("WAF_ID")["step"].apply(set)  # WAF_ID별 step 값 집합 생성

                # 올바른 WAF_ID 선택 (valid_steps만 포함하고, 다른 값(예: 5)이 없을 것)
                valid_waf_ids = waf_group[(waf_group.apply(lambda x: x.issubset(valid_steps))) & 
                                          (waf_group.apply(lambda x: x >= valid_steps))].index

                df = df[df["WAF_ID"].isin(valid_waf_ids)]
            else:
                print(f"[경고] {file_name}: 'WAF_ID' 또는 'step' 컬럼 없음, 필터링 건너뜀.")

            # 필요한 컬럼만 선택 (실제 존재하는 컬럼만 유지)
            selected_columns = [col for col in columns_to_keep if col in actual_columns]
            df = df[selected_columns]

            # 컬럼명 변경
            rename_dict = {"EQP_ID_x": "EQP_ID", "SLOT_NO_x": "SLOT_NO"}
            rename_dict = {k: v for k, v in rename_dict.items() if k in actual_columns}  # 존재하는 컬럼만 변경
            df = df.rename(columns=rename_dict)

            # WAF_ID 기준 중복 제거
            if "WAF_ID" in df.columns:
                df = df.drop_duplicates(subset=['WAF_ID'], keep=False)

            # 파일 저장
            output_file = os.path.join(output_dir, file_name)
            df.to_csv(output_file, index=False)
            print(f"저장 완료: {output_file}")

        except Exception as e:
            print(f"파일 처리 오류: {file_name} - {e}")

print("모든 파일 정제 완료!")