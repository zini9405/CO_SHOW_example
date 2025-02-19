import streamlit as st

# 📌 현재 페이지 상태 관리 (초기값 설정)
if 'selected_page' not in st.session_state:
    st.session_state['selected_page'] = None  # 선택된 페이지 초기화

if 'pred_page' not in st.session_state:
    st.session_state['pred_page'] = None  # pred 페이지 상태 초기화

# 📌 상태 초기화 함수 (불필요한 세션 데이터 제거)
def reset_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]  # 모든 세션 키 삭제 (완전 초기화)
    st.session_state['selected_page'] = None
    st.session_state['pred_page'] = None

with col34:
    # 📌 SFQR 버튼 클릭
    is_SFQR_clicked = st.button(label='SFQR', use_container_width=True)
    if is_SFQR_clicked:
        reset_state()  # 기존 세션 초기화
        st.session_state['selected_page'] = 'SFQR'  # SFQR 선택 상태 저장
        st.switch_page(f'./pages/SFQR.py')

    # 📌 ZDD 버튼 클릭
    is_ZDD_clicked = st.button(label='ZDD', use_container_width=True)
    if is_ZDD_clicked:
        reset_state()  # 기존 세션 초기화
        st.session_state['selected_page'] = 'ZDD'  # ZDD 선택 상태 저장
        st.switch_page(f'./pages/ZDD.py')

# 📌 SFQR_pred.py 및 ZDD_pred.py 실행 전에 상태 체크
if st.session_state.get('selected_page') == 'SFQR' and st.session_state.get('pred_page') is None:
    st.session_state['pred_page'] = 'SFQR_pred'
    st.switch_page(f'./pages/SFQR_pred.py')

elif st.session_state.get('selected_page') == 'ZDD' and st.session_state.get('pred_page') is None:
    st.session_state['pred_page'] = 'ZDD_pred'
    st.switch_page(f'./pages/ZDD_pred.py')