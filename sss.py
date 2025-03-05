import pandas as pd

# 파일 로드
df_a = pd.read_csv("a.csv")
df_b = pd.read_csv("b.csv")
df_c = pd.read_csv("c.csv")

# id 기준으로 병합
merged_df = df_a.merge(df_b, on="id", how="outer").merge(df_c, on="id", how="outer")

# 병합된 데이터 출력
import ace_tools as tools
tools.display_dataframe_to_user(name="Merged Data", dataframe=merged_df)

# 병합된 데이터 저장
merged_df.to_csv("merged_data.csv", index=False)