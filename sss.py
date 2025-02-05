import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import datetime

# Streamlit 페이지 설정
st.set_page_config(
    page_title="ZDDFRONTMEAN Analysis",
    page_icon="📊",
    layout="wide"
)

# Streamlit UI 제목
st.title("📊 ZDDFRONTMEAN_01_AFS2 Analysis")
st.markdown("### EQP 별 ZDDFRONTMEAN 트렌드")

# 날짜 선택
start_date = st.sidebar.date_input("Start date", datetime.date.today() - datetime.timedelta(days=60))
end_date = st.sidebar.date_input("End date", datetime.date.today())

# 데이터 가져오기 (예제 데이터)
df_eqp = st.session_state['df_Y'][(st.session_state['df_Y'].HST_REG_DTTM.between(start_date, end_date, inclusive='both'))]

# 비교할 EQP_ID 선택
eqp_1 = st.sidebar.selectbox("Select EQP_1", df_eqp['EQP_ID_MODULE_NAME'].unique())
eqp_2 = st.sidebar.selectbox("Select EQP_2", df_eqp['EQP_ID_MODULE_NAME'].unique())

# 4개 Column 레이아웃 생성
col1, col2, col3, col4 = st.columns(4)

# ✅ **첫 번째 그래프 (EQP_1 Mean ZDD Bar Chart)**
with col1:
    df_eqp1 = df_eqp[df_eqp.EQP_ID_MODULE_NAME == eqp_1].sort_values('HST_REG_DTTM')
    df_eqp_grp1 = df_eqp1.groupby(['HST_REG_DTTM', 'WAF_ID']).agg({'ZDDFRONTMEAN_01_AFS2':'mean'}).reset_index()
    df_eqp_grp1['MEAN_ZDDFRONTMEAN_01_AFS2'] = df_eqp_grp1.groupby('HST_REG_DTTM')['ZDDFRONTMEAN_01_AFS2'].transform('mean')

    # Bar Chart 생성
    chart1 = alt.Chart(df_eqp_grp1).mark_bar().encode(
        x=alt.X('HST_REG_DTTM:T', axis=alt.Axis(format='%Y-%m-%d', labelAngle=90), title=None),
        y=alt.Y('MEAN_ZDDFRONTMEAN_01_AFS2:Q', title='ZDD Mean'),
        tooltip=['HST_REG_DTTM', 'MEAN_ZDDFRONTMEAN_01_AFS2']
    ).properties(title=f'EQP: {eqp_1}')
    
    st.altair_chart(chart1, use_container_width=True)

# ✅ **두 번째 그래프 (EQP_2 Mean ZDD Bar Chart)**
with col2:
    df_eqp2 = df_eqp[df_eqp.EQP_ID_MODULE_NAME == eqp_2].sort_values('HST_REG_DTTM')
    df_eqp_grp2 = df_eqp2.groupby(['HST_REG_DTTM', 'WAF_ID']).agg({'ZDDFRONTMEAN_01_AFS2':'mean'}).reset_index()
    df_eqp_grp2['MEAN_ZDDFRONTMEAN_01_AFS2'] = df_eqp_grp2.groupby('HST_REG_DTTM')['ZDDFRONTMEAN_01_AFS2'].transform('mean')

    # Bar Chart 생성
    chart2 = alt.Chart(df_eqp_grp2).mark_bar().encode(
        x=alt.X('HST_REG_DTTM:T', axis=alt.Axis(format='%Y-%m-%d', labelAngle=90), title=None),
        y=alt.Y('MEAN_ZDDFRONTMEAN_01_AFS2:Q', title='ZDD Mean'),
        tooltip=['HST_REG_DTTM', 'MEAN_ZDDFRONTMEAN_01_AFS2']
    ).properties(title=f'EQP: {eqp_2}')
    
    st.altair_chart(chart2, use_container_width=True)

# ✅ **세 번째 그래프 (EQP_1 점 그래프 - WAF_ID 기준)**
with col3:
    df_eqp_grp1['HST_REG_DTTM'] = pd.to_datetime(df_eqp_grp1['HST_REG_DTTM']).dt.strftime('%Y-%m-%d')
    df_eqp_grp1 = df_eqp_grp1.sort_values(['HST_REG_DTTM', 'WAF_ID']).reset_index(drop=True)
    df_eqp_grp1['x_index'] = df_eqp_grp1.groupby('HST_REG_DTTM').cumcount()

    # Scatter Plot (점 그래프)
    chart3 = alt.Chart(df_eqp_grp1).mark_circle(size=80).encode(
        x=alt.X('x_index:Q', title="WAF_ID Number"),
        y=alt.Y('ZDDFRONTMEAN_01_AFS2:Q', title="ZDDFRONTMEAN_01_AFS2"),
        color=alt.Color('HST_REG_DTTM:N', title="날짜"),
        tooltip=['HST_REG_DTTM', 'WAF_ID', 'ZDDFRONTMEAN_01_AFS2']
    ).interactive()

    st.altair_chart(chart3, use_container_width=True)

# ✅ **네 번째 그래프 (EQP_2 점 그래프 - WAF_ID 기준)**
with col4:
    df_eqp_grp2['HST_REG_DTTM'] = pd.to_datetime(df_eqp_grp2['HST_REG_DTTM']).dt.strftime('%Y-%m-%d')
    df_eqp_grp2 = df_eqp_grp2.sort_values(['HST_REG_DTTM', 'WAF_ID']).reset_index(drop=True)
    df_eqp_grp2['x_index'] = df_eqp_grp2.groupby('HST_REG_DTTM').cumcount()

    # Scatter Plot (점 그래프)
    chart4 = alt.Chart(df_eqp_grp2).mark_circle(size=80).encode(
        x=alt.X('x_index:Q', title="WAF_ID Number"),
        y=alt.Y('ZDDFRONTMEAN_01_AFS2:Q', title="ZDDFRONTMEAN_01_AFS2"),
        color=alt.Color('HST_REG_DTTM:N', title="날짜"),
        tooltip=['HST_REG_DTTM', 'WAF_ID', 'ZDDFRONTMEAN_01_AFS2']
    ).interactive()

    st.altair_chart(chart4, use_container_width=True)

# --- 3. X 중요도 ---
st.markdown('---')
st.markdown('### 3. X 인자 중요도')
st.markdown(f'{eqp_1} - FDC 인자')