---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[19], line 178
    175     visualize_attention_scores(model, dataset.feature_names)
    177 if __name__ == "__main__":
--> 178     main()

Cell In[19], line 175
    172 # Forward 실행
    173 _ = model(sample_features, sample_eqp_ids)
--> 175 visualize_attention_scores(model, dataset.feature_names)

Cell In[19], line 101
     99 print("\nFeature Importance:")
    100 for idx in sorted_indices:
--> 101     print(f"{feature_names[idx]}: {avg_attention[idx]:.4f}")
    103 # 시각화
    104 plt.figure(figsize=(10, 6))

TypeError: unsupported format string passed to numpy.ndarray.__format__
