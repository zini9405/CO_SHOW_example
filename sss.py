import streamlit as st

# 세션 상태에 현재 페이지 정보 저장 (초기값: "Home")
if "page" not in st.session_state:
    st.session_state.page = "Home"

col34 = st.columns(1)[0]  # col34 정의 (여러 개의 컬럼이 아니라 단일 컬럼으로 가정)

with col34:
    is_SFQR_clicked = st.button(
        label='SFQR', 
        use_container_width=True
    )
    if is_SFQR_clicked:
        st.session_state.page = "SFQR"
        st.experimental_rerun()

    is_ZDD_clicked = st.button(
        label='ZDD', 
        use_container_width=True
    )
    if is_ZDD_clicked:
        st.session_state.page = "ZDD"
        st.experimental_rerun()

    st.link_button(
        label='SITE NT', 
        url='', 
        use_container_width=True, 
        disabled=True
    )
    st.link_button(
        label='DELTA TEMP', 
        url='', 
        use_container_width=True, 
        disabled=True
    )

# 페이지 전환 로직
if st.session_state.page == "SFQR":
    st.page_link("pages/SFQR.py")

elif st.session_state.page == "ZDD":
    st.page_link("pages/ZDD.py")