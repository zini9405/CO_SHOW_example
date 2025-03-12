MemoryError                               Traceback (most recent call last)
Cell In[10], line 148
    144     print("Variable Importance:", importance_dict)
    147 if __name__ == "__main__":
--> 148     main()

Cell In[10], line 101
     98 predictions, true_labels, attention_scores = test_model(model, train_loader_, device, save_path, train_loader.quantile_transformer)
    100 # 그래프 출력
--> 101 correlation, predictions, true_labels = calculate_correlation(predictions, true_labels)
    102 print(correlation)
    103 print(predictions)

Cell In[10], line 46
     43 true_labels = torch.tensor(true_labels).detach().cpu().numpy().reshape(-1, 1)
     45 # 상관계수 계산
---> 46 correlation = np.corrcoef(true_labels, predictions)[0, 1]
     47 print(f"Correlation Coefficient (True Labels vs Predictions): {correlation:.4f}")
     48 return correlation, predictions, true_labels

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\numpy\lib\function_base.py:2889, in corrcoef(x, y, rowvar, bias, ddof, dtype)
   2885 if bias is not np._NoValue or ddof is not np._NoValue:
   2886     # 2015-03-15, 1.10
   2887     warnings.warn('bias and ddof have no effect and are deprecated',
...
-> 2747 c = dot(X, X_T.conj())
   2748 c *= np.true_divide(1, fact)
   2749 return c.squeeze()

MemoryError: Unable to allocate 862. GiB for an array with shape (340212, 340212) and data type float64
