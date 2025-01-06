def visualize_attention_scores(model, feature_names):
    """
    Attention Weights를 시각화하여 변수별 중요도 출력
    """
    attention_maps = model.get_attention_maps()  # Attention Weights 가져오기
    last_attention_map = attention_maps[-1].squeeze(0).detach().cpu().numpy()  # 마지막 레이어 사용
    avg_attention = np.mean(last_attention_map, axis=0)  # 각 Feature에 대한 평균 Attention Score 계산

    # Feature 중요도 정렬
    sorted_indices = np.argsort(-avg_attention)  # 중요도 순서대로 정렬

    print("\nFeature Importance:")
    for idx in sorted_indices:
        print(f"{feature_names[idx]}: {avg_attention[idx]:.4f}")

    # 시각화
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(feature_names)), avg_attention[sorted_indices], tick_label=[feature_names[i] for i in sorted_indices])
    plt.xticks(rotation=45, ha='right')
    plt.title("Feature Importance (Attention Scores)")
    plt.ylabel("Attention Score")
    plt.tight_layout()
    plt.show()