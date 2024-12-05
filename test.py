import os
import pandas as pd
from collections import Counter

# wa 디렉토리 내 모든 .csv 파일 가져오기
directory = "wa"
csv_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]

# 관심 있는 STEP_NAME 목록
step_name_list = {
    'BAKE1', 'BAKE2', 'BAKE3',
    'COOL', 'COOL 1', 'COOL 2', 'COOL 3', 'COOL1', 'COOL2', 'COOL3',
    'DEPO',
    'ETCH',
    'POST PURGE', 'POST_PURGE',
    'PRE DEPO', 'PREDEPO', 'PRE_DEPO', 'Pre DEPO',
    'PRE_ETCH', 'PRE_ETCH1', 'PRE_ETCH2', 'PRE ETCH', 'PRE ETCH1',
    'PRE_VENT', 'PRE_VETN',
    'PURGE', 'PURGE 1', 'PURGE 2', 'PURGE1', 'PURGE2', 'PURGE3', 'PURGE4',
    'Poststep',
    'Prestep',
    'RAMP UP', 'RAMP_UP', 'STAB'
}

# STEP_NAME 개수 카운트
step_name_counter = Counter()

for file in csv_files:
    print(f"Processing file: {file}")  # 진행 상황 확인
    # CSV 파일 읽기
    df = pd.read_csv(file, usecols=['STEP_NAME'])
    # 관심 있는 STEP_NAME만 필터링하여 카운트
    for step_name in step_name_list:
        step_name_counter[step_name] += (df['STEP_NAME'] == step_name).sum()

# 결과 출력
for step_name, count in step_name_counter.items():
    print(f"{step_name}: {count}")

# 결과를 CSV 파일로 저장 (필요한 경우)
output_file = "step_name_counts.csv"
pd.DataFrame.from_dict(step_name_counter, orient='index', columns=['Count']).to_csv(output_file)
print(f"결과가 {output_file}에 저장되었습니다.")