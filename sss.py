import pandas as pd
import matplotlib.pyplot as plt
import os

# CSV 파일 불러오기
df = pd.read_csv('your_file.csv', usecols=['EQP_ID', '6900_GBIR_AFS2', 'pred'])

# 저장할 폴더 생성 (없으면 생성)
output_folder = "eqp_comparison_graphs"
os.makedirs(output_folder, exist_ok=True)

# 📌 EQP_ID별 그래프 생성 및 저장
grouped = df.groupby('EQP_ID')

# 새로운 비교 그래프 생성
plt.figure(figsize=(10, 6))

# 각 장비 데이터를 같은 그래프에 표시
for eqp, data in grouped:
    plt.scatter(data['6900_GBIR_AFS2'], data['pred'], label=eqp, alpha=0.7)

# Ideal Fit (y = x) 추가
plt.plot([df['6900_GBIR_AFS2'].min(), df['6900_GBIR_AFS2'].max()],
         [df['6900_GBIR_AFS2'].min(), df['6900_GBIR_AFS2'].max()], 
         linestyle='--', color='black', label='Ideal Fit')

# 그래프 제목 및 라벨 설정
plt.xlabel('6900_GBIR_AFS2 (Actual)')
plt.ylabel('pred (Predicted)')
plt.title('Comparison of EQP_ID - 6900_GBIR_AFS2 vs pred')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))  # 범례를 그래프 바깥쪽으로
plt.grid(True)
plt.tight_layout()

# 그래프 저장
save_path = os.path.join(output_folder, 'eqp_comparison_graph.png')
plt.savefig(save_path)
plt.close()  # 메모리 절약을 위해 그래프 닫기

print(f'✅ EQP 비교 그래프가 "{output_folder}" 폴더에 저장되었습니다.')