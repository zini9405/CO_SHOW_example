MergeError                                Traceback (most recent call last)
Cell In[50], line 8
      4 df_b = pd.read_csv("const_data.csv")
      7 # id 기준으로 병합
----> 8 merged_df = df_a.merge(df_b, on="SUBLOT_ID", how="outer")
     10 # 병합된 데이터 저장
     11 merged_df.to_csv("data_ver1.csv", index=False)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\frame.py:10832, in DataFrame.merge(self, right, how, on, left_on, right_on, left_index, right_index, sort, suffixes, copy, indicator, validate)
  10813 @Substitution("")
  10814 @Appender(_merge_doc, indents=2)
  10815 def merge(
   (...)
  10828     validate: MergeValidate | None = None,
  10829 ) -> DataFrame:
  10830     from pandas.core.reshape.merge import merge
> 10832     return merge(
  10833         self,
  10834         right,
  10835         how=how,
  10836         on=on,
  10837         left_on=left_on,
  10838         right_on=right_on,
  10839         left_index=left_index,
...
   2759         f"not allowed.",
   2760     )
   2762 return llabels, rlabels

MergeError: Passing 'suffixes' which cause duplicate columns {'index_y', 'Unnamed: 0_y', 'Unnamed: 0.1_y'} is not allowed.
