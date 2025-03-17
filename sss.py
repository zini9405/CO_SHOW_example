def standardize_new_data(new_df, scaler_path):
    # 저장된 스케일러 불러오기 (dict 형태)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    # 표준화 제외할 열
    exclude_columns = ['ANALYSIS_GROUP', 'SUBLOT', 'WAFER_ID', 'DATE', 'EQP_NM', 'Delta_SFQR', 'CL_HST_REG_DTTM']

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
