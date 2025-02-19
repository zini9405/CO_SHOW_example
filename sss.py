KeyError: 'st.session_state has no key "selected_page". Did you forget to initialize it? More info: https://docs.streamlit.io/develop/concepts/architecture/session-state#initialization'
Traceback:
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\runtime\scriptrunner\exec_code.py", line 88, in exec_func_with_error_handling
    result = func()
             ^^^^^^
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\runtime\scriptrunner\script_runner.py", line 579, in code_to_exec
    exec(code, module.__dict__)
File "C:\Users\SKsiltron\Desktop\smart_final\smart-tttm\front.py", line 46, in <module>
    st.session_state['current_page'] = st.session_state['selected_page']  # 현재 페이지 업데이트
                                       ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\runtime\state\session_state_proxy.py", line 100, in __getitem__
    return get_session_state()[key]
           ~~~~~~~~~~~~~~~~~~~^^^^^
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\runtime\state\safe_session_state.py", line 94, in __getitem__
    return self._state[key]
           ~~~~~~~~~~~^^^^^
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\runtime\state\session_state.py", line 457, in __getitem__
    raise KeyError(_missing_key_error_message(key))
