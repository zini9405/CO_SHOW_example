import os
import pandas as pd
from collections import defaultdict

# 파일이 있는 디렉토리 경로 설정
directory = "const_dataset"  # 여기에 실제 디렉토리 경로 입력

# 날짜별 파일을 저장할 딕셔너리
files_grouped = defaultdict(list)

# 디렉토리에서 파일 목록 가져오기
for file in os.listdir(directory):
    if file.endswith(".csv"):  # CSV 파일만 처리
        prefix = "_".join(file.split("_")[:2])  # 날짜 부분 추출 (예: 24_01)
        files_grouped[prefix].append(file)

# 파일 병합 및 저장
for date_prefix, files in files_grouped.items():
    dataframes = []
    
    for file in files:
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path, encoding='cp949')
        dataframes.append(df)

    # 데이터 병합
    merged_df = pd.concat(dataframes, ignore_index=True)

    # 병합된 파일 저장
    output_file = os.path.join(directory, f"{date_prefix}.csv")
    merged_df.to_csv(output_file, index=False)
    print(f"저장 완료: {output_file}")

print("모든 파일 병합 완료!")


---------------------------------------------------------------------------
UnicodeDecodeError                        Traceback (most recent call last)
Cell In[3], line 23
     21 for file in files:
     22     file_path = os.path.join(directory, file)
---> 23     df = pd.read_csv(file_path, encoding='cp949')
     24     dataframes.append(df)
     26 # 데이터 병합

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\io\parsers\readers.py:1026, in read_csv(filepath_or_buffer, sep, delimiter, header, names, index_col, usecols, dtype, engine, converters, true_values, false_values, skipinitialspace, skiprows, skipfooter, nrows, na_values, keep_default_na, na_filter, verbose, skip_blank_lines, parse_dates, infer_datetime_format, keep_date_col, date_parser, date_format, dayfirst, cache_dates, iterator, chunksize, compression, thousands, decimal, lineterminator, quotechar, quoting, doublequote, escapechar, comment, encoding, encoding_errors, dialect, on_bad_lines, delim_whitespace, low_memory, memory_map, float_precision, storage_options, dtype_backend)
   1013 kwds_defaults = _refine_defaults_read(
   1014     dialect,
   1015     delimiter,
   (...)
   1022     dtype_backend=dtype_backend,
   1023 )
   1024 kwds.update(kwds_defaults)
-> 1026 return _read(filepath_or_buffer, kwds)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\io\parsers\readers.py:626, in _read(filepath_or_buffer, kwds)
    623     return parser
    625 with parser:
--> 626     return parser.read(nrows)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\io\parsers\readers.py:1923, in TextFileReader.read(self, nrows)
...
File parsers.pyx:891, in pandas._libs.parsers.TextReader._check_tokenize_status()

File parsers.pyx:2053, in pandas._libs.parsers.raise_parser_error()

UnicodeDecodeError: 'cp949' codec can't decode byte 0xeb in position 124200: illegal multibyte sequence
