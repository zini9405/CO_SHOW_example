c. 상호작용 요약 도표Interaction summary plot

이 도표는 서로 다른 채널 간의 상호 작용을 한 눈에 볼 수 있게 해주는 매우 중요한 도표이다.


# SHAP interaction values
shap_interaction_values = shap.TreeExplainer(rf).shap_interaction_values(X_train)
 
# Interaction Summary Plot 
shap.summary_plot(shap_interaction_values, X_train)
