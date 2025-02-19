import streamlit as st

# 📌 현재 페이지 상태 관리 (없으면 기본값으로 None 설정)
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = None

with col34:
    # 📌 SFQR 버튼 클릭
    is_SFQR_clicked = st.button(label='SFQR', use_container_width=True)
    if is_SFQR_clicked:
        st.session_state['current_page'] = 'SFQR'
        st.switch_page(f'./pages/SFQR.py')

    # 📌 ZDD 버튼 클릭
    is_ZDD_clicked = st.button(label='ZDD', use_container_width=True)
    if is_ZDD_clicked:
        st.session_state['current_page'] = 'ZDD'
        st.switch_page(f'./pages/ZDD.py')

# 📌 SFQR_pred와 ZDD_pred 실행 전 상태 체크
if 'current_page' in st.session_state:
    if st.session_state['current_page'] == 'SFQR':
        st.switch_page(f'./pages/SFQR_pred.py')
    elif st.session_state['current_page'] == 'ZDD':
        st.switch_page(f'./pages/ZDD_pred.py')