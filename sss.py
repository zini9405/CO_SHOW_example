import streamlit as st

st.set_page_config(page_title="EPI Analysis", layout="wide")

st.markdown("<h2 style='text-align: center;'> EPI Analysis </h2>", unsafe_allow_html=True)

# 📌 현재 선택된 하위 페이지를 저장
if 'selected_epi_page' not in st.session_state:
    st.session_state['selected_epi_page'] = "sfqr"

# 📌 하위 메뉴 버튼 생성
col1, col2 = st.columns(2)

with col1:
    if st.button("SFQR Analysis", use_container_width=True):
        st.session_state['selected_epi_page'] = "sfqr"

with col2:
    if st.button("ZDD Analysis", use_container_width=True):
        st.session_state['selected_epi_page'] = "zdd"

st.markdown("---")

# 📌 선택된 하위 페이지 로드 (기존 파일 유지)
if st.session_state['selected_epi_page'] == "sfqr":
    exec(open("pages/SFQR.py").read())

elif st.session_state['selected_epi_page'] == "zdd":
    exec(open("pages/ZDD.py").read())





import streamlit as st

st.set_page_config(page_title="DSP Analysis", layout="wide")

st.markdown("<h2 style='text-align: center;'> DSP Analysis </h2>", unsafe_allow_html=True)

# 📌 현재 선택된 하위 페이지를 저장
if 'selected_dsp_page' not in st.session_state:
    st.session_state['selected_dsp_page'] = "gbir"

# 📌 하위 메뉴 버튼 생성
col1 = st.columns(1)[0]

with col1:
    if st.button("GBIR Analysis", use_container_width=True):
        st.session_state['selected_dsp_page'] = "gbir"

st.markdown("---")

# 📌 선택된 하위 페이지 로드 (기존 파일 유지)
if st.session_state['selected_dsp_page'] == "gbir":
    exec(open("pages/GBIR.py").read())





import streamlit as st

st.set_page_config(page_title="Wire Saw", layout="wide")

st.markdown("<h2 style='text-align: center;'> Wire Saw Dashboard </h2>", unsafe_allow_html=True)

# 📌 현재 선택된 하위 페이지를 저장
if 'selected_wiresaw_page' not in st.session_state:
    st.session_state['selected_wiresaw_page'] = "wiresaw"

# 📌 하위 메뉴 버튼 생성
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Wire Saw", use_container_width=True):
        st.session_state['selected_wiresaw_page'] = "wiresaw"

with col2:
    if st.button("Wire Saw EQP", use_container_width=True):
        st.session_state['selected_wiresaw_page'] = "wiresaw_eqp"

with col3:
    if st.button("Wire Saw Warp", use_container_width=True):
        st.session_state['selected_wiresaw_page'] = "wiresaw_warp"

st.markdown("---")

# 📌 선택된 하위 페이지 로드 (기존 파일 유지)
if st.session_state['selected_wiresaw_page'] == "wiresaw":
    exec(open("pages/wiresaw.py").read())

elif st.session_state['selected_wiresaw_page'] == "wiresaw_eqp":
    exec(open("pages/wiresaw_eqp.py").read())

elif st.session_state['selected_wiresaw_page'] == "wiresaw_warp":
    exec(open("pages/wiresaw_warp.py").read())








import streamlit as st

st.set_page_config(page_title="SMART TTTM", page_icon="📊", layout="wide")

st.sidebar.title("Navigation")

# 📌 현재 선택된 메인 페이지 저장
if 'selected_main_page' not in st.session_state:
    st.session_state['selected_main_page'] = "Main"

# 📌 메인 메뉴 버튼
main_pages = {
    "Main": "main",
    "Wire Saw": "wiresaw",
    "DSP Analysis": "dsp_analysis",
    "DSP Quality": "dsp_quality",
    "EPI Analysis": "epi_analysis",
    "EPI Quality": "epi_quality"
}

selected_main_page = st.sidebar.radio("Select Page", list(main_pages.keys()), index=0)
st.session_state['selected_main_page'] = main_pages[selected_main_page]

st.markdown("---")

# 📌 선택된 메인 페이지 동적 로드
if st.session_state['selected_main_page'] == "wiresaw":
    exec(open("pages/wiresaw.py").read())
elif st.session_state['selected_main_page'] == "dsp_analysis":
    exec(open("pages/dsp_analysis.py").read())
elif st.session_state['selected_main_page'] == "dsp_quality":
    exec(open("pages/dsp_quality.py").read())
elif st.session_state['selected_main_page'] == "epi_analysis":
    exec(open("pages/epi_analysis.py").read())
elif st.session_state['selected_main_page'] == "epi_quality":
    exec(open("pages/epi_quality.py").read())
else:
    exec(open("main.py").read())









import streamlit as st

st.set_page_config(
    page_title="SMART TTTM",
    page_icon="📊",
    layout="wide"
)

def set_title(title):
    return f"<h2 style='text-align: center; color: black;'>{title}</h2>"

st.image('./asset/wire_saw_summary/front/banner.PNG', use_column_width=True)
st.markdown('---')

# 📌 메인 메뉴 타이틀
col11, col12, col13, col14 = st.columns(4)

with col11:
    st.markdown(set_title('WIRE SAW'), unsafe_allow_html=True)

with col12:
    st.markdown(set_title('DSP'), unsafe_allow_html=True)

with col13:
    st.markdown(set_title('FCS'), unsafe_allow_html=True)

with col14:
    st.markdown(set_title('EPI'), unsafe_allow_html=True)

# 📌 메인 페이지 이미지
col21, col22, col23, col24 = st.columns(4)

with col21: st.image('./asset/wire_saw_summary/front/wiresaw.gif')
with col22: st.image('./asset/wire_saw_summary/front/dsp.gif')
with col23: st.image('./asset/wire_saw_summary/front/fcs.gif')
with col24: st.image('./asset/wire_saw_summary/front/epi.gif')

# 📌 각 메인 카테고리 버튼
col31, col32, col33, col34 = st.columns(4)

with col31:
    if st.button('Wire Saw', use_container_width=True):
        st.session_state['selected_main_page'] = "wiresaw"
        st.rerun()

with col32:
    if st.button('DSP Analysis', use_container_width=True):
        st.session_state['selected_main_page'] = "dsp_analysis"
        st.rerun()

with col33:
    if st.button('DSP Quality', use_container_width=True):
        st.session_state['selected_main_page'] = "dsp_quality"
        st.rerun()

with col34:
    if st.button('EPI Analysis', use_container_width=True):
        st.session_state['selected_main_page'] = "epi_analysis"
        st.rerun()

st.markdown("---")
st.write('문의사항: Smart제조AI팀 이주영T, Smart제조AI팀 이채현P, Smart제조AI팀 이준원P')