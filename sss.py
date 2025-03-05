import pandas as pd

# CSV 파일 로드
df = pd.read_csv("x.csv")

# 삭제할 값 목록
values_to_remove = ["CP-MCLT", "DUMMY-ALL", "BULK-FE", "ENGR-NIP"]

# 특정 열에서 해당 값을 가진 행 삭제
df = df[~df["LIFT-PIN1_PROD_ID"].isin(values_to_remove)]
df = df[~df["LIFT-PIN2_PROD_ID"].isin(values_to_remove)]
df = df[~df["LIFT-PIN3_PROD_ID"].isin(values_to_remove)]

# 결과 저장
df.to_csv("filtered_x.csv", index=False)

# 변환된 데이터 출력
import ace_tools as tools
tools.display_dataframe_to_user(name="Filtered Data", dataframe=df)