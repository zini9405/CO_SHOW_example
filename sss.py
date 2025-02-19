import streamlit as st

# 📌 현재 페이지 상태 관리 (초기값 설정)
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Main'  # 기본 페이지

# 📌 상태 초기화 함수 (불필요한 세션 데이터 제거)
def reset_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]  # 모든 세션 키 삭제 (완전 초기화)
    st.session_state['current_page'] = 'Main'

# 📌 페이지 네비게이션 버튼 추가
st.sidebar.title("Navigation")

# 📌 페이지 이동 함수
def go_to_page(page_name, file_name):
    reset_state()
    st.session_state['current_page'] = page_name
    st.switch_page(file_name)

# 📌 페이지 이동 버튼 추가
if st.sidebar.button("SFQR Analysis"):
    go_to_page('SFQR Analysis', 'pages/SFQR.py')

if st.sidebar.button("ZDD Analysis"):
    go_to_page('ZDD Analysis', 'pages/ZDD.py')

if st.sidebar.button("SFQR Quality"):
    go_to_page('SFQR Quality', 'pages/SFQR_pred.py')

if st.sidebar.button("ZDD Quality"):
    go_to_page('ZDD Quality', 'pages/ZDD_pred.py')

if st.sidebar.button("GBIR Analysis"):
    go_to_page('GBIR Analysis', 'pages/GBIR.py')

if st.sidebar.button("GBIR Quality"):
    go_to_page('GBIR Quality', 'pages/GBIR_pred.py')

# 📌 현재 선택된 페이지에 따라 자동 전환
if st.session_state['current_page'] == 'SFQR Analysis':
    st.switch_page('pages/SFQR.py')

elif st.session_state['current_page'] == 'ZDD Analysis':
    st.switch_page('pages/ZDD.py')

elif st.session_state['current_page'] == 'SFQR Quality':
    st.switch_page('pages/SFQR_pred.py')

elif st.session_state['current_page'] == 'ZDD Quality':
    st.switch_page('pages/ZDD_pred.py')

elif st.session_state['current_page'] == 'GBIR Analysis':
    st.switch_page('pages/GBIR.py')

elif st.session_state['current_page'] == 'GBIR Quality':
    st.switch_page('pages/GBIR_pred.py')