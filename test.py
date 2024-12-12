import os
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

# 디렉토리 경로 설정
directory_path = "path_to_your_directory"

# 장비별 값 범위를 저장할 리스트
device_ranges = []

# 디렉토리 내 모든 CSV 파일 처리
for file_name in os.listdir(directory_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(directory_path, file_name)
        df = pd.read_csv(file_path)
        
        if 'sfqr' in df.columns:
            # 0.5보다 큰 값 제외
            filtered_df = df[df['sfqr'] <= 0.5]
            
            if not filtered_df.empty:  # 데이터가 비어있지 않은 경우
                min_val = filtered_df['sfqr'].min()
                max_val = filtered_df['sfqr'].max()
                device_ranges.append((file_name, min_val, max_val))
            else:
                print(f"{file_name}: All values are above 0.5 after filtering. Skipped.")

# DataFrame으로 정리
range_df = pd.DataFrame(device_ranges, columns=['Device', 'Min', 'Max'])

if not range_df.empty:
    # 값 범위 계산
    range_df['Range'] = range_df['Max'] - range_df['Min']

    # 클러스터링을 위한 데이터 준비 (값 범위 사용)
    range_data = range_df[['Range']].to_numpy()

    # KMeans 클러스터링 (클러스터 개수는 조정 가능)
    kmeans = KMeans(n_clusters=3, random_state=42)
    range_df['Cluster'] = kmeans.fit_predict(range_data)

    # 클러스터별 장비 묶음 출력
    grouped_devices = range_df.groupby('Cluster')['Device'].apply(list)

    # 결과 출력
    print("Clustered Devices:")
    print(grouped_devices)

    # 결과 저장 (선택 사항)
    output_path = os.path.join(directory_path, "device_clusters_filtered.csv")
    range_df.to_csv(output_path, index=False)
    print(f"Cluster information saved to {output_path}")

    # 시각화
    plt.figure(figsize=(10, 6))
    for cluster_id in range_df['Cluster'].unique():
        cluster_data = range_df[range_df['Cluster'] == cluster_id]
        plt.scatter(cluster_data['Range'], [cluster_id] * len(cluster_data), label=f'Cluster {cluster_id}')
        for _, row in cluster_data.iterrows():
            plt.text(row['Range'], cluster_id, row['Device'], fontsize=8, ha='right')

    plt.xlabel('Range (Max - Min)')
    plt.ylabel('Cluster')
    plt.title('Device Clusters Based on sfqr Range')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("No devices remained after filtering. No clustering performed.")