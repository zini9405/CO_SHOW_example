import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# CSV 파일 불러오기
df = pd.read_csv('your_file.csv', usecols=['EQP_ID', '6900_GBIR_AFS2', 'pred'])

# 📌 EQP_ID별로 그룹화
grouped = df.groupby('EQP_ID')

# 📌 R-score 및 장비 개수, 편차 계산
eqp_stats = []
max_deviation_eqp = None
max_deviation = -1

for eqp, data in grouped:
    if len(data) > 1:
        r_score = r2_score(data['6900_GBIR_AFS2'], data['pred'])
    else:
        r_score = None

    deviation = abs(data['6900_GBIR_AFS2'] - data['pred']).max()  # 최대 오차 계산
    if deviation > max_deviation:
        max_deviation = deviation
        max_deviation_eqp = eqp  # 최대 편차를 보이는 장비 저장
    
    eqp_stats.append({'EQP_ID': eqp, 'R-score': r_score, 'Count': len(data), 'Max_Deviation': deviation})

# 📌 데이터프레임 변환
eqp_stats_df = pd.DataFrame(eqp_stats)

# 📌 그래프 그리기
plt.figure(figsize=(12, 6))

for eqp, data in grouped:
    plt.scatter(data['6900_GBIR_AFS2'], data['pred'], label=f'EQP {eqp}' if eqp == max_deviation_eqp else "", alpha=0.7)

# Ideal Fit (y = x) 추가
plt.plot([df['6900_GBIR_AFS2'].min(), df['6900_GBIR_AFS2'].max()],
         [df['6900_GBIR_AFS2'].min(), df['6900_GBIR_AFS2'].max()], 
         linestyle='--', color='black', label='Ideal Fit')

# 가장 벗어난 장비만 강조하여 표시
if max_deviation_eqp:
    max_eqp_data = grouped.get_group(max_deviation_eqp)
    plt.scatter(max_eqp_data['6900_GBIR_AFS2'], max_eqp_data['pred'], color='red', label=f'Max Deviation: {max_deviation_eqp}', s=100)

plt.xlabel('6900_GBIR_AFS2 (Actual)')
plt.ylabel('pred (Predicted)')
plt.title('EQP-wise 6900_GBIR_AFS2 vs pred (Only Max Deviation Labeled)')
plt.legend()
plt.grid(True)
plt.show()

# 📌 결과 데이터프레임 출력
import ace_tools as tools
tools.display_dataframe_to_user(name="EQP Group Statistics", dataframe=eqp_stats_df)

# 📌 CSV 저장 (필요하면 주석 해제)
# eqp_stats_df.to_csv('eqp_rscore_stats.csv', index=False)