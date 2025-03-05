import pandas as pd

# CSV 파일 읽기
df = pd.read_csv("a.csv")

# 변환할 새로운 데이터프레임 생성
result = df.groupby("name").apply(lambda group: group.drop(columns=["name"]).set_index("code").stack())\
          .unstack(level=[1, 2])

# 새로운 열 이름을 생성 (code 값을 포함)
result.columns = [f"{code}_{col}" for col, code in result.columns]

# 인덱스 초기화
result.reset_index(inplace=True)

# 결과 저장
result.to_csv("transformed_a.csv", index=False)

# 변환된 데이터프레임 출력
import ace_tools as tools
tools.display_dataframe_to_user(name="Transformed Data", dataframe=result)