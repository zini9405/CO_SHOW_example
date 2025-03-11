import os
import pandas as pd
import chardet
from collections import defaultdict

directory = "const_dataset"

files_grouped = defaultdict(list)

for file in os.listdir(directory):
    if file.endswith(".csv"):
        prefix = "_".join(file.split("_")[:2])
        files_grouped[prefix].append(file)

for date_prefix, files in files_grouped.items():
    dataframes = []
    
    for file in files:
        file_path = os.path.join(directory, file)
        
        # 인코딩 자동 감지
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        encoding_detected = chardet.detect(raw_data)['encoding']

        # CSV 파일 읽기
        df = pd.read_csv(file_path, encoding=encoding_detected, errors='replace')
        dataframes.append(df)

    merged_df = pd.concat(dataframes, ignore_index=True)

    output_file = os.path.join(directory, f"{date_prefix}.csv")
    merged_df.to_csv(output_file, index=False)
    print(f"저장 완료: {output_file}")

print("모든 파일 병합 완료!")