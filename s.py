---------------------------------------------------------------------------
NotFittedError                            Traceback (most recent call last)
Cell In[27], line 49
     44     plt.show()
     48     # Feature와 Label 관계 시각화
---> 49 visualize_feature_label_relationship(dataset, feature_names)

Cell In[27], line 19
     16 labels = dataset.labels
     18 quantile_transformer = QuantileTransformer(output_distribution='normal', random_state=42)
---> 19 labels = quantile_transformer.inverse_transform(labels.reshape(-1,1)).flatten()
     21 # 산점도: 각 feature와 label 관계
     22 num_features = len(feature_names)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\sklearn\preprocessing\_data.py:2963, in QuantileTransformer.inverse_transform(self, X)
   2947 def inverse_transform(self, X):
   2948     """Back-projection to the original space.
   2949 
   2950     Parameters
   (...)
   2961         The projected data.
   2962     """
-> 2963     check_is_fitted(self)
   2964     X = self._check_inputs(
   2965         X, in_fit=False, accept_sparse_negative=True, copy=self.copy
...
   1658     raise TypeError("%s is not an estimator instance." % (estimator))
   1660 if not _is_fitted(estimator, attributes, all_or_any):
-> 1661     raise NotFittedError(msg % {"name": type(estimator).__name__})

NotFittedError: This QuantileTransformer instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.
