y_6300 = '6300_y_24_01/24_01_01_6300_6350.parquet' WAFER_ID, GBIR_AFS2
y_6900 = '6900_24_01/24_01_01_6900_6950.parquet' WAFER_ID, GBIR_AFS2
x_6300 = '24_01_x/24_01_01_6100_DSP.parquet' WAF_ID
A = GBIR_20240110_A동_Sheet1.csv WAF_ID
b = GBIR_20240110_B동_Sheet1.csv WAF_ID


나는 x_6300 파일의 기준으로 5개의 데이터를 취합하고 싶어.
x_6300의 WAF_ID와 동일한 y_6300의 WAFER_ID, y_6900의 WAFER_ID, A의 WAF_ID, B의 WAF_ID(단, 5개 WAF ID가 다 존재하는 것만 취합해줘)
그리고 y_6300, y_6900 파일에는 GBIR_AFS2만 추출해서 x_6300에 취합해줘
그리고  y_6900의 WAFER_ID에 해당하는 GBIR_AFS2는 6900_GBIR_AFS2로 이름 변경해주고  y_6300의 WAFER_ID에 해당하는 GBIR_AFS2는 6300_GBIR_AFS2로 이름 변경해줘
중요한 데이터 전처리야. 신중하고 오류없이 처리해줘.
