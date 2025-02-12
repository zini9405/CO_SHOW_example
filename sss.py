import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv('all.csv')

# EQP_ID_MODULE_NAME 열의 고유값 및 개수 계산
eqp_counts = df['EQP_ID_MODULE_NAME'].value_counts()

# 결과 출력
print(eqp_counts)

# CSV로 저장 (필요하면 주석 해제)
# eqp_counts.to_csv('eqp_id_module_name_counts.csv', header=True)