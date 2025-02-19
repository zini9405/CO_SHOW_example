TypeError: unsupported operand type(s) for -: 'datetime.date' and 'str'
Traceback:
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\runtime\scriptrunner\exec_code.py", line 88, in exec_func_with_error_handling
    result = func()
             ^^^^^^
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\runtime\scriptrunner\script_runner.py", line 579, in code_to_exec
    exec(code, module.__dict__)
File "C:\Users\SKsiltron\Desktop\smart_final\smart-tttm\front.py", line 49, in <module>
    pg.run()
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\navigation\page.py", line 303, in run
    exec(code, module.__dict__)
File "C:\Users\SKsiltron\Desktop\smart_final\smart-tttm\pages\GBIR.py", line 36, in <module>
    end_date_gbir_gbir, end_date_gbir = st.sidebar.slider('Date',
                                        ^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\runtime\metrics_util.py", line 409, in wrapped_func
    result = non_optional_func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\elements\widgets\slider.py", line 502, in slider
    return self._slider(
           ^^^^^^^^^^^^^
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\elements\widgets\slider.py", line 676, in _slider
    ) and max_value - min_value < timedelta(days=1):


똑같이 이 문제가 발생해. main.py 코드 수정해야되는가? 쫌 제대로 알려줘

main.py 코드 

import streamlit as st
base_url = 'http://10.150.9.121/tttm_go_back_address'

st.set_page_config(
    page_title = 'SMART TTTM',
    page_icon = '📊',
    initial_sidebar_state = 'collapsed',
    layout = 'wide'
)

def set_title(title):
    return f"<h2 style = 'text-align: center; color: black;'>{title}</h1>"

st.image('./asset/wire_saw_summary/front/banner.PNG', use_column_width = True)
st.markdown('---')


col11, col12, col13, col14 = st.columns(4)

with col11:
    st.markdown(set_title('WIRE SAW'), unsafe_allow_html = True)

with col12:
    st.markdown(set_title('DSP'), unsafe_allow_html = True)

with col13:
    st.markdown(set_title('FCS'), unsafe_allow_html = True)

with col14:
    st.markdown(set_title('EPI'), unsafe_allow_html = True)


col21, col22, col23, col24 = st.columns(4)

with col21: st.image('./asset/wire_saw_summary/front/wiresaw.gif')
with col22: st.image('./asset/wire_saw_summary/front/dsp.gif')
with col23: st.image('./asset/wire_saw_summary/front/fcs.gif')
with col24: st.image('./asset/wire_saw_summary/front/epi.gif')


col31, col32, col33, col34 = st.columns(4)

with col31:
    is_WARP_clicked = st.button(
        label = 'WARP', 
        use_container_width = True
    )
    if is_WARP_clicked:
        st.switch_page(f'./pages/wiresaw.py')

    is_BOW_clicked = st.button(
        label = 'BOW', 
        use_container_width = True, 
        disabled = True
    )
    if is_BOW_clicked:
        #st.switch_page(f'./pages/wiresaw.py')
        pass

    is_NANO_clicked = st.button(
        label = 'NANO', 
        use_container_width = True, 
        disabled = True
    )
    if is_NANO_clicked:
        #st.switch_page(f'./pages/wiresaw.py')
        pass

with col32:

    is_SFQR_clicked = st.button(
        label = 'GBIR', 
        use_container_width = True
    )
    if is_SFQR_clicked:
        st.switch_page(f'./pages/GBIR.py')

    st.link_button(
        label = 'SFQR', 
        url = '', 
        use_container_width = True, 
        disabled = True
    )
    st.link_button(
        label = 'ESFQR', 
        url = '', 
        use_container_width = True, 
        disabled = True
    )

with col33:
    st.link_button(
        label = 'LLS (47 nm)', 
        url = '', 
        use_container_width = True, 
        disabled = True
    )
    st.link_button(
        label = 'METAL', 
        url = '', 
        use_container_width = True, 
        disabled = True
    )

with col34:
    is_SFQR_clicked = st.button(
        label = 'SFQR', 
        use_container_width = True
    )
    if is_SFQR_clicked:
        st.switch_page(f'./pages/SFQR.py')

    is_ZDD_clicked = st.button(
        label = 'ZDD', 
        use_container_width = True
    )
    if is_ZDD_clicked:
        st.switch_page(f'./pages/ZDD.py')


    st.link_button(
        label = 'SITE NT', 
        url = '', 
        use_container_width = True, 
        disabled = True
    )
    st.link_button(
        label = 'DELTA TEMP', 
        url = '', 
        use_container_width = True, 
        disabled = True
    )

for _ in range(9):
    st.write('')
#st.write('해당 페이지는 품질 현황과 장비의 TTTM Point 제안을 위해 개발되었습니다.')
st.write('문의사항: Smart제조AI팀 이주영T, Smart제조AI팀 이채현P, Smart제조AI팀 이준원P')
