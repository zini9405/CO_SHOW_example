import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
import pickle

# 표준화 수행 시 사용한 scaler 저장할 딕셔너리
scalers = {}

# 원본 데이터 읽기
df = pd.read_csv('processed_X_grouped.csv')

# 표준화 제외할 열 정의
exclude_columns = ['ANALYSIS_GROUP', 'SUBLOT', 'WAFER_ID', 'DATE', 'EQP_NM', 'Delta_SFQR', 'CL_HST_REG_DTTM']

# 숫자형 열 중 제외할 열 제외
numerical_columns = [col for col in df.select_dtypes(include=['number']).columns if col not in exclude_columns]

# 열별 최대/최소값 계산 및 10% 확장
max_min_values = df.agg(['min', 'max'])
expanded_ranges = {
    col: {
        "min": max_min_values.loc['min', col] - (max_min_values.loc['min', col]) * 0.1,
        "max": max_min_values.loc['max', col] + (max_min_values.loc['max', col]) * 0.1,
    }
    for col in numerical_columns
}

# 표준화 적용
df_standardized = df.copy()
for col in numerical_columns:
    expanded_min = expanded_ranges[col]['min']
    expanded_max = expanded_ranges[col]['max']
    
    # 범위 내에서만 표준화 수행
    mask = (df[col] >= expanded_min) & (df[col] <= expanded_max)
    
    scaler = StandardScaler()
    standardized_values = scaler.fit_transform(df.loc[mask, [col]])
    df_standardized.loc[mask, col] = standardized_values
    
    # 열별로 사용한 scaler 저장
    scalers[col] = {"mean": scaler.mean_[0], "scale": scaler.scale_[0]}

# Scaler 정보 저장 (복원을 위해 사용)
with open('scalers_SFQR_all.pkl', 'wb') as f:
    pickle.dump(scalers, f)

# 결과 출력
print("스케일러 저장 완료: scalers_all.pkl")


---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[37], line 20
     17 numerical_columns = [col for col in df.select_dtypes(include=['number']).columns if col not in exclude_columns]
     19 # 열별 최대/최소값 계산 및 10% 확장
---> 20 max_min_values = df.agg(['min', 'max'])
     21 expanded_ranges = {
     22     col: {
     23         "min": max_min_values.loc['min', col] - (max_min_values.loc['min', col]) * 0.1,
   (...)
     26     for col in numerical_columns
     27 }
     29 # 표준화 적용

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\frame.py:10149, in DataFrame.aggregate(self, func, axis, *args, **kwargs)
  10146 axis = self._get_axis_number(axis)
  10148 op = frame_apply(self, func=func, axis=axis, args=args, kwargs=kwargs)
> 10149 result = op.agg()
  10150 result = reconstruct_and_relabel_result(result, func, **kwargs)
  10151 return result

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\apply.py:928, in FrameApply.agg(self)
    926 result = None
    927 try:
--> 928     result = super().agg()
...
     43 def _amin(a, axis=None, out=None, keepdims=False,
     44           initial=_NoValue, where=True):
---> 45     return umr_minimum(a, axis, None, out, keepdims, initial, where)

TypeError: '<=' not supported between instances of 'float' and 'str'
