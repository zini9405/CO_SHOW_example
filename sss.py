---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[7], line 11
      8 df_filtered = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors='ignore')
     10 # 분산(Variance) 및 사분위 범위(IQR) 계산
---> 11 variance = df_filtered.var()
     12 iqr = df_filtered.quantile(0.75) - df_filtered.quantile(0.25)
     14 # 변화가 적은 열을 찾기 위해 정렬

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\frame.py:11734, in DataFrame.var(self, axis, skipna, ddof, numeric_only, **kwargs)
  11725 @doc(make_doc("var", ndim=2))
  11726 def var(
  11727     self,
   (...)
  11732     **kwargs,
  11733 ):
> 11734     result = super().var(axis, skipna, ddof, numeric_only, **kwargs)
  11735     if isinstance(result, Series):
  11736         result = result.__finalize__(self, method="var")

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\generic.py:12346, in NDFrame.var(self, axis, skipna, ddof, numeric_only, **kwargs)
  12338 def var(
  12339     self,
  12340     axis: Axis | None = 0,
   (...)
...
-> 1016 sqr = _ensure_numeric((avg - values) ** 2)
   1017 if mask is not None:
   1018     np.putmask(sqr, mask, 0)

TypeError: unsupported operand type(s) for -: 'float' and 'str'


그리고  분산 기준과 IQR 기준으로 변화가 적은 순서로 나열해서 알려줘. 
