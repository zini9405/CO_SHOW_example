import pandas as pd

# 파일 불러오기
y_6300 = pd.read_csv('6300_y_24_01_combined.csv', columns=['WAFER_ID', 'GBIR_AFS2'])
y_6900 = pd.read_csv('6900_24_01_combined.csv', columns=['WAFER_ID', 'GBIR_AFS2'])
x_6300 = pd.read_csv('24_01_x_combined.csv')
A = pd.read_csv('dataset/GBIR_20240110_A동_Sheet1.csv', usecols=['WAF_ID'])
B = pd.read_csv('dataset/GBIR_20240110_B동_Sheet1.csv', usecols=['WAF_ID'])

# 컬럼 이름 변경
y_6300.rename(columns={'GBIR_AFS2': '6300_GBIR_AFS2'}, inplace=True)
y_6900.rename(columns={'GBIR_AFS2': '6900_GBIR_AFS2'}, inplace=True)

# 컬럼명 통일 (WAFER_ID → WAF_ID)
y_6300.rename(columns={'WAFER_ID': 'WAF_ID'}, inplace=True)
y_6900.rename(columns={'WAFER_ID': 'WAF_ID'}, inplace=True)

# 5개 데이터셋을 기준으로 WAF_ID가 모두 존재하는 값만 선택
merged_df = (
    x_6300[['WAF_ID']]
    .merge(y_6300, on='WAF_ID', how='inner')
    .merge(y_6900, on='WAF_ID', how='inner')
    .merge(A, on='WAF_ID', how='inner')
    .merge(B, on='WAF_ID', how='inner')
)

# 결과 확인
print(merged_df.head())

# CSV 저장 (필요하면 주석 해제)
# merged_df.to_csv('merged_data.csv', index=False)

---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[40], line 4
      1 import pandas as pd
      3 # 파일 불러오기
----> 4 y_6300 = pd.read_csv('6300_y_24_01_combined.csv', columns=['WAFER_ID', 'GBIR_AFS2'])
      5 y_6900 = pd.read_csv('6900_24_01_combined.csv', columns=['WAFER_ID', 'GBIR_AFS2'])
      6 x_6300 = pd.read_csv('24_01_x_combined.csv')

TypeError: read_csv() got an unexpected keyword argument 'columns'
