import streamlit as st

# 새로고침 여부를 저장하는 상태 변수 추가
if "refresh_zdd" not in st.session_state:
    st.session_state["refresh_zdd"] = False

# ZDD 페이지로 이동하면서 새로고침하는 함수
def refresh_and_go_to_zdd():
    st.session_state["refresh_zdd"] = True
    st.experimental_rerun()

# 새로고침 상태가 True이면 ZDD 페이지로 이동
if st.session_state["refresh_zdd"]:
    st.session_state["refresh_zdd"] = False  # 상태 초기화
    st.switch_page("./pages/ZDD.py")

st.set_page_config(
    page_title='SMART TTTM',
    page_icon='📊',
    initial_sidebar_state='collapsed',
    layout='wide'
)

def set_title(title):
    return f"<h2 style='text-align: center; color: black;'>{title}</h2>"

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
        st.switch_page(f'./pages/wiresaw.py')

    is_BOW_clicked = st.button(
        label='BOW',
        use_container_width=True,
        disabled=True
    )
    if is_BOW_clicked:
        pass

    is_NANO_clicked = st.button(
        label='NANO',
        use_container_width=True,
        disabled=True
    )
    if is_NANO_clicked:
        pass

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
        st.switch_page(f'./pages/SFQR.py')

    is_ZDD_clicked = st.button(
        label='ZDD',
        use_container_width=True
    )
    if is_ZDD_clicked:
        refresh_and_go_to_zdd()  # 새로고침 후 ZDD 페이지로 이동

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

for _ in range(9):
    st.write('')

st.write('문의사항: DS1팀 이주영T, DS1팀 한승철P, DS2팀 유광남P')