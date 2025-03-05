 import pandas as pd

# 원본 CSV 파일명
input_file = "x.csv"
output_prefix = "split_x_"  # 저장할 파일명 접두사
chunk_size = 100000  # 한 번에 읽을 행 개수 (조절 가능)

# CSV를 청크 단위로 읽고 저장
for i, chunk in enumerate(pd.read_csv(input_file, chunksize=chunk_size)):
    output_file = f"{output_prefix}{i+1}.csv"  # 파일명: split_x_1.csv, split_x_2.csv, ...
    chunk.to_csv(output_file, index=False)  # 각 청크를 별도 파일로 저장
    print(f"저장 완료: {output_file}")

print("모든 청크 저장 완료!")