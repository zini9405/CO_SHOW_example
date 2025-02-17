import pandas as pd
import pickle

# 새 데이터에 대해 동일한 scaler 사용
def standardize_new_data(new_df, scaler_path):
    # 저장된 스케일러 불러오기 (dict 형태)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    # 표준화 제외할 열
    exclude_columns = ['BASE_DT', 'EQP_ID', 'WAF_ID', '6900_GBIR_AFS2']

    # 숫자형 열 중 제외할 열을 제외한 리스트
    numerical_columns = [col for col in new_df.select_dtypes(include=['number']).columns if col not in exclude_columns]
    
    # 표준화 적용 (X_scaled = (X - mean) / scale)
    new_df_standardized = new_df.copy()
    
    for col in numerical_columns:
        if col in scaler:
            mean = scaler[col]['mean']
            scale = scaler[col]['scale']
            new_df_standardized[col] = (new_df[col] - mean) / scale  # 직접 표준화 수식 적용

    return new_df_standardized

# 사용 예시
csv_file = 'new_data.csv'
scaler_path = 'scalers.pkl'

# 데이터 불러오기
df = pd.read_csv(csv_file)

# 표준화 적용
df = standardize_new_data(df, scaler_path)

# 6900_GBIR_AFS2 NaN 제거
df = df.dropna(subset=['6900_GBIR_AFS2'])

# NaN 값 0으로 채우기
df.fillna(0, inplace=True)

# 결과 확인
print(df.head())

# 저장 (필요하면 주석 해제)
# df.to_csv('standardized_data.csv', index=False)