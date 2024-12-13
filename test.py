import streamlit as st
import pandas as pd
import json
import re
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.metrics import r2_score

# 자연스러운 정렬을 위한 함수
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

# JSON 파일 로드 함수
def load_json(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)

# Session state 초기화
if 'df_Y' not in st.session_state:
    st.session_state['df_Y'] = pd.read_csv('./asset/SFQR/merged_file.csv', low_memory=False)

if 'SFQR_json' not in st.session_state:
    st.session_state['SFQR_json'] = load_json('./asset/SFQR/SFQR_jsonSFQR.json')

# Streamlit 앱 구성
st.title("SFQR Dashboard")

# EQP 선택
with st.sidebar:
    st.subheader('EQP SFQR')
    eqp_options = sorted(st.session_state['SFQR_json']['EQP_ID_MODULE_NAME'], key=natural_sort_key)
    selected_eqp = st.selectbox('EQP NAME', options=eqp_options, index=0)

# 선택된 EQP에 따라 데이터 필터링
filtered_df = st.session_state['df_Y'][st.session_state['df_Y']['EQP_ID_MODULE_NAME'] == selected_eqp]

# 날짜와 시간 선택
st.subheader("Date and Time Selection")
if not filtered_df.empty:
    min_datetime = pd.to_datetime(filtered_df['HST_REG_DTTM']).min()
    max_datetime = pd.to_datetime(filtered_df['HST_REG_DTTM']).max()

    # 명시적으로 datetime 객체를 전달하여 슬라이더 동작 수정
    start_datetime, end_datetime = st.slider(
        "Select Date and Time",
        min_value=min_datetime.to_pydatetime(),
        max_value=max_datetime.to_pydatetime(),
        value=(min_datetime.to_pydatetime(), max_datetime.to_pydatetime()),
        format="YYYY-MM-DD HH:mm"
    )

    # 선택된 날짜 범위로 데이터 필터링
    filtered_df = filtered_df[
        (pd.to_datetime(filtered_df['HST_REG_DTTM']) >= start_datetime) &
        (pd.to_datetime(filtered_df['HST_REG_DTTM']) <= end_datetime)
    ]
else:
    st.warning("No data available for the selected EQP.")

# 0,0: Filtered Data Graph (Date Range)
st.subheader("Filtered Data Graph (Date Range)")
if not filtered_df.empty:
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(pd.to_datetime(filtered_df['HST_REG_DTTM']), filtered_df['Pred'], label='Pred', marker='o', linestyle='-')
    ax1.plot(pd.to_datetime(filtered_df['HST_REG_DTTM']), filtered_df['SFQR_AFS2'], label='SFQR_AFS2', marker='x', linestyle='-')
    ax1.set_xlabel('Date and Time')
    ax1.set_ylabel('Values')
    ax1.legend()
    ax1.grid(True)

    # R² 스코어 계산 및 표시
    r2_date = r2_score(filtered_df['SFQR_AFS2'], filtered_df['Pred'])
    ax1.set_title(f"Filtered Data Graph (R² = {r2_date:.4f})")

    st.pyplot(fig1)
else:
    st.warning("No data available for the selected date range.")

# 0,1: Scatter Plot
st.subheader("Scatter Plot (Filtered Data - Pred vs SFQR_AFS2)")
if not filtered_df.empty:
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.scatter(filtered_df['SFQR_AFS2'], filtered_df['Pred'], alpha=0.6, c='blue')
    ax2.set_xlabel('SFQR_AFS2')
    ax2.set_ylabel('Pred')
    ax2.grid(True)

    # R² 스코어 계산 및 표시
    r2_scatter = r2_score(filtered_df['SFQR_AFS2'], filtered_df['Pred'])
    ax2.set_title(f"Scatter Plot (R² = {r2_scatter:.4f})")

    st.pyplot(fig2)
else:
    st.warning("No data available for the scatter plot.")

# 1,0: Filtered Data Table
st.subheader("Filtered Data Table")
if not filtered_df.empty:
    st.dataframe(filtered_df)
else:
    st.warning("No data available for the selected date range.")

# 1,1: Filtered Data Based on WAF_ID
if not filtered_df.empty:
    st.subheader("WAF_ID Selection")
    waf_id_options = filtered_df['WAF_ID'].unique()
    selected_waf_id = st.selectbox('WAF_ID', options=waf_id_options)

    # WAF_ID로 데이터 필터링
    filtered_df_waf = filtered_df[filtered_df['WAF_ID'] == selected_waf_id]

    st.subheader("Filtered Data by WAF_ID")
    if not filtered_df_waf.empty:
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        ax3.plot(pd.to_datetime(filtered_df_waf['HST_REG_DTTM']), filtered_df_waf['Pred'], label='Pred', marker='o', linestyle='-')
        ax3.plot(pd.to_datetime(filtered_df_waf['HST_REG_DTTM']), filtered_df_waf['SFQR_AFS2'], label='SFQR_AFS2', marker='x', linestyle='-')
        ax3.set_xlabel('Date and Time')
        ax3.set_ylabel('Values')
        ax3.legend()
        ax3.grid(True)

        # R² 스코어 계산 및 표시
        r2_waf = r2_score(filtered_df_waf['SFQR_AFS2'], filtered_df_waf['Pred'])
        ax3.set_title(f"Filtered Data by WAF_ID (R² = {r2_waf:.4f})")

        st.pyplot(fig3)
    else:
        st.warning("No data available for the selected WAF_ID.")
else:
    st.warning("No data available for the selected date range.")