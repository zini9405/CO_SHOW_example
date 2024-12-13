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

# 2x2 레이아웃 생성
st.subheader("Visualized Data (2x2 Layout)")
fig, axs = plt.subplots(2, 2, figsize=(15, 12))

# 0,0: Filtered Data Graph (Date Range)
if not filtered_df.empty:
    axs[0, 0].plot(pd.to_datetime(filtered_df['HST_REG_DTTM']), filtered_df['Pred'], label='Pred', marker='o', linestyle='-')
    axs[0, 0].plot(pd.to_datetime(filtered_df['HST_REG_DTTM']), filtered_df['SFQR_AFS2'], label='SFQR_AFS2', marker='x', linestyle='-')
    axs[0, 0].set_xlabel('Date and Time')
    axs[0, 0].set_ylabel('Values')
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # R² 스코어 계산 및 표시
    r2_date = r2_score(filtered_df['SFQR_AFS2'], filtered_df['Pred'])
    axs[0, 0].set_title(f"Filtered Data Graph (R² = {r2_date:.4f})")
else:
    axs[0, 0].set_title("No data for Filtered Data Graph")
    axs[0, 0].axis('off')

# 0,1: Scatter Plot
if not filtered_df.empty:
    axs[0, 1].scatter(filtered_df['SFQR_AFS2'], filtered_df['Pred'], alpha=0.6, c='blue')
    axs[0, 1].set_xlabel('SFQR_AFS2')
    axs[0, 1].set_ylabel('Pred')
    axs[0, 1].grid(True)

    # R² 스코어 계산 및 표시
    r2_scatter = r2_score(filtered_df['SFQR_AFS2'], filtered_df['Pred'])
    axs[0, 1].set_title(f"Scatter Plot (R² = {r2_scatter:.4f})")
else:
    axs[0, 1].set_title("No data for Scatter Plot")
    axs[0, 1].axis('off')

# 1,0: Filtered Data Table
if not filtered_df.empty:
    st.subheader("Filtered Data Based on Date")
    st.dataframe(filtered_df)  # 날짜 기준 필터링된 데이터 표시
else:
    st.warning("No data available for the selected date range.")

# WAF_ID 선택 (1,1 그래프 위에 표시)
if not filtered_df.empty:
    st.subheader("WAF_ID Selection")
    waf_id_options = filtered_df['WAF_ID'].unique()
    selected_waf_id = st.selectbox('WAF_ID', options=waf_id_options)

    # WAF_ID로 데이터 필터링
    filtered_df_waf = filtered_df[filtered_df['WAF_ID'] == selected_waf_id]
else:
    st.warning("No data available for the selected date range.")
    filtered_df_waf = pd.DataFrame()

# 1,1: Filtered Data Based on WAF_ID
if not filtered_df_waf.empty:
    axs[1, 1].plot(pd.to_datetime(filtered_df_waf['HST_REG_DTTM']), filtered_df_waf['Pred'], label='Pred', marker='o', linestyle='-')
    axs[1, 1].plot(pd.to_datetime(filtered_df_waf['HST_REG_DTTM']), filtered_df_waf['SFQR_AFS2'], label='SFQR_AFS2', marker='x', linestyle='-')
    axs[1, 1].set_xlabel('Date and Time')
    axs[1, 1].set_ylabel('Values')
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    # R² 스코어 계산 및 표시
    r2_waf = r2_score(filtered_df_waf['SFQR_AFS2'], filtered_df_waf['Pred'])
    axs[1, 1].set_title(f"Filtered Data by WAF_ID (R² = {r2_waf:.4f})")
else:
    axs[1, 1].set_title("No data for Filtered Data by WAF_ID")
    axs[1, 1].axis('off')

# Layout 출력
plt.tight_layout()
st.pyplot(fig)