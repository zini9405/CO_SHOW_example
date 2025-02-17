import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv('all.csv')

# 1️⃣ STEP_ID == 6 필터링
df = df[df['STEP_ID'] == 6]

# 2️⃣ CREATE_CODE == 'FS' 필터링
df = df[df['CREATE_CODE'] == 'FS']

# 3️⃣ 6300_GBIR_AFS2 열에서 NaN 값 제거
df = df.dropna(subset=['6300_GBIR_AFS2'])

# 4️⃣ 필요한 열만 선택
columns_to_keep = [
    'BASE_DT', 'EQP_ID_x', 'SLOT_NO_x', 'RECIPE_ID',
    'INTERNLA_GEAR_RPM_ACTUAL_STEP_MEAN', 'PAD_TEMP_STEP_MEAN',
    'RING_GEAR_MOTOR_CURRENT_STEP_MEAN', 'SLURRY_1_FLOW_STEP_MEAN',
    'SLURRY_IN_TEMP_STEP_MEAN', 'SUN_GEAR_MOTOR_CURRENT_STEP_MEAN',
    'SUN_GEAR_RPM_ACTUAL_STEP_MEAN', 'SURFACTANT_FLOW_ACTUAL_STEP_MEAN',
    'PRS_PRES_ACTUAL__STEP_MEAN', 'UPPER_COOLING_IN_TEMP_STEP_MEAN',
    'UPPER_COOLING_OUT_TEMP_STEP_MEAN', 'UPPER_COOLING_FLOW_STEP_MEAN',
    'UPPER_MOTOR_CURRENT_STEP_MEAN', 'UPPER_RPM_ACTUAL_STEP_MEAN',
    'LOWER_COOLING_IN_TEMP_STEP_MEAN', 'LOWER_COOLING_OUT_TEMP_STEP_MEAN',
    'LOWER_COOLING_FLOW_STEP_MEAN', 'LOWER_MOTOR_CURRENT_STEP_MEAN',
    'LOWER_RPM_ACTUAL_STEP_MEAN', 'PRS_PRES_ACTUAL__STEP_COUNT',
    'PAD_COUNT', 'SLURRY_USE_NUM', 'DD_USE_NUM', 'MAIN_RUNTIME',
    'CARRIER_MTL_USE_NUM', '6300_GBIR_AFS2'
]

df = df[columns_to_keep]

# 5️⃣ 컬럼명 변경 (EQP_ID_x → EQP_ID, SLOT_NO_x → SLOT_NO)
df.rename(columns={'EQP_ID_x': 'EQP_ID', 'SLOT_NO_x': 'SLOT_NO'}, inplace=True)

# 결과 확인
print(df.head())

# CSV 저장 (필요하면 주석 해제)
# df.to_csv('filtered_data.csv', index=False)