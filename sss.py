---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
Cell In[46], line 25
     23 drop_columns = ["GBIR_AFS2", "WAF_ID", "BASE_DT", "PAD_TEMP_STEP_MEAN"]
     24 if "EQP_ID" in df.columns:
---> 25     drop_columns.remove("EQP_ID")  # EQP_ID는 변환해야 하므로 제거 X
     27 # EQP_ID를 숫자로 변환 (임베딩할 예정)
     28 eqp_encoder = LabelEncoder()

ValueError: list.remove(x): x not in list
