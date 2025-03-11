100%|██████████| 31/31 [00:01<00:00, 15.87it/s]
100%|██████████| 29/29 [00:01<00:00, 15.27it/s]
100%|██████████| 30/30 [00:01<00:00, 15.01it/s]
100%|██████████| 30/30 [00:02<00:00, 13.53it/s]
100%|██████████| 31/31 [00:02<00:00, 13.78it/s]
100%|██████████| 30/30 [00:02<00:00, 13.04it/s]
100%|██████████| 31/31 [00:02<00:00, 13.09it/s]
100%|██████████| 31/31 [00:02<00:00, 12.73it/s]
100%|██████████| 30/30 [00:02<00:00, 13.42it/s]
100%|██████████| 31/31 [00:02<00:00, 11.85it/s]
100%|██████████| 30/30 [00:02<00:00, 11.75it/s]
100%|██████████| 31/31 [00:02<00:00, 11.78it/s]
100%|██████████| 27/27 [00:02<00:00, 12.65it/s]
100%|██████████| 26/26 [00:02<00:00, 12.18it/s]
100%|██████████| 14/14 [01:39<00:00,  7.09s/it]
100%|██████████| 31/31 [00:00<00:00, 256.26it/s]
병합된 데이터 개수: 8981
  ETL_FLAG FAB_ID OPER_ID   EQP_NM START_EVENT_NM       ST_DTTM       ED_DTTM  \
0      MMS    WFB          ESSSM01            CBM  202401010240  202401010700   
1      MMS  EPIG5            ADE05            MBM  202401010430  202401011240   
2      MMS    ETC          GR3 All             점검  202401011500  202401011600   
3      MMS    WF7          TEAFS02            MBM  202401011800  202401011830   
4      MMS    WF7           TPEP01             BM  202401012200  202401012240   

                                           WORK_DESC  \
