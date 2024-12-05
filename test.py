MemoryError                               Traceback (most recent call last)
Cell In[51], line 31
     28     grouped.append(group)
     30 # 다시 병합
---> 31 df_filled = pd.concat(grouped).reset_index(drop=True)
     33 # 결과 출력
     34 print(df_filled)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\frame.py:6417, in DataFrame.reset_index(self, level, drop, inplace, col_level, col_fill, allow_duplicates, names)
   6415     new_obj = self
   6416 else:
-> 6417     new_obj = self.copy(deep=None)
   6418 if allow_duplicates is not lib.no_default:
   6419     allow_duplicates = validate_bool_kwarg(allow_duplicates, "allow_duplicates")

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\generic.py:6811, in NDFrame.copy(self, deep)
   6662 @final
   6663 def copy(self, deep: bool_t | None = True) -> Self:
   6664     """
   6665     Make a copy of this object's indices and data.
   6666 
   (...)
   6809     dtype: int64
   6810     """
...
    289 if not isinstance(arrs, tuple):
    290     arrs = (arrs,)
--> 291 return _nx.concatenate(arrs, 0, dtype=dtype, casting=casting)

MemoryError: Unable to allocate 5.23 GiB for an array with shape (32, 21941622) and data type float64
