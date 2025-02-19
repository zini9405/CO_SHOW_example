import streamlit as st
import datetime

# 📌 상태 관리: 다른 페이지에서 이동하면 상태 초기화
if 'current_page' not in st.session_state or st.session_state['current_page'] != 'GBIR Analysis':
    st.session_state.clear()
    st.session_state['current_page'] = 'GBIR Analysis'

# 📌 오늘 날짜 가져오기
today = datetime.date.today()

# 📌 기본 날짜 설정 (datetime.date 형식 유지)
start_date_default = today - datetime.timedelta(days=30)  # 30일 전
end_date_default = today  # 오늘

# 📌 날짜 슬라이더 (datetime.date 타입으로 설정)
start_date_gbir, end_date_gbir = st.sidebar.slider(
    'Select Date Range',
    min_value=today - datetime.timedelta(days=365),  # 최소값 (1년 전)
    max_value=today,  # 최대값 (오늘)
    value=(start_date_default, end_date_default),  # 기본값 (datetime.date 형식 유지)
    format="YYYY-MM-DD"
)

# 📌 선택된 날짜 확인 (디버깅용)
st.write(f"Selected Dates: {start_date_gbir} ~ {end_date_gbir}")


with col32:
    is_GBIR_clicked = st.button(
        label='GBIR',
        use_container_width=True
    )
    if is_GBIR_clicked:
        st.session_state.clear()  # 상태 초기화
        st.session_state['current_page'] = 'GBIR Analysis'
        st.switch_page(f'./pages/GBIR.py')

with col34:
    is_SFQR_clicked = st.button(
        label='SFQR',
        use_container_width=True
    )
    if is_SFQR_clicked:
        st.session_state.clear()  # 상태 초기화
        st.session_state['current_page'] = 'SFQR Analysis'
        st.switch_page(f'./pages/SFQR.py')

    is_ZDD_clicked = st.button(
        label='ZDD',
        use_container_width=True
    )
    if is_ZDD_clicked:
        st.session_state.clear()  # 상태 초기화
        st.session_state['current_page'] = 'ZDD Analysis'
        st.switch_page(f'./pages/ZDD.py')
