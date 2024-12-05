import pandas as pd
import os

# STEP 순서 정의
step_order = {
    0: 'Prestep',
    1: 'PURGE',
    2: 'RAMP_UP',
    3: 'BAKE1',
    4: 'BAKE2',
    5: 'PRE_ETCH',
    6: 'PRE_DEPO',
    7: 'DEPO',
    8: 'POST_PURGE',
    9: 'COOL1',
    10: 'COOL2',
    11: 'COOL3',
    12: 'Poststep'
}

# 불필요한 STEP_NAME 목록
exclude_step_names = {
    'BAKE3', 'COOL', 'COOL 1', 'COOL 2', 'COOL 3', 
    'PURGE 1', 'PURGE 2', 'PURGE1', 'PURGE2', 'PURGE3', 'PURGE4', 
    'STAB'
}

# STEP_NAME 수정 매핑
rename_map = {
    'POST PURGE': 'POST_PURGE',
    'PRE DEPO': 'PRE_DEPO',
    'PREDEPO': 'PRE_DEPO',
    'Pre DEPO': 'PRE_DEPO',
    'PRE_VENT': 'PRE_DEPO',
    'PRE_VETN': 'PRE_DEPO',
    'PRE ETCH': 'PRE_ETCH',
    'PRE ETCH1': 'PRE_ETCH',
    'PRE ETCH2': 'PRE_ETCH',
    'ETCH': 'PRE_ETCH',
    'RAMP UP': 'RAMP_UP'
}

# 예시 데이터 로드 (wa 디렉토리의 CSV 파일 병합)
directory = "wa"
csv_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]
df = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

# 1. WAF_ID 열로 그룹화
grouped = df.groupby('WAF_ID')

# 결과를 저장할 리스트
processed_groups = []

for waf_id, group in grouped:
    # 2. 불필요한 STEP_NAME 포함된 그룹 삭제
    if group['STEP_NAME'].isin(exclude_step_names).any():
        continue  # 그룹 제외
    
    # 3. STEP_NAME 수정
    group['STEP_NAME'] = group['STEP_NAME'].replace(rename_map)
    
    # 4. STEP 순서 보장 (0~12 값 채우기)
    missing_steps = set(step_order.keys()) - set(group['STEP_ID'])
    for step in missing_steps:
        new_row = {
            'STEP_ID': step,
            'STEP_NAME': step_order[step],
            'EQP_ID': group['EQP_ID'].iloc[0],
            'MODULE_NAME': group['MODULE_NAME'].iloc[0],
            'WAF_ID': group['WAF_ID'].iloc[0],
            'RECIPE_ID': group['RECIPE_ID'].iloc[0],
            'HST_REG_DTTM': group['HST_REG_DTTM'].iloc[0],
        }
        # 나머지 열을 -20으로 채우기
        for col in group.columns:
            if col not in new_row:
                new_row[col] = -20
        group = pd.concat([group, pd.DataFrame([new_row])], ignore_index=True)
    
    # STEP_ID 순서대로 정렬
    group = group.sort_values(by='STEP_ID').reset_index(drop=True)
    processed_groups.append(group)

# 5. 그룹을 하나로 합치기
final_df = pd.concat(processed_groups, ignore_index=True)

# 결과 저장
final_df.to_csv("processed_data.csv", index=False)
print("결과가 'processed_data.csv'에 저장되었습니다.")