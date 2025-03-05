import pandas as pd

# CSV 파일 읽기
df = pd.read_csv("a.csv")

# 중복된 (name, code) 조합 확인
duplicate_entries = df.groupby(["name", "code"]).filter(lambda x: len(x) > 1)

# 중복된 값이 있는 경우 출력
if not duplicate_entries.empty:
    print("중복된 name, code 조합이 있는 데이터:")
    print(duplicate_entries)

# 중복이 있는 경우 첫 번째 값만 선택하여 처리
df = df.groupby(["name", "code"]).first().reset_index()

# 데이터를 변환하기 위해 피벗 형태로 재구성
result = df.pivot(index="name", columns="code")

# 새로운 열 이름 생성 (code 값을 포함)
result.columns = [f"{col[1]}_{col[0]}" for col in result.columns]

# 인덱스 초기화
result.reset_index(inplace=True)

# 변환된 데이터 저장
result.to_csv("transformed_a.csv", index=False)

# 변환된 데이터 출력
import ace_tools as tools
tools.display_dataframe_to_user(name="Transformed Data", dataframe=result)