# FIRST_FLOW_GROUP 값이 "FIRST"인 행만 필터링
df_first = df_6300[df_6300["FIRST_FLOW_GROUP"] == "FIRST"]

# 결과 출력
print(df_first)