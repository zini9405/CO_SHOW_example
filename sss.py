---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[20], line 162
    158     print("Variable Importance:", importance_dict)
    161 if __name__ == "__main__":
--> 162     main()

Cell In[20], line 119
    117 print(true_labels)
    118 print(r2_score(true_labels, predictions))
--> 119 predictions = predictions.flattenen()
    120 true_labels = true_labels.flattenen()
    121 # 데이터프레임 생성

AttributeError: 'numpy.ndarray' object has no attribute 'flattenen'
