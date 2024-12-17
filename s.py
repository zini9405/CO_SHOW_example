import seaborn as sns
import matplotlib.pyplot as plt

# Feature와 Label의 관계 시각화 함수
def visualize_feature_label_relationship(dataset, feature_names, quantile_transformer):
    """
    각 feature와 원래 label 간의 관계를 시각화합니다.
    Args:
        dataset: CustomDataset 객체
        feature_names: 특징 이름 리스트
        quantile_transformer: QuantileTransformer 객체 (복원에 사용)
    """
    print("Visualizing feature-label relationships...")

    # 데이터 준비
    features = dataset.features
    transformed_labels = dataset.labels

    # Label 복원 (inverse_transform)
    labels = quantile_transformer.inverse_transform(transformed_labels.reshape(-1, 1)).flatten()

    # 산점도: 각 feature와 원래 label 관계
    num_features = len(feature_names)
    for i in range(num_features):
        plt.figure(figsize=(8, 5))
        plt.scatter(features[:, i], labels, alpha=0.5, color="blue")
        plt.xlabel(feature_names[i])
        plt.ylabel("Original Label")
        plt.title(f"Relationship between {feature_names[i]} and Original Label")
        plt.grid(True)
        plt.show()

    # 상관관계 히트맵
    print("Generating feature-label correlation heatmap...")
    data = pd.DataFrame(features, columns=feature_names)
    data['Label'] = labels  # 원래 스케일의 label 추가

    # 상관관계 계산
    correlation_matrix = data.corr()

    # 히트맵 시각화
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
    plt.title("Feature-Original Label Correlation Heatmap")
    plt.show()