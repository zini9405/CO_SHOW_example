import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# CSV 파일 로드
df = pd.read_csv("dff.csv")

# predictions과 true_labels 컬럼 확인
if 'predictions' not in df.columns or 'true_labels' not in df.columns:
    raise ValueError("CSV 파일에 'predictions' 또는 'true_labels' 컬럼이 없습니다.")

# 데이터 나누기
chunk_size = 1000  # 1000개씩 나눔
num_chunks = int(np.ceil(len(df) / chunk_size))  # 총 구간 개수

# 구간별 그래프 그리기
for i in range(num_chunks):
    start_idx = i * chunk_size
    end_idx = min((i + 1) * chunk_size, len(df))

    chunk = df.iloc[start_idx:end_idx]  # 특정 구간 선택

    plt.figure(figsize=(10, 5))
    plt.plot(chunk.index, chunk['predictions'], marker='o', linestyle='-', label="Predictions")
    plt.plot(chunk.index, chunk['true_labels'], marker='s', linestyle='--', label="True Labels")

    plt.xlabel("Sample Index")
    plt.ylabel("Value")
    plt.title(f"Predictions vs True Labels (Chunk {i+1}/{num_chunks})")
    plt.legend()
    plt.grid(True)
    plt.show()