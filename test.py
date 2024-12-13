import streamlit as st
import pandas as pd
import json
import re
import matplotlib.pyplot as plt
from datetime import datetime

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
# filtered_df = st.session_state['df_Y'][st.session_state['df_Y']['EQP_ID_MODULE_NAME'] == 'CENC16B']

# 날짜 선택
# 날짜와 시간 선택
st.subheader("날짜와 시간 선택")
if not filtered_df.empty:
    min_datetime = pd.to_datetime(filtered_df['HST_REG_DTTM']).min()
    max_datetime = pd.to_datetime(filtered_df['HST_REG_DTTM']).max()

    # 명시적으로 datetime 객체를 전달하여 슬라이더 동작 수정
    start_datetime, end_datetime = st.slider(
        "날짜와 시간을 선택하세요",
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
    st.warning("선택된 EQP에 대한 데이터가 없습니다.")


# 필터링된 데이터(웨이퍼로 필터링 전) 그래프
st.subheader("날짜 기준 필터링된 데이터 그래프")
if not filtered_df.empty:
    fig1, ax1 = plt.subplots(figsize=(30, 6))
    ax1.plot(pd.to_datetime(filtered_df['HST_REG_DTTM']), filtered_df['Pred'], label='Pred', marker='o')
    ax1.plot(pd.to_datetime(filtered_df['HST_REG_DTTM']), filtered_df['SFQR_AFS2'], label='SFQR_AFS2', marker='x')
    ax1.set_xlabel('Date and Time')
    ax1.set_ylabel('Values')
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)
else:
    st.warning("날짜 기준 필터링된 데이터가 없습니다.")


# WAF_ID 선택
if not filtered_df.empty:
    st.subheader("WAF_ID 선택")
    waf_id_options = filtered_df['WAF_ID'].unique()
    selected_waf_id = st.selectbox('WAF_ID', options=waf_id_options)

    # WAF_ID로 데이터 필터링
    filtered_df = filtered_df[filtered_df['WAF_ID'] == selected_waf_id]
else:
    st.warning("선택된 날짜 범위에 대한 데이터가 없습니다.")

# WAF_ID로 필터링된 데이터 그래프
st.subheader("WAF_ID 기준 필터링된 데이터 그래프")
if not filtered_df.empty:
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(pd.to_datetime(filtered_df['HST_REG_DTTM']), filtered_df['Pred'], label='Pred', marker='o')
    ax2.plot(pd.to_datetime(filtered_df['HST_REG_DTTM']), filtered_df['SFQR_AFS2'], label='SFQR_AFS2', marker='x')
    ax2.set_xlabel('Date and Time')
    ax2.set_ylabel('Values')
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)
else:
    st.warning("WAF_ID 기준 필터링된 데이터가 없습니다.")



산점도 그래프도 추가하는 코드도 구현해주고 날짜 기준으로 필터링된 waf_id로 변경해줘. 지금은 전체 waf_id로 구현돼어 있어. 그리고 r2_score 값도 추가해줘

