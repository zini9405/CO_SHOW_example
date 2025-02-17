# 새 데이터에 대해 동일한 scaler 사용
def standardize_new_data(new_df, scaler_path):
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    exclude_columns = ['BASE_DT', 'EQP_ID', 'WAF_ID', '6900_GBIR_AFS2']

    # 숫자형 열 중 제외할 열 제외
    numerical_columns = [col for col in new_df.select_dtypes(include=['number']).columns if col not in exclude_columns]
    
    new_df_standardized = new_df.copy()
    new_df_standardized[numerical_columns] = scaler.transform(new_df[numerical_columns])
    
    return new_df_standardized


scaler 파일

'SLOT_NO': {'mean': 12.974388824214202, 'scale': 7.047941189865221},
 'RECIPE_ID': {'mean': 31.373427053730648, 'scale': 8.900819827232842},
 'INTERNLA_GEAR_RPM_ACTUAL_STEP_MEAN': {'mean': 4.4998535948806815,
  'scale': 0.6602251951883292},
 'PAD_TEMP_STEP_MEAN': {'mean': 28.27537247090136,
  'scale': 11.549126790269343},
 'RING_GEAR_MOTOR_CURRENT_STEP_MEAN': {'mean': 17.359841937553966,
  'scale': 2.0386003408298716},
 'SLURRY_1_FLOW_STEP_MEAN': {'mean': 10.252418095922478,
  'scale': 1.8661566948594877},
 'SLURRY_IN_TEMP_STEP_MEAN': {'mean': 22.315061156669852,
  'scale': 1.4250179708190496},
 'SUN_GEAR_MOTOR_CURRENT_STEP_MEAN': {'mean': 6.834722152203723,
  'scale': 1.4125939646500303},
 'SUN_GEAR_RPM_ACTUAL_STEP_MEAN': {'mean': 16.812792791649684,
  'scale': 3.010483569460977},
 'SURFACTANT_FLOW_ACTUAL_STEP_MEAN': {'mean': 1.4933999538839127,
  'scale': 0.818853737513499},
 'PRS_PRES_ACTUAL__STEP_MEAN': {'mean': 117.92822036340894,
  'scale': 44.29005042501517},
 'UPPER_COOLING_IN_TEMP_STEP_MEAN': {'mean': 20.48223261938878,
  'scale': 0.6561384222664526},
 'UPPER_COOLING_OUT_TEMP_STEP_MEAN': {'mean': 21.787057718079865,
  'scale': 0.9639763975191185},
 'UPPER_COOLING_FLOW_STEP_MEAN': {'mean': 26.19041898897981,
  'scale': 8.86068481778627},
 'UPPER_MOTOR_CURRENT_STEP_MEAN': {'mean': 56.20701826013863,
  'scale': 13.91463283862114},
 'UPPER_RPM_ACTUAL_STEP_MEAN': {'mean': 2.9914692560356566,
  'scale': 5.997640658753852},
 'LOWER_COOLING_IN_TEMP_STEP_MEAN': {'mean': 20.521555017682804,
  'scale': 0.7524950650218306},
 'LOWER_COOLING_OUT_TEMP_STEP_MEAN': {'mean': 22.344049373829616,
  'scale': 1.3261574137933942},
 'LOWER_COOLING_FLOW_STEP_MEAN': {'mean': 26.02935438669784,
  'scale': 8.792941617481903},
 'LOWER_MOTOR_CURRENT_STEP_MEAN': {'mean': 65.08826366363533,
  'scale': 12.808461137942327},
 'LOWER_RPM_ACTUAL_STEP_MEAN': {'mean': 23.440999400438862,
  'scale': 3.2740424764020886},
 'PRS_PRES_ACTUAL__STEP_COUNT': {'mean': 817.7030513067306,
  'scale': 425.46505958497227},
 'PAD_COUNT': {'mean': 513.2883302404275, 'scale': 378.1415794372828},
 'SLURRY_USE_NUM': {'mean': 429.69176370877284, 'scale': 298.2220143651525},
 'DD_USE_NUM': {'mean': 39.70816996192507, 'scale': 27.28059519930904},
 'MAIN_RUNTIME': {'mean': 908.9749401781031, 'scale': 296.2914007473515},
 'CARRIER_MTL_USE_NUM': {'mean': 299.59193388471436,
  'scale': 362.0445803166511}}

---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[7], line 5
      2 scaler_path = 'scalers.pkl'
      3 df = pd.read_csv(csv_file)
----> 5 df = standardize_new_data(df, scaler_path)
      7 df = df.dropna(subset=['6900_GBIR_AFS2'])
      9 df.fillna(0, inplace=True)

Cell In[4], line 72
     69 numerical_columns = [col for col in new_df.select_dtypes(include=['number']).columns if col not in exclude_columns]
     71 new_df_standardized = new_df.copy()
---> 72 new_df_standardized[numerical_columns] = scaler.transform(new_df[numerical_columns])
     74 return new_df_standardized

AttributeError: 'dict' object has no attribute 'transform'
