TypeError                                 Traceback (most recent call last)
File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\groupby\groupby.py:1824, in GroupBy.apply(self, func, include_groups, *args, **kwargs)
   1823 try:
-> 1824     result = self._python_apply_general(f, self._selected_obj)
   1825     if (
   1826         not isinstance(self.obj, Series)
   1827         and self._selection is None
   1828         and self._selected_obj.shape != self._obj_with_exclusions.shape
   1829     ):

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\groupby\groupby.py:1885, in GroupBy._python_apply_general(self, f, data, not_indexed_same, is_transform, is_agg)
   1859 """
   1860 Apply function f in python space
   1861 
   (...)
   1883     data after applying f
   1884 """
-> 1885 values, mutated = self._grouper.apply_groupwise(f, data, self.axis)
   1886 if not_indexed_same is None:

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\groupby\ops.py:919, in BaseGrouper.apply_groupwise(self, f, data, axis)
    918 group_axes = group.axes
--> 919 res = f(group)
    920 if not mutated and not _is_indexed_like(res, group_axes, axis):

Cell In[16], line 35
     34     else:
---> 35         group[col] = group[col].fillna(group[col].mean())  # NaN을 그룹 평균값으로 채움
     36 return group

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\series.py:6549, in Series.mean(self, axis, skipna, numeric_only, **kwargs)
   6541 @doc(make_doc("mean", ndim=1))
   6542 def mean(
   6543     self,
   (...)
   6547     **kwargs,
   6548 ):
-> 6549     return NDFrame.mean(self, axis, skipna, numeric_only, **kwargs)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\generic.py:12420, in NDFrame.mean(self, axis, skipna, numeric_only, **kwargs)
  12413 def mean(
  12414     self,
  12415     axis: Axis | None = 0,
   (...)
  12418     **kwargs,
  12419 ) -> Series | float:
> 12420     return self._stat_function(
  12421         "mean", nanops.nanmean, axis, skipna, numeric_only, **kwargs
  12422     )

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\generic.py:12377, in NDFrame._stat_function(self, name, func, axis, skipna, numeric_only, **kwargs)
  12375 validate_bool_kwarg(skipna, "skipna", none_allowed=False)
> 12377 return self._reduce(
  12378     func, name=name, axis=axis, skipna=skipna, numeric_only=numeric_only
  12379 )

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\series.py:6457, in Series._reduce(self, op, name, axis, skipna, numeric_only, filter_type, **kwds)
   6453     raise TypeError(
   6454         f"Series.{name} does not allow {kwd_name}={numeric_only} "
   6455         "with non-numeric dtypes."
   6456     )
-> 6457 return op(delegate, skipna=skipna, **kwds)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\nanops.py:147, in bottleneck_switch.__call__.<locals>.f(values, axis, skipna, **kwds)
    146 else:
--> 147     result = alt(values, axis=axis, skipna=skipna, **kwds)
    149 return result

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\nanops.py:404, in _datetimelike_compat.<locals>.new_func(values, axis, skipna, mask, **kwargs)
    402     mask = isna(values)
--> 404 result = func(values, axis=axis, skipna=skipna, mask=mask, **kwargs)
    406 if datetimelike:

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\nanops.py:719, in nanmean(values, axis, skipna, mask)
    718 count = _get_counts(values.shape, mask, axis, dtype=dtype_count)
--> 719 the_sum = values.sum(axis, dtype=dtype_sum)
    720 the_sum = _ensure_numeric(the_sum)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\numpy\core\_methods.py:49, in _sum(a, axis, dtype, out, keepdims, initial, where)
     47 def _sum(a, axis=None, dtype=None, out=None, keepdims=False,
     48          initial=_NoValue, where=True):
---> 49     return umr_sum(a, axis, dtype, out, keepdims, initial, where)

TypeError: can only concatenate str (not "int") to str

During handling of the above exception, another exception occurred:

TypeError                                 Traceback (most recent call last)
Cell In[16], line 39
     36     return group
     38 # EQP_NM 기준으로 그룹화 후 빈값 처리
