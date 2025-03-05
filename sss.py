import pandas as pd

# CSV 파일 로드
df = pd.read_csv("x.csv")

# '_Unnamed: 0'이 포함된 모든 열 삭제
df = df.drop(columns=[col for col in df.columns if "_Unnamed: 0" in col], errors="ignore")

# 모든 값이 NaN인 열 삭제
df = df.dropna(axis=1, how="all")

# 열 값이 동일한 경우 중복된 열 삭제
df = df.T.drop_duplicates().T  # Transpose하여 중복된 열을 찾고 다시 원래 형태로 변환

# 결과 저장
df.to_csv("cleaned_x.csv", index=False)

# 변환된 데이터 출력
import ace_tools as tools
tools.display_dataframe_to_user(name="Cleaned Data", dataframe=df)