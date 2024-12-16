# 정규화 
import pandas as pd
from sklearn.preprocessing import StandardScaler

# CSV 파일 읽기
df = data

# 표준화 제외할 열 정의
exclude_columns = ['SFQR_AFS2', 'SFQR_AFS2_SUB']

# 숫자형 열 중 제외할 열 제외
numerical_columns = [col for col in df.select_dtypes(include=['number']).columns if col not in exclude_columns]

df.replace(-20, float('nan'), inplace=True)

# 표준화 수행
df_standardized = df.copy()
scaler = StandardScaler()

# 열별로 최대/최소값 계산 및 10% 확장
max_min_values = df.agg(['min', 'max'])
expanded_ranges = {
    col: {
        "min": max_min_values.loc['min', col] - (max_min_values.loc['min', col]) * 0.1,
        "max": max_min_values.loc['max', col] + (max_min_values.loc['max', col]) * 0.1,
    }
    for col in numerical_columns
}

# 표준화 적용
for col in numerical_columns:
    expanded_min = expanded_ranges[col]['min']
    expanded_max = expanded_ranges[col]['max']
    
    # 범위 내에서만 표준화 수행
    mask = (df[col] >= expanded_min) & (df[col] <= expanded_max)
    standardized_values = scaler.fit_transform(df.loc[mask, [col]])
    df_standardized.loc[mask, col] = standardized_values

# 결과 저장
df_standardized.to_csv('final.csv', index=False)

# 출력: 최대/최소값과 확장된 범위
print("열별 최대값, 최소값 및 확장된 범위:")
for col in numerical_columns:
    print(f"{col}:")
    print(f"  원래 최소값: {max_min_values.loc['min', col]:.2f}, 최대값: {max_min_values.loc['max', col]:.2f}")
    print(f"  확장된 최소값: {expanded_ranges[col]['min']:.2f}, 확장된 최대값: {expanded_ranges[col]['max']:.2f}")




열별 최대값, 최소값 및 확장된 범위:
SLOT_NO:
  원래 최소값: 1.00, 최대값: 25.00
  확장된 최소값: 0.90, 확장된 최대값: 27.50
STEP_ID:
  원래 최소값: 0.00, 최대값: 12.00
  확장된 최소값: 0.00, 확장된 최대값: 13.20
AVG_ROTATION_SPEED_AT_CH_MOTIONCTRL_ROTATION_RVEL_STEP_MEAN:
  원래 최소값: 0.00, 최대값: 80.51
  확장된 최소값: 0.00, 확장된 최대값: 88.56
BLOWER_AIR_BOTTOM_PRESSURE_BOTTOM_AT_CHA_STEP_MEAN:
  원래 최소값: 416.61, 최대값: 1658.65
  확장된 최소값: 374.95, 확장된 최대값: 1824.52
BLOWER_AIR_PRESSURE_AT_CHA_STEP_MEAN:
  원래 최소값: 291.50, 최대값: 2293.40
  확장된 최소값: 262.35, 확장된 최대값: 2522.74
CURRENT_FLOW_AT_CH_GASPANEL_STICK01_MFC_RFLOW_STEP_MEAN:
  원래 최소값: 4996.70, 최대값: 100000.00
  확장된 최소값: 4497.03, 확장된 최대값: 110000.00
CURRENT_FLOW_AT_CH_GASPANEL_STICK02_MFC_RFLOW_STEP_MEAN:
  원래 최소값: 0.00, 최대값: 51875.71
  확장된 최소값: 0.00, 확장된 최대값: 57063.29
CURRENT_FLOW_AT_CH_GASPANEL_STICK03_MFC_RFLOW_STEP_MEAN:
  원래 최소값: -216.40, 최대값: 26261.34
  확장된 최소값: -194.76, 확장된 최대값: 28887.48
CURRENT_FLOW_AT_CH_GASPANEL_STICK04_MFC_RFLOW_STEP_MEAN:
  원래 최소값: -1266.00, 최대값: 11739.60
  확장된 최소값: -1139.40, 확장된 최대값: 12913.56
CURRENT_FLOW_AT_CH_GASPANEL_STICK05_MFC_RFLOW_STEP_MEAN:
  원래 최소값: -1081.71, 최대값: 5046.00
  확장된 최소값: -973.54, 확장된 최대값: 5550.60
CURRENT_FLOW_AT_CH_GASPANEL_STICK06_MFC_RFLOW_STEP_MEAN:
  원래 최소값: -3.69, 최대값: 99.84
  확장된 최소값: -3.32, 확장된 최대값: 109.83
LIFT_TORQUE_AT_CHA_MOTIONCTRL_LIFT_RTORQUE_STEP_MEAN:
  원래 최소값: -25.14, 최대값: 34.87
  확장된 최소값: -22.63, 확장된 최대값: 38.35
