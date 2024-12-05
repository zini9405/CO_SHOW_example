import os
import pyarrow.csv as pc
import pyarrow as pa
import pyarrow.parquet as pq

# wa 디렉토리 경로 지정
directory = "wa"

# wa 디렉토리 내 모든 .csv 파일 가져오기
csv_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]

# Arrow로 파일 병합
tables = []
for file in csv_files:
    print(f"Reading file: {file}")  # 진행 상황 확인
    table = pc.read_csv(file)  # 파일 읽기
    tables.append(table)

# 모든 테이블 병합
combined_table = pa.concat_tables(tables)

# 결과를 Parquet 형식으로 저장
output_file = "combined_wa.parquet"
pq.write_table(combined_table, output_file)

print(f"모든 파일이 {output_file}로 병합되었습니다.")