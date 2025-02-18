import pandas as pd
import matplotlib.pyplot as plt
import os

# CSV 파일 불러오기
df = pd.read_csv('your_file.csv', usecols=['EQP_ID', '6900_GBIR_AFS2', 'pred'])

# 저장할 폴더 생성 (없으면 생성)
output_folder = "eqp_graphs"
os.makedirs(output_folder, exist_ok=True)

# 📌 EQP_ID별 그래프 생성 및 저장
grouped = df.groupby('EQP_ID')

for eqp, data in grouped:
    plt.figure(figsize=(6, 4))
    
    # 산점도 플롯
    plt.scatter(data['6900_GBIR_AFS2'], data['pred'], color='blue', alpha=0.7, label=f'{eqp}')
    
    # Ideal Fit (y = x) 추가
    plt.plot([data['6900_GBIR_AFS2'].min(), data['6900_GBIR_AFS2'].max()],
             [data['6900_GBIR_AFS2'].min(), data['6900_GBIR_AFS2'].max()], 
             linestyle='--', color='black', label='Ideal Fit')

    # 그래프 제목 및 라벨 설정
    plt.xlabel('6900_GBIR_AFS2 (Actual)')
    plt.ylabel('pred (Predicted)')
    plt.title(f'EQP {eqp} - 6900_GBIR_AFS2 vs pred')
    plt.legend()
    plt.grid(True)
    
    # 그래프 저장
    save_path = os.path.join(output_folder, f'{eqp}_graph.png')
    plt.savefig(save_path)
    plt.close()  # 메모리 절약을 위해 그래프 닫기

print(f'✅ 각 장비별 그래프가 "{output_folder}" 폴더에 저장되었습니다.')