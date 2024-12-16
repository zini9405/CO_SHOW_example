TypeError                                 Traceback (most recent call last)
Cell In[7], line 51
     45 explainer = shap.Explainer(
     46     lambda x: model(torch.tensor(x, dtype=torch.float32)).detach().numpy(),
     47     input_data
     48 )
     50 # SHAP 값 계산
---> 51 shap_values = explainer(input_data)
     53 # SHAP 시각화: 전체 데이터에 대한 중요도
     54 shap.summary_plot(shap_values, input_data, feature_names=feature_names)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\shap\explainers\_permutation.py:77, in PermutationExplainer.__call__(self, max_evals, main_effects, error_bounds, batch_size, outputs, silent, *args)
     74 def __call__(self, *args, max_evals=500, main_effects=False, error_bounds=False, batch_size="auto",
     75              outputs=None, silent=False):
     76     """Explain the output of the model on the given arguments."""
---> 77     return super().__call__(
     78         *args, max_evals=max_evals, main_effects=main_effects, error_bounds=error_bounds, batch_size=batch_size,
     79         outputs=outputs, silent=silent
     80     )

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\shap\explainers\_explainer.py:266, in Explainer.__call__(self, max_evals, main_effects, error_bounds, batch_size, outputs, silent, *args, **kwargs)
    264     feature_names = [[] for _ in range(len(args))]
    265 for row_args in show_progress(zip(*args), num_rows, self.__class__.__name__+" explainer", silent):
--> 266     row_result = self.explain_row(
...
-> 2348 xfin = isfinite(x)
   2349 yfin = isfinite(y)
   2350 if all(xfin) and all(yfin):

TypeError: ufunc 'isfinite' not supported for the input types, and the inputs could not be safely coerced to any supported types according to the casting rule ''safe''
