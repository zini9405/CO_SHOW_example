Batch data shape: torch.Size([8, 3, 13, 34])
Batch labels shape: torch.Size([8])
Batch masks shape: torch.Size([8, 3, 13, 34])
DataLoader created successfully with 1339751 samples.

A module that was compiled using NumPy 1.x cannot be run in
NumPy 2.1.3 as it may crash. To support both 1.x and 2.x
versions of NumPy, modules must be compiled with NumPy 2.0.
Some module may need to rebuild instead e.g. with 'pybind11>=2.12'.

If you are a user of the module, the easiest solution will be to
downgrade to 'numpy<2' or try to upgrade the affected module.
We expect that some modules will need time to support NumPy 2.

Traceback (most recent call last):  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\SKsiltron\AppData\Roaming\Python\Python312\site-packages\ipykernel_launcher.py", line 18, in <module>
    app.launch_new_instance()
  File "C:\Users\SKsiltron\AppData\Roaming\Python\Python312\site-packages\traitlets\config\application.py", line 1075, in launch_instance
    app.start()
  File "C:\Users\SKsiltron\AppData\Roaming\Python\Python312\site-packages\ipykernel\kernelapp.py", line 739, in start
    self.io_loop.start()
  File "C:\Users\SKsiltron\AppData\Roaming\Python\Python312\site-packages\tornado\platform\asyncio.py", line 205, in start
    self.asyncio_loop.run_forever()
  File "c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 641, in run_forever
    self._run_once()
  File "c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 1986, in _run_once
    handle._run()
  File "c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\asyncio\events.py", line 88, in _run
...
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_28188\2436220519.py:44: UserWarning: Failed to initialize NumPy: _ARRAY_API not found (Triggered internally at ..\torch\csrc\utils\tensor_numpy.cpp:84.)
  torch.tensor(masked_data_window, dtype=torch.float32),
C:\Users\SKsiltron\AppData\Local\Temp\ipykernel_28188\2436220519.py:46: DeprecationWarning: In future, it will be an error for 'np.bool' scalars to be interpreted as an index
  torch.tensor(mask, dtype=torch.bool),  # Include the mask for further processing if needed
