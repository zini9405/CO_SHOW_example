import streamlit as st
import pandas as pd
import altair as alt

# Streamlit 페이지 설정
st.set_page_config(
    page_title="ZDDFRONTMEAN Analysis",
    page_icon="📊",
    layout="wide"
)

# 데이터 로드 (여기서는 예제 데이터 사용)
# 실제 데이터 사용 시: sub_df_eqp2 = pd.read_csv("파일경로.csv")
sub_df_eqp2 = pd.DataFrame({
    "HST_REG_DTTM": ["2024-09-30"] * 5 + ["2024-10-16"] * 5,
    "WAF_ID": ["A15QAG76SLD6", "A15QAG77SLA5", "A15QAG78SLE7", "A15QAG79SLB6", "A15W9C60SLH0",
               "B20064HUSL", "B20063LCSL", "B20063LBSL", "B20063LDSL", "B20064HVSL"],
    "ZDDFRONTMEAN_01_AFS2": [-10.29, -14.82, -13.13, -12.70, -11.20,
                              -22.97, -35.28, -32.52, -35.44, -22.02]
})

# HST_REG_DTTM별 WAF_ID 개수 계산
df_grouped = sub_df_eqp2.groupby('HST_REG_DTTM')['WAF_ID'].count().reset_index()
df_grouped.rename(columns={'WAF_ID': 'waf_count'}, inplace=True)

# 기존 데이터프레임과 병합하여 x축에 WAF_ID 개수를 추가
sub_df_eqp2 = sub_df_eqp2.merge(df_grouped, on='HST_REG_DTTM')

# Streamlit UI
st.title("📊 ZDDFRONTMEAN_01_AFS2 Analysis")
st.markdown("### HST_REG_DTTM별 WAF_ID 개수와 ZDDFRONTMEAN 트렌드")

# Altair 차트 생성
chart = alt.Chart(sub_df_eqp2).mark_circle(size=80).encode(
    x=alt.X('waf_count:Q', title="WAF_ID 개수"),
    y=alt.Y('ZDDFRONTMEAN_01_AFS2:Q', title="ZDDFRONTMEAN_01_AFS2"),
    color=alt.Color('HST_REG_DTTM:N', title="날짜"),
    tooltip=['HST_REG_DTTM', 'waf_count', 'ZDDFRONTMEAN_01_AFS2']
).interactive()

# Streamlit에 차트 출력
st.altair_chart(chart, use_container_width=True)