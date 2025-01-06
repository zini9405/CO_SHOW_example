---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)
Cell In[17], line 176
    173     visualize_attention_scores(model, dataset.feature_names)
    175 if __name__ == "__main__":
--> 176     main()

Cell In[17], line 173
    170 # Forward 실행
    171 _ = model(sample_features, sample_eqp_ids)
--> 173 visualize_attention_scores(model, dataset.feature_names)

Cell In[17], line 99
     97 print("\nFeature Importance:")
     98 for idx in sorted_indices:
---> 99     print(f"{feature_names[idx]}: {avg_attention[idx]:.4f}")
    101 # 시각화
    102 plt.figure(figsize=(10, 6))

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\indexes\base.py:5389, in Index.__getitem__(self, key)
   5386 if is_integer(key) or is_float(key):
   5387     # GH#44051 exclude bool, which would return a 2d ndarray
   5388     key = com.cast_scalar_indexer(key)
-> 5389     return getitem(key)
   5391 if isinstance(key, slice):
   5392     # This case is separated from the conditional above to avoid
   5393     # pessimization com.is_bool_indexer and ndim checks.
   5394     return self._getitem_slice(key)

IndexError: index 300 is out of bounds for axis 0 with size 32
