import pandas as pd

# 원본 CSV 파일명
input_file = "FDC_Y.csv"
output_prefix = "final/split_x_"  # 저장할 파일명 접두사
chunk_size = 100000  # 한 번에 읽을 행 개수 (조절 가능)

df_b = pd.read_csv("filtered_const_data.csv")

# CSV를 청크 단위로 읽고 저장
for i, chunk in enumerate(pd.read_csv(input_file, chunksize=chunk_size)):
    chunk = chunk.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'index'])
    output_file = f"{output_prefix}{i+1}.csv"  
    merged_df = df_b.merge(chunk, on="SUBLOT_ID", how="outer")
    merged_df.to_csv(output_file, index=False)
    print(f"저장 완료: {output_file}")

print("모든 청크 저장 완료!")


이 코드에서     merged_df = df_b.merge(chunk, on="SUBLOT_ID", how="outer") 두 조건이 맞는 행만 저장하는 코드로 수정해줘