---> 39 df = df.groupby("EQP_NM").apply(fill_missing_values)
     41 # SFQR_AFS2 - SFQR_AFS2_SUB 값 계산하여 새로운 열 추가
     42 df["SFQR"] = df["SFQR_AFS2"] - df["SFQR_AFS2_SUB"]

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\groupby\groupby.py:1846, in GroupBy.apply(self, func, include_groups, *args, **kwargs)
   1830             warnings.warn(
   1831                 message=_apply_groupings_depr.format(
   1832                     type(self).__name__, "apply"
   (...)
   1835                 stacklevel=find_stack_level(),
   1836             )
   1837     except TypeError:
   1838         # gh-20949
   1839         # try again, with .apply acting as a filtering
   (...)
   1843         # fails on *some* columns, e.g. a numeric operation
   1844         # on a string grouper column
-> 1846         return self._python_apply_general(f, self._obj_with_exclusions)
   1848 return result

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\groupby\groupby.py:1885, in GroupBy._python_apply_general(self, f, data, not_indexed_same, is_transform, is_agg)
   1850 @final
   1851 def _python_apply_general(
   1852     self,
   (...)
   1857     is_agg: bool = False,
   1858 ) -> NDFrameT:
   1859     """
   1860     Apply function f in python space
   1861 
   (...)
   1883         data after applying f
   1884     """
-> 1885     values, mutated = self._grouper.apply_groupwise(f, data, self.axis)
   1886     if not_indexed_same is None:
   1887         not_indexed_same = mutated

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\groupby\ops.py:919, in BaseGrouper.apply_groupwise(self, f, data, axis)
    917 # group might be modified
    918 group_axes = group.axes
--> 919 res = f(group)
    920 if not mutated and not _is_indexed_like(res, group_axes, axis):
    921     mutated = True

Cell In[16], line 35
     33         group[col] = 0  # 모든 값이 NaN이면 0으로 채움
     34     else:
---> 35         group[col] = group[col].fillna(group[col].mean())  # NaN을 그룹 평균값으로 채움
     36 return group

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\series.py:6549, in Series.mean(self, axis, skipna, numeric_only, **kwargs)
   6541 @doc(make_doc("mean", ndim=1))
   6542 def mean(
   6543     self,
   (...)
   6547     **kwargs,
   6548 ):
-> 6549     return NDFrame.mean(self, axis, skipna, numeric_only, **kwargs)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\generic.py:12420, in NDFrame.mean(self, axis, skipna, numeric_only, **kwargs)
  12413 def mean(
  12414     self,
  12415     axis: Axis | None = 0,
   (...)
  12418     **kwargs,
  12419 ) -> Series | float:
> 12420     return self._stat_function(
  12421         "mean", nanops.nanmean, axis, skipna, numeric_only, **kwargs
  12422     )

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\generic.py:12377, in NDFrame._stat_function(self, name, func, axis, skipna, numeric_only, **kwargs)
  12373 nv.validate_func(name, (), kwargs)
  12375 validate_bool_kwarg(skipna, "skipna", none_allowed=False)
> 12377 return self._reduce(
  12378     func, name=name, axis=axis, skipna=skipna, numeric_only=numeric_only
  12379 )

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\series.py:6457, in Series._reduce(self, op, name, axis, skipna, numeric_only, filter_type, **kwds)
   6452     # GH#47500 - change to TypeError to match other methods
   6453     raise TypeError(
   6454         f"Series.{name} does not allow {kwd_name}={numeric_only} "
   6455         "with non-numeric dtypes."
   6456     )
-> 6457 return op(delegate, skipna=skipna, **kwds)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\nanops.py:147, in bottleneck_switch.__call__.<locals>.f(values, axis, skipna, **kwds)
    145         result = alt(values, axis=axis, skipna=skipna, **kwds)
    146 else:
--> 147     result = alt(values, axis=axis, skipna=skipna, **kwds)
    149 return result

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\nanops.py:404, in _datetimelike_compat.<locals>.new_func(values, axis, skipna, mask, **kwargs)
    401 if datetimelike and mask is None:
    402     mask = isna(values)
--> 404 result = func(values, axis=axis, skipna=skipna, mask=mask, **kwargs)
    406 if datetimelike:
    407     result = _wrap_results(result, orig_values.dtype, fill_value=iNaT)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\nanops.py:719, in nanmean(values, axis, skipna, mask)
    716     dtype_count = dtype
    718 count = _get_counts(values.shape, mask, axis, dtype=dtype_count)
--> 719 the_sum = values.sum(axis, dtype=dtype_sum)
    720 the_sum = _ensure_numeric(the_sum)
    722 if axis is not None and getattr(the_sum, "ndim", False):

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\numpy\core\_methods.py:49, in _sum(a, axis, dtype, out, keepdims, initial, where)
     47 def _sum(a, axis=None, dtype=None, out=None, keepdims=False,
     48          initial=_NoValue, where=True):
---> 49     return umr_sum(a, axis, dtype, out, keepdims, initial, where)

TypeError: can only concatenate str (not "int") to str
