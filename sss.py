---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)
Cell In[15], line 176
    173     visualize_attention_scores(model, dataset.feature_names)
    175 if __name__ == "__main__":
--> 176     main()

Cell In[15], line 173
    162 model = FullMultiLevelTransformer(input_dim=32, eqp_vocab_size=len(eqp_mapping), d_model=256, nhead=4, num_layers=4, dim_feedforward=512)
    163 # predictions, true_labels = test_model(model, test_loader, device, save_path, dataset.quantile_transformer)
    164 
    165 # # 그래프 출력
   (...)
    171 
    172 # visualize_eqp_embedding(model, eqp_mapping)
--> 173 visualize_attention_scores(model, dataset.feature_names)

Cell In[15], line 94
     92 attention_maps = model.get_attention_maps()
     93 print(attention_maps)
---> 94 avg_attention = torch.mean(attention_maps[-1], dim=1).squeeze().detach().cpu().numpy()  # 마지막 레이어 사용
     95 sorted_indices = np.argsort(-avg_attention)  # 중요도 순서대로 정렬
     97 print("\nFeature Importance:")

IndexError: list index out of range
