---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[33], line 1
----> 1 shap_analysis(model, dataset, device, feature_names)

Cell In[32], line 150
    148 # SHAP 상호작용 값 계산
    149 print("Calculating SHAP interaction values...")
--> 150 shap_interaction_values = explainer.shap_interaction_values(sampled_features)
    152 # 상호작용 요약 도표 시각화
    153 plt.figure(figsize=(12, 6))

AttributeError: 'PermutationExplainer' object has no attribute 'shap_interaction_values'
