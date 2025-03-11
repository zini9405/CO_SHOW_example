import pandas as pd

# 예제 리스트 (실제 데이터로 대체)
predictions = [0.9, 0.7, 0.2, 0.8, 0.3]  # 예측값 리스트
true_labels = [1, 1, 0, 1, 0]  # 실제 정답 리스트

# 데이터프레임 생성
df = pd.DataFrame({'predictions': predictions, 'true_labels': true_labels})

# CSV 파일로 저장
csv_filename = "predictions_vs_labels.csv"
df.to_csv(csv_filename, index=False)

print(f"CSV 파일이 저장되었습니다: {csv_filename}")