import pandas as pd
import numpy as np

# CSV 파일 로드
df = pd.read_csv("dataset_ver3.csv")

columns_to_extract =     ['ANALYSIS_GROUP', 'SUBLOT', 'WAFER_ID', 'EQP_NM', 'DATE',
    "PROCESS-RAMP_UP-TEMP","STEP_TIME_RMS_PROC","PROCESS-RAMP_UP-TEMP","PROCESS-BAKE1-TEMP","PROCESS-COOL2-SLIT_H2",
    "PROCESS-DEPO-MULTIRUN_SET","PROCESS-COOL1-SLIT_H2","PROCESS-COOL3-SLIT_H2","PROCESS-DEPO-WITH_TEMP","PROCESS-DEPO-XFER_POWER",
    "PROCESS-POST_PURGE-SLIT_H2","PROCESS-DEPO-ACTIVE_POWER","PROCESS-BAKE2-TEMP","PROCESS-PRE_VENT-MAIN_H2","PROCESS-PRE_VENT-TEMP",
    "CLEAN-BAKE-MAIN_H2","CLEAN-PRE_VENT-TEMP","CLEAN-PURGE-SLIT_H2","CLEAN-RAMP_UP-MAIN_H2","CLEAN-PRE_VENT-MAIN_H2",
    "CLEAN-COOL-MAIN_H2","CLEAN-ETCH-MAIN_H2","CLEAN-RAMP_UP-TEMP","CLEAN-BAKE-TEMP","CLEAN-COOL-SLIT_H2","CLEAN-PURGE-MAIN_H2",
    "CLEAN-ETCH-TEMP","CLEAN-POST_PURGE-SLIT_H2","CLEAN-POST_PURGE-MAIN_H2","CLEAN-ETCH-SLIT_H2","CLEAN-RAMP_UP-SLIT_H2",'Delta_SFQR']

df_extracted = df[[col for col in columns_to_extract if col in df.columns]]

text_columns = ['ANALYSIS_GROUP', 'SUBLOT', 'WAFER_ID', 'EQP_NM', 'DATE']


# 1️⃣ **문자열 컬럼 결측치 처리 (NaN → "Unknown")**
for col in text_columns:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")  

# df = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors="ignore")

# 결측값을 채우는 함수 정의
def fill_missing_values(series):
    values = series.values.copy()

    for i in range(len(values)):
        if pd.isna(values[i]):
            # 이전 값 찾기
            prev_idx = i - 1
            while prev_idx >= 0 and pd.isna(values[prev_idx]):
                prev_idx -= 1

            # 다음 값 찾기
            next_idx = i + 1
            while next_idx < len(values) and pd.isna(values[next_idx]):
                next_idx += 1

            # 이전과 다음 값이 모두 존재하면 평균으로
            if prev_idx >= 0 and next_idx < len(values) and not pd.isna(values[next_idx]):
                values[i] = (values[prev_idx] + values[next_idx]) / 2
            else:
                # 둘 중 하나라도 없으면 전체 평균값으로 채움
                mean_value = np.nanmean(values)
                values[i] = mean_value

    return pd.Series(values, index=series.index)

# 그룹화하고 결측값 채우기
def fill_group(group):
    for col in group.columns:
        if group[col].isnull().any() and col not in ['ANALYSIS_GROUP', 'EQP_NM']:
            group[col] = fill_missing_values(group[col])
    return group

df_filled = df_extracted.groupby(['ANALYSIS_GROUP', 'EQP_NM'], group_keys=False).apply(fill_group)


ValueError                                Traceback (most recent call last)
Cell In[36], line 60
     57             group[col] = fill_missing_values(group[col])
     58     return group
---> 60 df_filled = df_extracted.groupby(['ANALYSIS_GROUP', 'EQP_NM'], group_keys=False).apply(fill_group)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\groupby\groupby.py:1824, in GroupBy.apply(self, func, include_groups, *args, **kwargs)
   1822 with option_context("mode.chained_assignment", None):
   1823     try:
-> 1824         result = self._python_apply_general(f, self._selected_obj)
   1825         if (
   1826             not isinstance(self.obj, Series)
   1827             and self._selection is None
   1828             and self._selected_obj.shape != self._obj_with_exclusions.shape
   1829         ):
   1830             warnings.warn(
   1831                 message=_apply_groupings_depr.format(
   1832                     type(self).__name__, "apply"
   (...)
   1835                 stacklevel=find_stack_level(),
   1836             )

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\groupby\groupby.py:1885, in GroupBy._python_apply_general(self, f, data, not_indexed_same, is_transform, is_agg)
   1850 @final
...
   1578         f"The truth value of a {type(self).__name__} is ambiguous. "
   1579         "Use a.empty, a.bool(), a.item(), a.any() or a.all()."
   1580     )

ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
