AttributeError: 'StreamlitPage' object has no attribute 'current_page'
Traceback:
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\runtime\scriptrunner\exec_code.py", line 88, in exec_func_with_error_handling
    result = func()
             ^^^^^^
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\runtime\scriptrunner\script_runner.py", line 579, in code_to_exec
    exec(code, module.__dict__)
File "C:\Users\SKsiltron\Desktop\smart_final\smart-tttm\front.py", line 40, in <module>
    if st.session_state['current_page'] != pg.current_page:
