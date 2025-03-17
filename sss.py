KeyError                                  Traceback (most recent call last)
Cell In[49], line 51
     49 if __name__ == "__main__":
     50     set_seed(42)
---> 51     main()

Cell In[49], line 11
      7 EQP_ID_MODULE_NAME = set(df['EQP_NM'])
      9 eqp_mapping = map_to_numeric(EQP_ID_MODULE_NAME)
---> 11 df = standardize_new_data(df, scaler_path)
     13 df = df.sort_values(by=["DATE", "WAFER_ID"], ascending=[True, True])
     15 df = df.dropna(subset=['Delta_SFQR'])

Cell In[44], line 95
     93 for col in numerical_columns:
     94     if col in scaler:
---> 95         mean = scaler[col]['mean']
     96         scale = scaler[col]['scale']
     97         new_df_standardized[col] = (new_df[col] - mean) / scale  # 직접 표준화 수식 적용

KeyError: 'mean'
