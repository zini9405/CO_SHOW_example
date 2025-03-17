import pickle
import pandas as pd

def normalize_new_data(new_df, scaler_path):
    # 저장된 스케일러 불러오기 (dict 형태)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    # 정규화 제외할 열
    exclude_columns = ['ANALYSIS_GROUP', 'SUBLOT', 'WAFER_ID', 'DATE', 'EQP_NM', 'Delta_SFQR', 'CL_HST_REG_DTTM']

    # 숫자형 열 중 제외할 열을 제외한 리스트
    numerical_columns = [col for col in new_df.select_dtypes(include=['number']).columns if col not in exclude_columns]
    
    # 정규화 적용 (X_scaled = (X - min) / (max - min))
    new_df_normalized = new_df.copy()
    
    for col in numerical_columns:
        if col in scaler:
            if 'min' in scaler[col] and 'max' in scaler[col]:  # min/max 값이 존재하는 경우에만 변환
                min_val = scaler[col]['min']
                max_val = scaler[col]['max']
                
                # min과 max가 동일한 경우 0으로 설정 (안전 처리)
                if max_val - min_val == 0:
                    new_df_normalized[col] = 0
                else:
                    new_df_normalized[col] = (new_df[col] - min_val) / (max_val - min_val)

    return new_df_normalized