import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 불러오기
df = pd.read_csv('standardized_data.csv')

# 📌 특정 열 선택 (예: 'PAD_TEMP_STEP_MEAN')
column_name = 'PAD_TEMP_STEP_MEAN'

# 그래프 크기 설정
plt.figure(figsize=(12, 5))

# 1️⃣ 히스토그램 (데이터 분포 확인)
plt.subplot(1, 3, 1)
plt.hist(df[column_name], bins=30, edgecolor='black', alpha=0.7)
plt.title(f'Histogram of {column_name}')
plt.xlabel(column_name)
plt.ylabel('Frequency')

# 2️⃣ 박스플롯 (이상치 확인)
plt.subplot(1, 3, 2)
plt.boxplot(df[column_name], vert=True)
plt.title(f'Boxplot of {column_name}')
plt.ylabel(column_name)

# 3️⃣ 시계열 그래프 (시간에 따른 변화, BASE_DT가 있는 경우)
if 'BASE_DT' in df.columns:
    df['BASE_DT'] = pd.to_datetime(df['BASE_DT'])  # 날짜 변환
    df_sorted = df.sort_values(by='BASE_DT')  # 날짜 정렬

    plt.subplot(1, 3, 3)
    plt.plot(df_sorted['BASE_DT'], df_sorted[column_name], marker='o', linestyle='-')
    plt.title(f'Time Series of {column_name}')
    plt.xlabel('Date')
    plt.ylabel(column_name)
    plt.xticks(rotation=45)  # 날짜 라벨 회전

# 그래프 출력
plt.tight_layout()
plt.show()