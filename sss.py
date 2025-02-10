import streamlit as st

base_url = 'http://10.150.9.121/tttm_go_back_address'

st.set_page_config(
    page_title='SMART TTTM',
    page_icon='📊',
    initial_sidebar_state='collapsed',
    layout='wide'
)

def set_title(title):
    return f"<h2 style='text-align: center; color: black;'>{title}</h2>"

# 세션 상태 초기화 (초기 페이지 설정)
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

st.image('./asset/wire_saw_summary/front/banner.PNG', use_column_width=True)
st.markdown('---')

col11, col12, col13, col14 = st.columns(4)

with col11:
    st.markdown(set_title('WIRE SAW'), unsafe_allow_html=True)

with col12:
    st.markdown(set_title('DSP'), unsafe_allow_html=True)

with col13:
    st.markdown(set_title('FCS'), unsafe_allow_html=True)

with col14:
    st.markdown(set_title('EPI'), unsafe_allow_html=True)

col21, col22, col23, col24 = st.columns(4)

with col21:
    st.image('./asset/wire_saw_summary/front/wiresaw.gif')
with col22:
    st.image('./asset/wire_saw_summary/front/dsp.gif')
with col23:
    st.image('./asset/wire_saw_summary/front/fcs.gif')
with col24:
    st.image('./asset/wire_saw_summary/front/epi.gif')

col31, col32, col33, col34 = st.columns(4)

with col31:
    is_WARP_clicked = st.button(
        label='WARP',
        use_container_width=True
    )
    if is_WARP_clicked:
        st.session_state["page"] = "WARP"
        st.experimental_rerun()

    is_BOW_clicked = st.button(
        label='BOW',
        use_container_width=True,
        disabled=True
    )

    is_NANO_clicked = st.button(
        label='NANO',
        use_container_width=True,
        disabled=True
    )

with col32:
    st.link_button(
        label='GBIR',
        url='',
        use_container_width=True,
        disabled=True
    )
    st.link_button(
        label='SFQR',
        url='',
        use_container_width=True,
        disabled=True
    )
    st.link_button(
        label='ESFQR',
        url='',
        use_container_width=True,
        disabled=True
    )

with col33:
    st.link_button(
        label='LLS (47 nm)',
        url='',
        use_container_width=True,
        disabled=True
    )
    st.link_button(
        label='METAL',
        url='',
        use_container_width=True,
        disabled=True
    )

with col34:
    is_SFQR_clicked = st.button(
        label='SFQR',
        use_container_width=True
    )
    if is_SFQR_clicked:
        st.session_state["page"] = "SFQR"
        st.experimental_rerun()

    is_ZDD_clicked = st.button(
        label='ZDD',
        use_container_width=True
    )
    if is_ZDD_clicked:
        st.session_state["page"] = "ZDD"
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

# 🔹 페이지 전환 로직
if st.session_state["page"] == "SFQR":
    st.page_link("pages/SFQR.py")

elif st.session_state["page"] == "ZDD":
    st.page_link("pages/ZDD.py")

elif st.session_state["page"] == "WARP":
    st.page_link("pages/wiresaw.py")

for _ in range(9):
    st.write('')

st.write('문의사항: DS1팀 이주영T, DS1팀 한승철P, DS2팀 유광남P')