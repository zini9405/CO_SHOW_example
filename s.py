---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)
Cell In[35], line 1
----> 1 shap_analysis(model, dataset, device, feature_names)

Cell In[34], line 155
    151 feature_y = 1  # Y축에 사용할 특징 인덱스
    153 plt.figure(figsize=(10, 6))
    154 plt.scatter(sampled_features[:, feature_x], sampled_features[:, feature_y], 
--> 155             c=shap_values[:, feature_x] + shap_values[:, feature_y], cmap='viridis')
    156 plt.colorbar(label="SHAP Value Sum")
    157 plt.xlabel(feature_names[feature_x])

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\shap\_explanation.py:391, in Explanation.__getitem__(self, item)
    389 if new_self is None:
    390     new_self = copy.copy(self)
--> 391 new_self._s = new_self._s.__getitem__(item)
    392 new_self.op_history.append({
    393     "name": "__getitem__",
    394     "args": (item,),
    395     "prev_shape": self.shape
    396 })
    398 return new_self

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\slicer\slicer.py:112, in Slicer.__getitem__(self, item)
...
    417 is_element = any([True if isinstance(x, int) else False for x in cut_index])
--> 418 sliced_o = o[cut_index]
    420 return is_element, sliced_o, cut

IndexError: index 1 is out of bounds for axis 1 with size 1
