Cell In[17], line 31
     28 numeric_columns = [col for col in df.columns if col not in text_columns and col not in columns_to_remove]
     30 # EQP_NM 그룹별 평균값으로 결측치 채움
---> 31 df[numeric_columns] = df.groupby("EQP_NM")[numeric_columns].transform(lambda x: x.fillna(x.mean()))
     33 # **모든 값이 NaN이었던 경우 0으로 채우기**
     34 df[numeric_columns] = df[numeric_columns].fillna(0)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\groupby\generic.py:1815, in DataFrameGroupBy.transform(self, func, engine, engine_kwargs, *args, **kwargs)
   1812 @Substitution(klass="DataFrame", example=__examples_dataframe_doc)
   1813 @Appender(_transform_template)
   1814 def transform(self, func, *args, engine=None, engine_kwargs=None, **kwargs):
-> 1815     return self._transform(
   1816         func, *args, engine=engine, engine_kwargs=engine_kwargs, **kwargs
   1817     )

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\groupby\groupby.py:2021, in GroupBy._transform(self, func, engine, engine_kwargs, *args, **kwargs)
   2018     warn_alias_replacement(self, orig_func, func)
   2020 if not isinstance(func, str):
-> 2021     return self._transform_general(func, engine, engine_kwargs, *args, **kwargs)
   2023 elif func not in base.transform_kernel_allowlist:
   2024     msg = f"'{func}' is not a valid function name for transform(name)"

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\groupby\generic.py:1747, in DataFrameGroupBy._transform_general(self, func, engine, engine_kwargs, *args, **kwargs)
...
     47 def _sum(a, axis=None, dtype=None, out=None, keepdims=False,
     48          initial=_NoValue, where=True):
---> 49     return umr_sum(a, axis, dtype, out, keepdims, initial, where)

TypeError: can only concatenate str (not "int") to str
