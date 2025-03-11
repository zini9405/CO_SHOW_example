import matplotlib.pyplot as plt
import pandas as pd

# 예제 데이터
predictions = [0.9, 0.7, 0.2, 0.8, 0.3]  # 예측값 리스트
true_labels = [1, 1, 0, 1, 0]  # 실제 정답 리스트

# 데이터프레임 생성
df = pd.DataFrame({'predictions': predictions, 'true_labels': true_labels})

# 그래프 그리기
plt.figure(figsize=(8, 5))
plt.plot(df.index, df.predictions, marker='o', linestyle='-', label="Predictions")
plt.plot(df.index, df.true_labels, marker='s', linestyle='--', label="True Labels")

plt.xlabel("Sample Index")
plt.ylabel("Value")
plt.title("Predictions vs True Labels")
plt.legend()
plt.grid(True)
plt.show()