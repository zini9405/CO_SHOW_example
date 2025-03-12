    print(predictions)
[[0.09037495]
 [0.08781517]
 [0.08375616]
 ...
 [0.09084177]
 [0.09238058]
 [0.07158369]]


    print(true_labels)
[[0.06857984]
 [0.08680185]
 [0.11073644]
 ...
 [0.10623648]
 [0.09829003]
 [0.08247983]]

    dfff = pd.DataFrame({'predictions': predictions, 'true_labels': true_labels})
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
Cell In[19], line 161
    157     print("Variable Importance:", importance_dict)
    160 if __name__ == "__main__":
--> 161     main()

Cell In[19], line 121
    118 print(r2_score(true_labels, predictions))
    120 # 데이터프레임 생성
--> 121 dfff = pd.DataFrame({'predictions': predictions, 'true_labels': true_labels})
    123 # CSV 파일로 저장
    124 csv_filename = "predictions_vs_labels.csv"

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\frame.py:778, in DataFrame.__init__(self, data, index, columns, dtype, copy)
    772     mgr = self._init_mgr(
    773         data, axes={"index": index, "columns": columns}, dtype=dtype, copy=copy
    774     )
    776 elif isinstance(data, dict):
    777     # GH#38939 de facto copy defaults to False only in non-dict cases
--> 778     mgr = dict_to_mgr(data, index, columns, dtype=dtype, copy=copy, typ=manager)
    779 elif isinstance(data, ma.MaskedArray):
    780     from numpy.ma import mrecords

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\pandas\core\internals\construction.py:503, in dict_to_mgr(data, index, columns, dtype, typ, copy)
...
--> 664         raise ValueError("Per-column arrays must each be 1-dimensional")
    666 if not indexes and not raw_lengths:
    667     raise ValueError("If using all scalar values, you must pass an index")

ValueError: Per-column arrays must each be 1-dimensional
