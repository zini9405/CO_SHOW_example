import pandas as pd

# CSV 파일 읽기
data = pd.read_csv("a.csv")

# 데이터를 변환 (MTRL_ITEM_CODE를 컬럼명으로 확장)
result = data.groupby("SUBLOT_ID").agg(lambda x: list(x) if x.name != "MTRL_ITEM_CODE" else x).reset_index()

# 새로운 컬럼 생성: MTRL_ITEM_CODE별 변수 값 매칭
final_data = pd.DataFrame({"SUBLOT_ID": result["SUBLOT_ID"]})

for idx, row in result.iterrows():
    sublot_id = row["SUBLOT_ID"]
    codes = row["MTRL_ITEM_CODE"]  # code 열 값들
    for code in codes:
        for col in data.columns:
            if col not in ["SUBLOT_ID", "MTRL_ITEM_CODE"]:
                new_col_name = f"{code}_{col}"
                if new_col_name not in final_data:
                    final_data[new_col_name] = None
                final_data.at[idx, new_col_name] = row[col]

# 결과 저장
final_data.to_csv("transformed_a.csv", index=False)

# 변환된 데이터프레임 출력
import ace_tools as tools
tools.display_dataframe_to_user(name="Transformed Data", dataframe=final_data)