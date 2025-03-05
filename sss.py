import pandas as pd

# CSV 파일 로드
df = pd.read_csv("x.csv")

# '_Unnamed: 0'이 포함된 모든 열 삭제
df = df.drop(columns=[col for col in df.columns if "_Unnamed: 0" in col], errors="ignore")

# 값이 빈 값(NaN)인 열 삭제
df = df.dropna(axis=1, how="all")  # 특정 열이 아니라, 전체 열 중 NaN만 포함된 열 삭제

# 결과 저장
df.to_csv("cleaned_x.csv", index=False)

# 변환된 데이터 출력
import ace_tools as tools
tools.display_dataframe_to_user(name="Cleaned Data", dataframe=df)