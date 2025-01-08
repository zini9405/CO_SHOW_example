ValueError                                Traceback (most recent call last)
Cell In[3], line 1
----> 1 df_Y['HST_REG_DTTM'] = df_Y['HST_REG_DTTM'].map(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d').date())

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\series.py:4700, in Series.map(self, arg, na_action)
   4620 def map(
   4621     self,
   4622     arg: Callable | Mapping | Series,
   4623     na_action: Literal["ignore"] | None = None,
   4624 ) -> Series:
   4625     """
   4626     Map values of Series according to an input mapping or function.
   4627 
   (...)
   4698     dtype: object
   4699     """
-> 4700     new_values = self._map_values(arg, na_action=na_action)
   4701     return self._constructor(new_values, index=self.index, copy=False).__finalize__(
   4702         self, method="map"
   4703     )

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\base.py:921, in IndexOpsMixin._map_values(self, mapper, na_action, convert)
    918 if isinstance(arr, ExtensionArray):
    919     return arr.map(mapper, na_action=na_action)
...
    335 if len(data_string) != found.end():
    336     raise ValueError("unconverted data remains: %s" %
    337                       data_string[found.end():])

ValueError: time data '2024-01-01 07:00:04' does not match format '%Y%m%d'
