import streamlit as st
import pandas as pd
import altair as alt
import datetime

# Streamlit 페이지 설정
st.set_page_config(
    page_title="EQP 데이터 비교",
    page_icon="📊",
    layout="wide"
)

# 데이터 로드
if 'df_Y' not in st.session_state:
    df_Y = pd.read_csv('./asset/wire_saw_summary/sfqr/all_minmax_with_predictions_and_importance.csv', low_memory=False)
    df_Y['HST_REG_DTTM'] = pd.to_datetime(df_Y['HST_REG_DTTM']).dt.strftime('%Y-%m-%d')  # 날짜 포맷 변환
    st.session_state['df_Y'] = df_Y

df_Y = st.session_state['df_Y']

# Streamlit UI 제목
st.markdown("<h2 style='text-align: center;'>📊 EQP 데이터 비교 (ZDDFRONTMEAN_01_AFS2 vs Pred)</h2>", unsafe_allow_html=True)

# EQP_ID_MODULE_NAME 선택
eqp_list = df_Y['EQP_ID_MODULE_NAME'].unique()
selected_eqp = st.sidebar.selectbox("EQP_ID_MODULE_NAME 선택", eqp_list)

# 선택한 EQP에 해당하는 데이터 필터링
df_filtered_eqp = df_Y[df_Y['EQP_ID_MODULE_NAME'] == selected_eqp]

# HST_REG_DTTM 선택 (해당 EQP에서 날짜 목록만 가져오기)
date_list = df_filtered_eqp['HST_REG_DTTM'].unique()
selected_date = st.sidebar.selectbox("HST_REG_DTTM 선택", date_list)

# 선택한 날짜의 데이터 필터링
df_filtered_date = df_filtered_eqp[df_filtered_eqp['HST_REG_DTTM'] == selected_date]

# ✅ 먼저 해당 날짜의 모든 WAF_ID 데이터를 그래프로 표시
df_melted_all = df_filtered_date.melt(id_vars=['HST_REG_DTTM', 'WAF_ID'], value_vars=['ZDDFRONTMEAN_01_AFS2', 'pred'],
                                      var_name='Variable', value_name='Value')

# 📊 WAF_ID별 그래프 (전체 데이터 표시)
chart_all = alt.Chart(df_melted_all).mark_circle(size=80).encode(
    x=alt.X('HST_REG_DTTM:T', title="날짜"),
    y=alt.Y('Value:Q', title="값"),
    color=alt.Color('Variable:N', title="변수 종류"),
    tooltip=['HST_REG_DTTM', 'WAF_ID', 'Variable', 'Value']
).properties(title=f'📊 {selected_date} - 전체 WAF_ID 데이터')

# 그래프 출력
st.altair_chart(chart_all, use_container_width=True)

# ✅ Streamlit selectbox로 WAF_ID 선택
selected_waf = st.sidebar.selectbox("WAF_ID 선택", df_filtered_date['WAF_ID'].unique())

# 선택한 WAF_ID 데이터 필터링
df_final = df_filtered_date[df_filtered_date['WAF_ID'] == selected_waf]

# 데이터 확인 및 개별 그래프 생성
if df_final.empty:
    st.warning("선택한 WAF_ID에 대한 데이터가 없습니다.")
else:
    # ✅ 📌 Altair 시각화를 위한 데이터 변환
    df_melted = df_final.melt(id_vars=['HST_REG_DTTM'], value_vars=['ZDDFRONTMEAN_01_AFS2', 'pred'], var_name='Variable', value_name='Value')

    # ✅ 📊 선택한 WAF_ID의 상세 그래프
    chart = alt.Chart(df_melted).mark_line(point=True).encode(
        x=alt.X('HST_REG_DTTM:T', title="날짜"),
        y=alt.Y('Value:Q', title="값"),
        color=alt.Color('Variable:N', title="변수 종류"),
        tooltip=['HST_REG_DTTM', 'Variable', 'Value']
    ).properties(title=f'📊 {selected_waf} - ZDDFRONTMEAN_01_AFS2 vs Pred')

    # 개별 그래프 출력
    st.altair_chart(chart, use_container_width=True)

    # ✅ 📋 선택한 WAF_ID의 데이터 테이블
    st.markdown(f"### 📋 {selected_waf}의 상세 데이터")
    st.dataframe(df_final)