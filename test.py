import matplotlib.pyplot as plt
import torch

def plot_predictions(predictions, true_labels):
    """
    예측값과 실제값을 비교하는 산점도 생성
    """
    # 모든 데이터를 torch.Tensor로 변환
    predictions = torch.cat([torch.tensor(p).unsqueeze(0) for p in predictions]).detach().cpu()
    true_labels = torch.cat([torch.tensor(t).unsqueeze(0) for t in true_labels]).detach().cpu()

    # 산점도 생성
    plt.figure(figsize=(8, 8))
    plt.scatter(true_labels, predictions, alpha=0.6, edgecolor="k")
    plt.plot(
        [true_labels.min().item(), true_labels.max().item()],
        [true_labels.min().item(), true_labels.max().item()],
        'r--', lw=2
    )  # y=x 선
    plt.title("Predictions vs True Labels")
    plt.xlabel("True Labels")
    plt.ylabel("Predictions")
    plt.grid(True)
    plt.show()

# 테스트 함수 실행 후 그래프 출력
predictions, true_labels = test_model(model, test_loader, device, save_path)
plot_predictions(predictions, true_labels)