0  1) Robot Lower Arm Aligner Wafer Pick-Up 하지 않고...   
1  1.Robot Reset, Calibration --> N.G(Motion Erro...   
2                           1. Grower 현장 일일 Local 점검   
3  1.T/P 이용하여 Wafer Recovery.\n2.All PC Rebooting...   
4  1.Slurry PH Cal 실시.\n2.Slurry Tank H Level Sen...   

                                    DESCRIPTION  \
0                           Error 없이 Holding 발생   
1                 R, T, Z-Axis Motion Error 발생.   
2                         Grower 현장 일일 Local 점검   
3                             Error 없이 Holding.   
4  Slurry PH Alarm, Slurry Tank Level Alarm 발생.   

                                                 CHK       REPAIR_DESC  \
0                                         [M11] 구동불량       [M61] RESET   
1                                      R-axis 문제 추정.         [BM07] 교체   
...
1  20241118154612  20240101  
2  20241118154612  20240101  
3  20241118154612  20240101  
4  20241118154612  20240101  
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...

100%|██████████| 31/31 [00:36<00:00,  1.18s/it]
100%|██████████| 29/29 [00:35<00:00,  1.23s/it]
100%|██████████| 31/31 [00:40<00:00,  1.31s/it]
100%|██████████| 30/30 [00:41<00:00,  1.38s/it]
100%|██████████| 31/31 [00:44<00:00,  1.45s/it]
100%|██████████| 30/30 [00:46<00:00,  1.56s/it]
100%|██████████| 31/31 [00:47<00:00,  1.52s/it]
100%|██████████| 31/31 [00:46<00:00,  1.51s/it]
100%|██████████| 30/30 [00:44<00:00,  1.48s/it]
100%|██████████| 31/31 [00:46<00:00,  1.49s/it]
100%|██████████| 30/30 [00:47<00:00,  1.59s/it]]
100%|██████████| 31/31 [00:47<00:00,  1.54s/it]]
100%|██████████| 31/31 [00:47<00:00,  1.53s/it]]
100%|██████████| 26/26 [00:40<00:00,  1.56s/it]]
100%|██████████| 14/14 [52:25<00:00, 224.66s/it]
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\24_02.csv.csv
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\24_02.csv
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\24_03.csv.csv
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\24_03.csv
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\24_04.csv.csv
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\24_04.csv
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (22,25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\24_05.csv
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\24_06.csv
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\24_07.csv
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\24_08.csv
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (22,25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\24_09.csv
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\24_10.csv
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\24_11.csv
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (22,25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\24_12.csv
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\25_01.csv
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\3700107572.py:27: DtypeWarning: Columns (22,25) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(file_path, encoding=encoding_detected, encoding_errors='replace')
저장 완료: const_dataset\25_02.csv
모든 파일 병합 완료!
  7%|▋         | 1/14 [00:03<00:46,  3.54s/it]
파일 처리 오류: 24_07.csv - "['EQP_ID_6100'] not in index"
 14%|█▍        | 2/14 [00:05<00:32,  2.70s/it]
파일 처리 오류: 24_02.csv - "['EQP_ID_6100'] not in index"
 21%|██▏       | 3/14 [00:08<00:30,  2.76s/it]
파일 처리 오류: 24_05.csv - "['EQP_ID_6100'] not in index"
 29%|██▊       | 4/14 [00:10<00:25,  2.59s/it]
파일 처리 오류: 24_03.csv - "['EQP_ID_6100'] not in index"
 36%|███▌      | 5/14 [00:14<00:26,  2.97s/it]
파일 처리 오류: 24_11.csv - "['EQP_ID_6100'] not in index"
 43%|████▎     | 6/14 [00:17<00:23,  2.94s/it]
파일 처리 오류: 24_09.csv - "['EQP_ID_6100'] not in index"
 43%|████▎     | 6/14 [01:04<01:26, 10.82s/it]
---------------------------------------------------------------------------
KeyboardInterrupt                         Traceback (most recent call last)
Cell In[30], line 28
     25 df_6300_filtered = df_6300[['EQP_ID_6100', 'EQP_NM_6100', 'SUBLOT_ID_6100', 'WAFER_ID', 'GBIR_AFS2']]
     27 # 6100_process 데이터 로드
---> 28 df_6100 = pd.read_csv(os.path.join(dir_6100, file_name), encoding="utf-8", low_memory=False)
     30 # 6100_process와 6300_process 병합 (WAF_ID == WAFER_ID)
     31 com_x = df_6100.merge(df_6300_filtered, left_on="SUBLOT_ID", right_on="SUBLOT_ID_6100", how="inner")

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
   1171 
   1172     """
   1173     return (a, mask, values)

KeyboardInterrupt: 
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
  0%|          | 0/14 [00:00<?, ?it/s]
324614
255068
146800
146800
146800
  7%|▋         | 1/14 [00:03<00:45,  3.52s/it]
저장 완료: merged_dataset_process_cleaned1\24_01.csv
345371
247075
141584
141584
141584
 14%|█▍        | 2/14 [00:06<00:41,  3.42s/it]
저장 완료: merged_dataset_process_cleaned1\24_02.csv
335416
264469
140364
140364
140364
 21%|██▏       | 3/14 [00:10<00:37,  3.43s/it]
저장 완료: merged_dataset_process_cleaned1\24_03.csv
426896
270907
153931
153931
153931
 29%|██▊       | 4/14 [00:14<00:37,  3.75s/it]
저장 완료: merged_dataset_process_cleaned1\24_04.csv
450648
339685
181011
181011
181011
 36%|███▌      | 5/14 [00:19<00:37,  4.15s/it]
저장 완료: merged_dataset_process_cleaned1\24_05.csv
471900
359119
182207
182207
182207
 43%|████▎     | 6/14 [00:24<00:34,  4.33s/it]
저장 완료: merged_dataset_process_cleaned1\24_06.csv
518762
367969
198657
198657
198657
 50%|█████     | 7/14 [00:29<00:32,  4.62s/it]
저장 완료: merged_dataset_process_cleaned1\24_07.csv
504878
356848
182855
182855
182855
 57%|█████▋    | 8/14 [00:34<00:28,  4.79s/it]
저장 완료: merged_dataset_process_cleaned1\24_08.csv
420171
316737
157590
157590
157590
 64%|██████▍   | 9/14 [00:38<00:23,  4.71s/it]
저장 완료: merged_dataset_process_cleaned1\24_09.csv
623969
370089
192377
192377
192377
 71%|███████▏  | 10/14 [00:45<00:20,  5.12s/it]
저장 완료: merged_dataset_process_cleaned1\24_10.csv
504248
341546
166697
166697
166697
 79%|███████▊  | 11/14 [00:50<00:15,  5.12s/it]
저장 완료: merged_dataset_process_cleaned1\24_11.csv
506184
420308
179384
179384
179384
 86%|████████▌ | 12/14 [00:55<00:10,  5.20s/it]
저장 완료: merged_dataset_process_cleaned1\24_12.csv
389262
297663
129304
129304
129304
 93%|█████████▎| 13/14 [00:59<00:04,  4.85s/it]
저장 완료: merged_dataset_process_cleaned1\25_01.csv
389243
295606
128645
128645
128645
100%|██████████| 14/14 [01:03<00:00,  4.53s/it]
저장 완료: merged_dataset_process_cleaned1\25_02.csv
모든 파일 정제 완료!

  7%|▋         | 1/14 [00:03<00:43,  3.35s/it]
파일 처리 오류: 24_07.csv - "['EQP_ID_6100'] not in index"
 14%|█▍        | 2/14 [00:05<00:31,  2.65s/it]
파일 처리 오류: 24_02.csv - "['EQP_ID_6100'] not in index"
 21%|██▏       | 3/14 [00:08<00:30,  2.73s/it]
파일 처리 오류: 24_05.csv - "['EQP_ID_6100'] not in index"
 29%|██▊       | 4/14 [00:10<00:25,  2.55s/it]
파일 처리 오류: 24_03.csv - "['EQP_ID_6100'] not in index"
 36%|███▌      | 5/14 [00:14<00:26,  2.93s/it]
파일 처리 오류: 24_11.csv - "['EQP_ID_6100'] not in index"
 43%|████▎     | 6/14 [00:16<00:22,  2.86s/it]
파일 처리 오류: 24_09.csv - "['EQP_ID_6100'] not in index"
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\2862276932.py:27: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  df_6300_filtered.rename(columns={'EQP_ID_6100': 'EQP_ID'}, inplace=True)
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_20260\2862276932.py:30: SettingWithCopyWarning: 
A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  df_6300_filtered.rename(columns={'WAFER_ID': 'WAF_ID'}, inplace=True)
