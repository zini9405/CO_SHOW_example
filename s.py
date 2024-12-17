# SHAP 분석 함수
def shap_analysis(model, dataset, device, feature_names):
    """
    SHAP 분석 및 시각화
    Args:
        model: 학습된 Transformer 모델
        dataset: CustomDataset 객체
        device: 실행할 디바이스 (CPU/GPU)
        feature_names: 특징 이름 리스트
    """
    print("Starting SHAP analysis...")

    # 모델 평가 모드
    model.eval()

    # 데이터 샘플 추출 (SHAP 계산 속도를 위해 일부 데이터 사용)
    num_samples = min(len(dataset), 500)  # 최대 500개 샘플 사용
    sampled_features = dataset.features[:num_samples]
    sampled_labels = dataset.labels[:num_samples]

    # 모델 예측 함수 정의
    def model_predict(x):
        x_tensor = torch.tensor(x, dtype=torch.float32).to(device)
        with torch.no_grad():
            return model(x_tensor).cpu().numpy()

    # SHAP Explainer 초기화 (KernelExplainer 사용)
    explainer = shap.KernelExplainer(model_predict, sampled_features[:50])

    # SHAP 값 계산
    shap_values = explainer.shap_values(sampled_features)

    # SHAP 요약 시각화
    plt.figure(figsize=(12, 6))  # 그래프 크기 조정
    shap.summary_plot(
        shap_values,
        sampled_features,
        feature_names=feature_names,
        plot_size=(0.8, 0.8),  # 텍스트 크기 조정
        show=True
    )

    # SHAP 상호작용 값 계산
    print("Calculating SHAP interaction values...")
    shap_interaction_values = explainer.shap_interaction_values(sampled_features)

    # 상호작용 요약 도표 시각화
    plt.figure(figsize=(12, 6))
    shap.summary_plot(
        shap_interaction_values,
        sampled_features,
        feature_names=feature_names,
        max_display=20
    )