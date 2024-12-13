# 날짜 기준 필터링된 데이터 표시
st.subheader("Filtered Data Based on Date")
if not filtered_df.empty:
    st.dataframe(filtered_df)
else:
    st.warning("No data available for the selected date range.")

[0,0] [0,1]은 잘했어, 

근데 1,0은 위에 코드가 들어가야돼. 그리고 waf_id필터도 1,1 그래프 위에 있어야돼.
