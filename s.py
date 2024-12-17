from sklearn.preprocessing import MinMaxScaler

# SHAP 분석 함수
def shap_analysis(model, dataset, device, feature_names):
    """
    SHAP 분석 및 근사적인 상호작용 분석
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
    shap_values = np.array(shap_values)  # 명확하게 numpy 배열로 변환

    # SHAP 요약 시각화
    plt.figure(figsize=(12, 6))
    shap.summary_plot(
        shap_values,
        sampled_features,
        feature_names=feature_names,
        show=True
    )

    # 근사적인 상호작용 분석: Feature Pair Plot
    print("Generating SHAP Feature Pair Plot...")
    feature_x = 0  # X축에 사용할 특징 인덱스
    feature_y = 1  # Y축에 사용할 특징 인덱스

    # SHAP 값 정규화
    scaler = MinMaxScaler()
    normalized_shap = scaler.fit_transform(shap_values.reshape(-1, 1))

    plt.figure(figsize=(10, 6))
    plt.scatter(
        sampled_features[:, feature_x],
        sampled_features[:, feature_y],
        c=normalized_shap.flatten(),  # 정규화된 SHAP 값 사용
        cmap='viridis'
    )
    plt.colorbar(label="Normalized SHAP Value")
    plt.xlabel(feature_names[feature_x])
    plt.ylabel(feature_names[feature_y])
    plt.title("SHAP Feature Pair Interaction Plot")
    plt.grid(True)
    plt.show()