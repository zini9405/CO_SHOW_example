import pandas as pd
import numpy as np

# CSV 파일 로드
df = pd.read_csv("dataset_ver3.csv")

columns_to_extract = [
    'ANALYSIS_GROUP', 'SUBLOT', 'WAFER_ID', 'EQP_NM', 'DATE',
    "PROCESS-RAMP_UP-TEMP","STEP_TIME_RMS_PROC","PROCESS-RAMP_UP-TEMP","PROCESS-BAKE1-TEMP","PROCESS-COOL2-SLIT_H2",
    "PROCESS-DEPO-MULTIRUN_SET","PROCESS-COOL1-SLIT_H2","PROCESS-COOL3-SLIT_H2","PROCESS-DEPO-WITH_TEMP","PROCESS-DEPO-XFER_POWER",
    "PROCESS-POST_PURGE-SLIT_H2","PROCESS-DEPO-ACTIVE_POWER","PROCESS-BAKE2-TEMP","PROCESS-PRE_VENT-MAIN_H2","PROCESS-PRE_VENT-TEMP",
    "CLEAN-BAKE-MAIN_H2","CLEAN-PRE_VENT-TEMP","CLEAN-PURGE-SLIT_H2","CLEAN-RAMP_UP-MAIN_H2","CLEAN-PRE_VENT-MAIN_H2",
    "CLEAN-COOL-MAIN_H2","CLEAN-ETCH-MAIN_H2","CLEAN-RAMP_UP-TEMP","CLEAN-BAKE-TEMP","CLEAN-COOL-SLIT_H2","CLEAN-PURGE-MAIN_H2",
    "CLEAN-ETCH-TEMP","CLEAN-POST_PURGE-SLIT_H2","CLEAN-POST_PURGE-MAIN_H2","CLEAN-ETCH-SLIT_H2","CLEAN-RAMP_UP-SLIT_H2",'Delta_SFQR'
]
columns_to_extract = list(dict.fromkeys(columns_to_extract))  # 중복 제거

df_extracted = df[[col for col in columns_to_extract if col in df.columns]]

text_columns = ['ANALYSIS_GROUP', 'SUBLOT', 'WAFER_ID', 'EQP_NM', 'DATE']

# 문자열 컬럼 결측치 처리
for col in text_columns:
    if col in df_extracted.columns:
        df_extracted[col] = df_extracted[col].fillna("Unknown")

# 결측값을 채우는 함수
def fill_missing_values(series):
    values = series.values.copy()
    for i in range(len(values)):
        if pd.isna(values[i]):
            prev_idx = i - 1
            while prev_idx >= 0 and pd.isna(values[prev_idx]):
                prev_idx -= 1
            next_idx = i + 1
            while next_idx < len(values) and pd.isna(values[next_idx]):
                next_idx += 1

            if prev_idx >= 0 and next_idx < len(values) and not pd.isna(values[next_idx]):
                values[i] = (values[prev_idx] + values[next_idx]) / 2
            else:
                values[i] = np.nanmean(values)
    return pd.Series(values, index=series.index)

# 그룹 내에서 결측치 채우기
def fill_group(group):
    for col in group.columns:
        if col not in ['ANALYSIS_GROUP', 'EQP_NM'] and group[col].dtype != 'object':
            if group[col].isnull().any():
                group[col] = fill_missing_values(group[col])
    return group

# 그룹화 적용
df_filled = df_extracted.groupby(['ANALYSIS_GROUP', 'EQP_NM'], group_keys=False).apply(fill_group)

# 결과 저장
df_filled.to_csv("filled_dataset.csv", index=False)