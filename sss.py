import streamlit as st

# 📌 현재 페이지 상태 관리 (기본값 설정)
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = None

# 📌 상태 초기화 함수 (클릭 시 기존 정보 제거)
def reset_state():
    st.session_state.clear()
    st.session_state['current_page'] = None

with st.sidebar:
    is_SFQR_clicked = st.button(label='SFQR', use_container_width=True)
    if is_SFQR_clicked:
        reset_state()  # 이전 상태 초기화
        st.session_state['current_page'] = 'SFQR'
        st.switch_page(f'./pages/SFQR.py')

    is_ZDD_clicked = st.button(label='ZDD', use_container_width=True)
    if is_ZDD_clicked:
        reset_state()  # 이전 상태 초기화
        st.session_state['current_page'] = 'ZDD'
        st.switch_page(f'./pages/ZDD.py')

# 📌 SFQR_pred.py 및 ZDD_pred.py 실행 전에 상태 체크
if 'current_page' in st.session_state:
    if st.session_state['current_page'] == 'SFQR':
        st.switch_page(f'./pages/SFQR_pred.py')
    elif st.session_state['current_page'] == 'ZDD':
        st.switch_page(f'./pages/ZDD_pred.py')