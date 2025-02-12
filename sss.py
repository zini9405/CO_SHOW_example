import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv('all.csv')

# 각 EQP_ID_MODULE_NAME별 각 RECIPE_ID의 개수 계산
eqp_recipe_counts = df.groupby(['EQP_ID_MODULE_NAME', 'RECIPE_ID']).size().reset_index(name='COUNT')

# 결과 출력
print(eqp_recipe_counts)

# CSV로 저장 (필요하면 주석 해제)
# eqp_recipe_counts.to_csv('eqp_recipe_counts.csv', index=False)