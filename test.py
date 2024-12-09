import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import probplot

# 샘플 데이터 로드 (y_train에 데이터가 있다고 가정)
# y_train = np.load("your_data.npy")  # 데이터 불러오기 예시

# 예제 데이터 생성 (실제 데이터로 교체하세요)
y_train = np.random.uniform(0.011111, 0.984731, size=1000)

# 1. 기본 통계량 확인
print("Basic Statistics")
print(f"Min: {np.min(y_train)}")
print(f"Max: {np.max(y_train)}")
print(f"Mean: {np.mean(y_train)}")
print(f"Std Dev: {np.std(y_train)}")
print(f"Median: {np.median(y_train)}")
print()

# 2. 히스토그램
plt.figure(figsize=(8, 5))
plt.hist(y_train, bins=50, edgecolor='k', alpha=0.7)
plt.title("Distribution of y_train (Histogram)")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.grid(axis='y')
plt.show()

# 3. 커널 밀도 추정 (KDE)
plt.figure(figsize=(8, 5))
sns.kdeplot(y_train, shade=True, color='blue')
plt.title("Kernel Density Estimation (KDE) of y_train")
plt.xlabel("Value")
plt.ylabel("Density")
plt.grid()
plt.show()

# 4. 박스플롯
plt.figure(figsize=(8, 2))
plt.boxplot(y_train, vert=False, patch_artist=True)
plt.title("Boxplot of y_train")
plt.xlabel("Value")
plt.show()

# 5. QQ Plot (정규성 확인)
plt.figure(figsize=(8, 5))
probplot(y_train, dist="norm", plot=plt)
plt.title("QQ Plot for Normality Check")
plt.grid()
plt.show()

# 6. 구간별 데이터 분포 확인
bins = np.linspace(0, 1, 6)  # 0.0~0.2, 0.2~0.4, ... 구간 생성
categories = pd.cut(y_train, bins=bins)
distribution = categories.value_counts().sort_index()
print("Data Distribution Across Bins:")
print(distribution)

# 시각화
plt.figure(figsize=(8, 5))
plt.bar(distribution.index.astype(str), distribution.values, color='orange', edgecolor='k')
plt.title("Data Distribution Across Bins")
plt.xlabel("Bins")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()

# 7. 샘플링한 데이터 분포 확인
sampled_data = np.random.choice(y_train, size=min(1000, len(y_train)), replace=False)

plt.figure(figsize=(8, 5))
plt.hist(sampled_data, bins=50, edgecolor='k', alpha=0.7)
plt.title("Sampled Data Distribution")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.grid(axis='y')
plt.show()
