import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# CSV 파일 불러오기
df = pd.read_csv('your_file.csv', usecols=['EQP_ID', '6900_GBIR_AFS2', 'pred'])

# 📌 EQP_ID별로 그룹화
grouped = df.groupby('EQP_ID')

# 📌 R-score 및 장비 개수 계산
eqp_stats = []
for eqp, data in grouped:
    if len(data) > 1:  # 데이터가 1개 이하이면 R-score 계산 불가
        r_score = r2_score(data['6900_GBIR_AFS2'], data['pred'])
    else:
        r_score = None  # R-score 계산 불가능할 경우 None 처리
    
    eqp_stats.append({'EQP_ID': eqp, 'R-score': r_score, 'Count': len(data)})

# 📌 결과를 데이터프레임으로 변환
eqp_stats_df = pd.DataFrame(eqp_stats)

# 📌 그래프 그리기
plt.figure(figsize=(12, 6))

for eqp, data in grouped:
    plt.scatter(data['6900_GBIR_AFS2'], data['pred'], label=f'EQP {eqp}', alpha=0.7)

plt.plot([df['6900_GBIR_AFS2'].min(), df['6900_GBIR_AFS2'].max()],
         [df['6900_GBIR_AFS2'].min(), df['6900_GBIR_AFS2'].max()], 
         linestyle='--', color='black', label='Ideal Fit')

plt.xlabel('6900_GBIR_AFS2 (Actual)')
plt.ylabel('pred (Predicted)')
plt.title('EQP-wise 6900_GBIR_AFS2 vs pred')
plt.legend()
plt.grid(True)
plt.show()

# 📌 결과 출력
import ace_tools as tools
tools.display_dataframe_to_user(name="EQP Group Statistics", dataframe=eqp_stats_df)

# 📌 CSV 저장 (필요하면 주석 해제)
# eqp_stats_df.to_csv('eqp_rscore_stats.csv', index=False)