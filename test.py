def plot_predictions(predictions, true_labels):
    """
    예측값과 정답값을 비교하는 산점도 생성
    """
    plt.figure(figsize=(8, 8))
    
    # 정답값 (True Labels)
    plt.scatter(
        range(len(true_labels)),
        true_labels,
        alpha=0.6,
        edgecolor="blue",
        label="True Labels",
        color="blue"
    )
    
    # 예측값 (Predictions)
    plt.scatter(
        range(len(predictions)),
        predictions,
        alpha=0.6,
        edgecolor="red",
        label="Predictions",
        color="red"
    )
    
    # 그래프 설정
    plt.title("Predictions vs True Labels")
    plt.xlabel("Sample Index")
    plt.ylabel("Values")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()