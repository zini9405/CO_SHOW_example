---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
Cell In[48], line 28
     26 # 추가된 행과 원래 데이터를 합치기
     27 print(pd.DataFrame(rows_to_add))
---> 28 rows_to_add_df = pd.DataFrame(rows_to_add).set_index('STEP_ID')
     29 group = pd.concat([group, rows_to_add_df]).sort_index()
     30 grouped.append(group)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\frame.py:6122, in DataFrame.set_index(self, keys, drop, append, inplace, verify_integrity)
   6119                 missing.append(col)
   6121 if missing:
-> 6122     raise KeyError(f"None of {missing} are in the columns")
   6124 if inplace:
   6125     frame = self

KeyError: "None of ['STEP_ID'] are in the columns"
