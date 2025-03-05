ValueError                                Traceback (most recent call last)
Cell In[28], line 13
     10 data = pd.read_csv(os.path.join(base_path, sfqr))
     11 # 변환할 새로운 데이터프레임 생성
     12 result = data.groupby("SUBLOT_ID").apply(lambda group: group.drop(columns=["SUBLOT_ID"]).set_index("MTRL_ITEM_CODE").stack())\
---> 13     .unstack(level=[1, 2])
     15 # 새로운 열 이름을 생성 (code 값을 포함)
     16 result.columns = [f"{code}_{col}" for col, code in result.columns]

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\series.py:4615, in Series.unstack(self, level, fill_value, sort)
   4570 """
   4571 Unstack, also known as pivot, Series with MultiIndex to produce DataFrame.
   4572 
   (...)
   4611 b    2    4
   4612 """
   4613 from pandas.core.reshape.reshape import unstack
-> 4615 return unstack(self, level, fill_value, sort)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\reshape\reshape.py:494, in unstack(obj, level, fill_value, sort)
    490 if isinstance(level, (tuple, list)):
    491     if len(level) != 1:
    492         # _unstack_multiple only handles MultiIndexes,
    493         # and isn't needed for a single level
...
--> 210     raise ValueError("Index contains duplicate entries, cannot reshape")
    212 self.group_index = comp_index
    213 self.mask = mask

ValueError: Index contains duplicate entries, cannot reshape
