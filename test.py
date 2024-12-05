import pyarrow.csv as pc
import pyarrow.parquet as pq

# Arrow로 CSV 병합
csv_files = ["file1.csv", "file2.csv", "file3.csv"]
tables = [pc.read_csv(file) for file in csv_files]
combined_table = pa.concat_tables(tables)

# Parquet 형식으로 저장 (압축 및 병합)
pq.write_table(combined_table, "combined_waf_id.parquet")