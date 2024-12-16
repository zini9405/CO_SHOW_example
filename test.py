---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[15], line 8
      5 visualize_predictions(predictions, true_labels)
      7 # SHAP 분석
----> 8 shap_analysis(model, dataset, device, feature_names)

Cell In[13], line 148
    145 # 특정 샘플 SHAP Force Plot
    146 sample_index = 0  # 첫 번째 샘플
    147 shap.force_plot(
--> 148     explainer.expected_value[0],
    149     shap_values[sample_index],
    150     sampled_features[sample_index],
    151     feature_names=feature_names
    152 )

AttributeError: 'PermutationExplainer' object has no attribute 'expected_value'
