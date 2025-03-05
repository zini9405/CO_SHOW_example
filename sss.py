 import pandas as pd

chunk_size = 100000  # 한 번에 읽을 행 개수

for chunk in pd.read_csv("x.csv", chunksize=chunk_size):
    print(chunk.head())  # 청크 단위로 데이터를 출력 (첫 5행)
    break  # 첫 번째 청크만 출력하고 종료