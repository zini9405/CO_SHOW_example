import pandas as pd
import os
from tqdm import tqdm

output_dir_path = 'C:/Users/SKsiltron/Desktop/SFQR/wafer_id_1'

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

# 데이터프레임 로드 (df는 기존 데이터로부터 가져와야 함)
df = data  # 기존에 정의된 data를 사용해야 함

# 1. WAF_ID 열로 그룹화
grouped = df.groupby('WAF_ID')

# 결과를 저장할 리스트
processed_groups = []

for waf_id, group in tqdm(grouped, desc="Processing Groups"):
    # 2. 불필요한 STEP_NAME 포함된 그룹 삭제
    if group['STEP_NAME'].isin(exclude_step_names).any():
        continue  # 그룹 제외
    
    # 3. STEP_NAME 수정
    group['STEP_NAME'] = group['STEP_NAME'].replace(rename_map)
    
    # 4. STEP 순서 보장 (0~12 값 채우기)
    group['STEP_ID'] = group['STEP_ID'].astype(int)  # STEP_ID를 숫자로 변환
    existing_steps = set(group['STEP_ID'])
    missing_steps = set(step_order.keys()) - existing_steps
    
    # 누락된 STEP_ID 추가
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
    group = group.sort_values(by='STEP_ID', key=lambda x: x.astype(int)).reset_index(drop=True)
    processed_groups.append(group)

# 각 그룹을 개별 파일로 저장
for group in tqdm(processed_groups, desc="Saving Groups"):
    name = group.iloc[0]['WAF_ID']
    output_file_path = os.path.join(output_dir_path, f'{name}.csv')
    group.to_csv(output_file_path, index=False)

# 5. 그룹을 하나로 합치기
final_df = pd.concat(processed_groups, ignore_index=True)

# 결과 저장
final_df.to_csv("processed_data.csv", index=False)
print("결과가 'processed_data.csv'에 저장되었습니다.")