# WAF_ID별 개수 계산
waf_id_counts = df_first["WAF_ID"].value_counts()

# 개수가 9개 이하인 WAF_ID만 선택
valid_waf_ids = waf_id_counts[waf_id_counts <= 9].index

# 해당 WAF_ID만 필터링하여 새로운 데이터프레임 생성
df_filtered = df_first[df_first["WAF_ID"].isin(valid_waf_ids)]

# 결과 출력
print(df_filtered)
