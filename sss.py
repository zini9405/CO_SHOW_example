import streamlit as st
import datetime

# 📌 오늘 날짜 가져오기
today = datetime.date.today()

# 📌 시작 날짜 & 종료 날짜 설정
start_date_default = today - datetime.timedelta(days=30)  # 기본값: 30일 전
end_date_default = today  # 기본값: 오늘

# 📌 날짜 슬라이더 (datetime.date 타입으로 설정)
start_date_zdd, end_date_zdd = st.sidebar.slider(
    'Select Date Range',
    min_value=today - datetime.timedelta(days=365),  # 최소값 (1년 전)
    max_value=today,  # 최대값 (오늘)
    value=(start_date_default, end_date_default),  # 기본값
    format="YYYY-MM-DD"
)

# 📌 날짜 타입 확인 (디버깅용)
st.write(f"Selected Dates: {start_date_zdd} ~ {end_date_zdd}")