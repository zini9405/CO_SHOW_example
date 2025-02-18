import pandas as pd
import matplotlib.pyplot as plt
import os

# CSV 파일 불러오기
df = pd.read_csv('your_file.csv', usecols=['EQP_ID', '6900_GBIR_AFS2', 'pred'])

# 저장할 폴더 생성 (없으면 생성)
output_folder = "eqp_trend_graphs"
os.makedirs(output_folder, exist_ok=True)

# 📌 EQP_ID별 그래프 생성 및 저장
grouped = df.groupby('EQP_ID')

for eqp, data in grouped:
    plt.figure(figsize=(6, 4))

    # X축을 정렬된 인덱스로 설정 (시간 흐름이 없으므로 순서대로)
    x_values = range(len(data))

    # 6900_GBIR_AFS2 (실제값) 점선 그래프
    plt.plot(x_values, data['6900_GBIR_AFS2'], linestyle='--', marker='o', color='blue', label='Actual')

    # pred (예측값) 점선 그래프
    plt.plot(x_values, data['pred'], linestyle='--', marker='x', color='red', label='Predicted')

    # 그래프 제목 및 라벨 설정
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title(f'EQP {eqp} - Actual vs Predicted')
    plt.legend()
    plt.grid(True)

    # 그래프 저장
    save_path = os.path.join(output_folder, f'{eqp}_trend.png')
    plt.savefig(save_path)
    plt.close()  # 메모리 절약을 위해 그래프 닫기

print(f'✅ 각 장비별 트렌드 그래프가 '{output_folder}' 폴더에 저장되었습니다.")