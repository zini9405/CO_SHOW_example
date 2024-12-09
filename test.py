import matplotlib.pyplot as plt

def plot_predictions(predictions, true_labels):
    """
    예측값과 실제값을 비교하는 산점도 생성
    """
    predictions = torch.tensor(predictions).cpu().numpy()
    true_labels = torch.tensor(true_labels).cpu().numpy()

    plt.figure(figsize=(8, 8))
    plt.scatter(true_labels, predictions, alpha=0.6, edgecolor="k")
    plt.plot([true_labels.min(), true_labels.max()], [true_labels.min(), true_labels.max()], 'r--', lw=2)  # y=x 선
    plt.title("Predictions vs True Labels")
    plt.xlabel("True Labels")
    plt.ylabel("Predictions")
    plt.grid(True)
    plt.show()

# Test 모델 실행 후 그래프 출력
predictions, true_labels = test_model(model, test_loader, device, save_path)
plot_predictions(predictions, true_labels)