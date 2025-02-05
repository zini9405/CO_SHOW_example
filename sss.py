import streamlit as st
import pandas as pd
import altair as alt

# Streamlit 페이지 설정
st.set_page_config(
    page_title="ZDDFRONTMEAN Analysis",
    page_icon="📊",
    layout="wide"
)

# 예제 데이터 로드 (실제 데이터 사용 시 파일에서 읽어오기)
sub_df_eqp2 = pd.DataFrame({
    "HST_REG_DTTM": ["2024-09-30", "2024-09-30", "2024-09-30", "2024-09-30", "2024-09-30",
                     "2024-10-16", "2024-10-16", "2024-10-16", "2024-10-16", "2024-10-16"],
    "WAF_ID": ["A15QAG76SLD6", "A15QAG77SLA5", "A15QAG78SLE7", "A15QAG79SLB6", "A15W9C60SLH0",
               "B20064HUSL", "B20063LCSL", "B20063LBSL", "B20063LDSL", "B20064HVSL"],
    "ZDDFRONTMEAN_01_AFS2": [-10.29, -14.82, -13.13, -12.70, -11.20,
                              -22.97, -35.28, -32.52, -35.44, -22.02]
})

# 날짜 형식 변환 (YYYY-MM-DD)
sub_df_eqp2['HST_REG_DTTM'] = pd.to_datetime(sub_df_eqp2['HST_REG_DTTM']).dt.strftime('%Y-%m-%d')

# WAF_ID 개수 순서대로 x축 값 할당 (0부터 시작하는 인덱스)
sub_df_eqp2 = sub_df_eqp2.sort_values('HST_REG_DTTM').reset_index(drop=True)
sub_df_eqp2['x_index'] = range(len(sub_df_eqp2))  # 0부터 시작하는 인덱스

# Streamlit UI
st.title("📊 ZDDFRONTMEAN_01_AFS2 Analysis")
st.markdown("### WAF_ID 개수별 ZDDFRONTMEAN_01_AFS2 값")

# Altair 차트 생성
chart = alt.Chart(sub_df_eqp2).mark_circle(size=80).encode(
    x=alt.X('x_index:Q', title="Index (0부터 시작)"),
    y=alt.Y('ZDDFRONTMEAN_01_AFS2:Q', title="ZDDFRONTMEAN_01_AFS2"),
    color=alt.Color('HST_REG_DTTM:N', title="날짜"),
    tooltip=['HST_REG_DTTM', 'WAF_ID', 'ZDDFRONTMEAN_01_AFS2']
).interactive()

# Streamlit에 차트 출력
st.altair_chart(chart, use_container_width=True)