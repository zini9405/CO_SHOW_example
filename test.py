def plot_predictions(predictions, true_labels):
    """
    정답값(x축)과 예측값(y축)을 비교하는 산점도 생성
    """
    plt.figure(figsize=(8, 8))
    
    # 산점도 생성
    plt.scatter(
        true_labels,
        predictions,
        alpha=0.6,
        edgecolor="k",
        label="Predictions vs True Labels",
        color="blue"
    )
    
    # y=x 선 추가 (이상적인 경우)
    plt.plot(
        [min(true_labels), max(true_labels)],
        [min(true_labels), max(true_labels)],
        'r--',
        lw=2,
        label="Ideal Line (y=x)"
    )
    
    # 그래프 설정
    plt.title("Predictions vs True Labels")
    plt.xlabel("True Labels")
    plt.ylabel("Predictions")
    plt.legend(loc="upper left")
    plt.grid(True)
    plt.show()