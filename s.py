TypeError                                 Traceback (most recent call last)
Cell In[20], line 1
----> 1 shap_analysis(model, dataset, device, feature_names)

Cell In[19], line 38
     36 # SHAP 요약 시각화
     37 plt.figure(figsize=(12, 6))
---> 38 shap.summary_plot(
     39     shap_values,
     40     sampled_features,
     41     feature_names=feature_names,
     42     show=True
     43 )
     45 # 근사적인 상호작용 분석: Feature Pair Plot
     46 print("Generating SHAP Feature Pair Plot...")

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\shap\plots\_beeswarm.py:595, in summary_legacy(shap_values, features, feature_names, max_display, plot_type, color, axis_color, title, alpha, show, sort, color_bar, plot_size, layered_violin_max_num_bins, class_names, class_inds, color_bar_label, cmap, show_values_in_legend, use_log_scale)
    591 proj_shap_values = shap_values[:, sort_inds[0], sort_inds]
    592 proj_shap_values[:, 1:] *= 2  # because off diag effects are split in half
    593 summary_legacy(
    594     proj_shap_values, features[:, sort_inds] if features is not None else None,
--> 595     feature_names=feature_names[sort_inds],
    596     sort=False, show=False, color_bar=False,
    597     plot_size=None,
...
    599 )
    600 pl.xlim((slow, shigh))
    601 pl.xlabel("")
