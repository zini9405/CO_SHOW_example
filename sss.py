import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv('all.csv')

# 각 EQP_ID_MODULE_NAME 별 고유 RECIPE_ID 개수 계산
eqp_recipe_counts = df.groupby('EQP_ID_MODULE_NAME')['RECIPE_ID'].nunique()

# 결과 출력
print(eqp_recipe_counts)

# CSV로 저장 (필요하면 주석 해제)
# eqp_recipe_counts.to_csv('eqp_recipe_counts.csv', header=True)