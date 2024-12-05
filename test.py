import pandas as pd

# 예시 데이터
data = {
    'EQP_ID': ['E1', 'E1', 'E1', 'E2'],
    'MODULE_NAME': ['M1', 'M1', 'M2', 'M2'],
    'WAF_ID': ['W1', 'W1', 'W1', 'W2'],
    'RECIPE_ID': ['R1', 'R1', 'R1', 'R2'],
    'STEP_ID': [0, 1, 3, 0],
    'STEP_NAME': ['Step0', 'Step1', 'Step3', 'Step0'],
    'HST_REG_DTTM': ['20240101070004090000', '20240101070004090000', '20240101070004090000', '20240202080005090000'],
    'MEASURE_1': [10, 20, 30, 40],
    'MEASURE_2': [15, 25, 35, 45],
}
df = pd.DataFrame(data)

# STEP_ID 0부터 13까지 보장하도록 채우기
all_steps = list(range(14))  # 0부터 13까지의 값
grouped = []

for waf_id, group in df.groupby('WAF_ID'):
    group = group.set_index('STEP_ID')  # STEP_ID를 인덱스로 설정
    missing_steps = set(all_steps) - set(group.index)  # 누락된 STEP_ID 찾기
    for step in missing_steps:
        # 누락된 STEP_ID에 대해 값 채우기
        new_row = {
            'EQP_ID': group['EQP_ID'].iloc[0],
            'MODULE_NAME': group['MODULE_NAME'].iloc[0],
            'WAF_ID': waf_id,
            'RECIPE_ID': group['RECIPE_ID'].iloc[0],
            'STEP_ID': step,
            'STEP_NAME': f'Step{step}',
            'HST_REG_DTTM': group['HST_REG_DTTM'].iloc[0],
        }
        # 나머지 값은 -1로 채우기
        for col in df.columns:
            if col not in new_row:
                new_row[col] = -1
        group = group.append(pd.DataFrame([new_row]).set_index('STEP_ID'))
    grouped.append(group.sort_index())  # STEP_ID 순서대로 정렬

# 다시 병합
df_filled = pd.concat(grouped).reset_index()

# WAF_ID 병합
df_filled['WAF_ID'] = df_filled['WAF_ID'].astype(str).groupby(df_filled['WAF_ID']).transform('first')

# 결과 출력
print(df_filled)