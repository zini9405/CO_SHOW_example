import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

# 데이터 로드
df = pd.read_csv('all.csv')  # 학습 데이터 파일

# 표준화 제외할 열 정의
exclude_columns = ['SFQR_AFS2', 'ESFQR2_MAX_AFS2', 'ZDDFRONTMEAN_01_AFS2', 'ESFQD_ZONE1MEAN_AFS2', 'ESFQD_ZONE1MAX_AFS2', 'ESFQD2_ZONE1MEAN_AFS2', 'ESFQD2_ZONE1MAX_AFS2',
                   'SFQR_AFS2_SUB', 'ESFQR2_MAX_AFS2_SUB', 'ZDDFRONTMEAN_01_AFS2_SUB', 'ESFQD_ZONE1MEAN_AFS2_SUB', 'ESFQD_ZONE1MAX_AFS2_SUB', 'ESFQD2_ZONE1MEAN_AFS2_SUB', 'ESFQD2_ZONE1MAX_AFS2_SUB']

# 숫자형 열 중 제외할 열 제외
numerical_columns = [col for col in df.select_dtypes(include=['number']).columns if col not in exclude_columns]

# 표준화 수행
scaler = StandardScaler()
df_standardized = df.copy()

# 열별로 표준화 적용
df_standardized[numerical_columns] = scaler.fit_transform(df[numerical_columns])

# 표준화 파라미터 저장 (mean, std)
scaler_params_path = 'scaler_params.pkl'
with open(scaler_params_path, 'wb') as f:
    pickle.dump(scaler, f)

# 결과 저장
df_standardized.to_csv('all_minmax_standardized.csv', index=False)
print(f"Standardization completed. Scaler parameters saved to '{scaler_params_path}'.")

# 새 데이터에 대해 동일한 scaler 사용
def standardize_new_data(new_df, scaler_path):
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    # 숫자형 열 중 제외할 열 제외
    numerical_columns = [col for col in new_df.select_dtypes(include=['number']).columns if col not in exclude_columns]
    
    new_df_standardized = new_df.copy()
    new_df_standardized[numerical_columns] = scaler.transform(new_df[numerical_columns])
    
    return new_df_standardized

# 새로운 데이터 테스트
new_data = pd.read_csv('new_data.csv')  # 새로운 데이터 파일
new_data_standardized = standardize_new_data(new_data, scaler_params_path)
new_data_standardized.to_csv('new_data_standardized.csv', index=False)
print("New data standardized and saved to 'new_data_standardized.csv'.")