PRESSURE_AT_BUFFER_VACSYS_PRESSGAUGE_RPRESSURE_STEP_MEAN:
  원래 최소값: 0.00, 최대값: 791.96
  확장된 최소값: 0.00, 확장된 최대값: 871.16
PRESSURE_AT_CH_MAN1000T_RPRESSURE_STEP_MEAN:
  원래 최소값: 729.50, 최대값: 773.41
  확장된 최소값: 656.55, 확장된 최대값: 850.76
SCR_POWER_AT_CH_TEMPCTRL_HEATER_TOP_INNER_RPOWER_STEP_MEAN:
  원래 최소값: 558.00, 최대값: 33370.87
  확장된 최소값: 502.20, 확장된 최대값: 36707.95
SCR_POWER_AT_CH_TEMPCTRL_HEATER_TOP_OUTER_RPOWER_STEP_MEAN:
  원래 최소값: 0.00, 최대값: 19712.71
  확장된 최소값: 0.00, 확장된 최대값: 21683.99
SCR_POWER_AT_CH_TEMPCTRL_HEATER_BOTTOM_INNER_RPOWER_STEP_MEAN:
  원래 최소값: 0.00, 최대값: 14144.00
  확장된 최소값: 0.00, 확장된 최대값: 15558.40
SCR_POWER_AT_CH_TEMPCTRL_HEATER_BOTTOM_OUTER_RPOWER_STEP_MEAN:
  원래 최소값: 0.00, 최대값: 55771.06
  확장된 최소값: 0.00, 확장된 최대값: 61348.17
TEMPERATURE_READING_AT_CH_TEMPCTRL_HEATER_BOTTOM_PYROMETER_RTEMP_STEP_MEAN:
  원래 최소값: 300.75, 최대값: 1169.83
  확장된 최소값: 270.68, 확장된 최대값: 1286.82
TEMPERATURE_READING_AT_CH_TEMPCTRL_HEATER_EDGE_PYROMETER_RTEMP_STEP_MEAN:
  원래 최소값: 0.00, 최대값: 800.00
  확장된 최소값: 0.00, 확장된 최대값: 880.00
TEMPERATURE_READING_AT_CH_TEMPCTRL_HEATER_TOP_PYROMETER_RTEMP_STEP_MEAN:
  원래 최소값: -79.59, 최대값: 1161.02
  확장된 최소값: -71.63, 확장된 최대값: 1277.12
VP_ACCUSET_IN_STEP_MEAN:
  원래 최소값: 0.00, 최대값: 177.00
  확장된 최소값: 0.00, 확장된 최대값: 194.70
VP_ACCUSET_OUT_STEP_MEAN:
  원래 최소값: 0.00, 최대값: 300.00
  확장된 최소값: 0.00, 확장된 최대값: 330.00
VP_MULTIRUN_ORDER_STEP_MEAN:
  원래 최소값: 0.00, 최대값: 12.00
  확장된 최소값: 0.00, 확장된 최대값: 13.20
VP_RCP_CNT_STEP_MAX:
  원래 최소값: 1.00, 최대값: 1175.00
  확장된 최소값: 0.90, 확장된 최대값: 1292.50
VP_SUSCEPTORHEIGHT_STEP_MAX:
  원래 최소값: -3.50, 최대값: 2.50
  확장된 최소값: -3.15, 확장된 최대값: 2.75
VP_RCP_CNT2_STEP_MAX:
  원래 최소값: 0.00, 최대값: 1175.00
  확장된 최소값: 0.00, 확장된 최대값: 1292.50
CH_SAVED_TRAINED_EXTENDED_EXTENSION_B1_STEP_MEAN:
  원래 최소값: 0.00, 최대값: 139605.00
  확장된 최소값: 0.00, 확장된 최대값: 153565.50
CH_SAVED_TRAINED_EXTENDED_ROTATION_B1_STEP_MEAN:
  원래 최소값: 0.00, 최대값: 205400.00
  확장된 최소값: 0.00, 확장된 최대값: 225940.00
ACTUAL_SPEED_AT_CH_TEMPCTRL_HEATER_BOTTOM_VSB_RSPEED_STEP_MEAN:
  원래 최소값: 88.40, 최대값: 100.00
  확장된 최소값: 79.56, 확장된 최대값: 110.00
ACTUAL_SPEED_AT_CH_TEMPCTRL_HEATER_TOP_VSB_RSPEED_STEP_MEAN:
  원래 최소값: 54.99, 최대값: 100.00
  확장된 최소값: 49.49, 확장된 최대값: 110.00


다시 원래값으로 복원할 수 있는 코드 구현해줘.
