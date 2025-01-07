import pandas as pd
import matplotlib.pyplot as plt

# 데이터 불러오기
csv_file = 'all_minmax.csv'
df = pd.read_csv(csv_file)

# 결측치 처리 및 정렬
df = df.dropna(subset=['SFQR_AFS2', 'SFQR_AFS2_SUB'])  # 필요한 열에서 결측치 제거
df.fillna(0, inplace=True)  # 나머지 결측치는 0으로 대체
df = df.sort_values("HST_REG_DTTM")  # 시간 순으로 정렬

# 그룹별 평균 계산
grouped = df.groupby('EQP_ID_MODULE_NAME')  # EQP_ID_MODULE_NAME으로 그룹화
result = grouped['SFQR_AFS2'].agg(['mean'])  # 평균 계산

# 시각화
plt.figure(figsize=(12, 6))
result['mean'].plot(kind='bar', color='skyblue', alpha=0.7)

plt.title('Mean SFQR_AFS2 by EQP_ID_MODULE_NAME', fontsize=16)
plt.xlabel('EQP_ID_MODULE_NAME', fontsize=14)
plt.ylabel('Mean SFQR_AFS2', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=10)  # x축 라벨 각도 조정
plt.tight_layout()

# 그래프 표시
plt.show()