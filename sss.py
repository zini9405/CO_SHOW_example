TypeError: unsupported operand type(s) for -: 'datetime.date' and 'str'
Traceback:
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\runtime\scriptrunner\exec_code.py", line 88, in exec_func_with_error_handling
    result = func()
             ^^^^^^
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\runtime\scriptrunner\script_runner.py", line 579, in code_to_exec
    exec(code, module.__dict__)
File "C:\Users\SKsiltron\Desktop\smart_final\smart-tttm\front.py", line 44, in <module>
    pg.run()
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\navigation\page.py", line 303, in run
    exec(code, module.__dict__)
File "C:\Users\SKsiltron\Desktop\smart_final\smart-tttm\pages\ZDD.py", line 31, in <module>
    start_date_zdd, end_date_zdd = st.sidebar.slider('Date',
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\runtime\metrics_util.py", line 409, in wrapped_func
    result = non_optional_func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\elements\widgets\slider.py", line 502, in slider
    return self._slider(
           ^^^^^^^^^^^^^
File "C:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\streamlit\elements\widgets\slider.py", line 676, in _slider
    ) and max_value - min_value < timedelta(days=1):


여전히 충돌이 되서 안돼...
