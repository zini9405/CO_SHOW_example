import pandas as pd

# 파일 로드 (불필요한 인덱스 열 제거)
df_a = pd.read_csv("a.csv").drop(columns=[col for col in ["Unnamed: 0", "index"] if col in df_a])
df_b = pd.read_csv("b.csv").drop(columns=[col for col in ["Unnamed: 0", "index"] if col in df_b])
df_c = pd.read_csv("c.csv").drop(columns=[col for col in ["Unnamed: 0", "index"] if col in df_c])

# id 기준으로 병합 (중복 컬럼 방지)
merged_df = df_a.merge(df_b, on="SUBLOT_ID", how="outer", suffixes=("_a", "_b"))\
                .merge(df_c, on="SUBLOT_ID", how="outer", suffixes=("", "_c"))

# 다시 중복된 컬럼 제거 (필요하면 조정 가능)
merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]

# 결과 저장
merged_df.to_csv("merged_data.csv", index=False)

# 변환된 데이터 출력
import ace_tools as tools
tools.display_dataframe_to_user(name="Merged Data", dataframe=merged_df)