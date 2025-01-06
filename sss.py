---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
Cell In[15], line 204
    202 if __name__ == "__main__":
    203     set_seed(42)
--> 204     main()

Cell In[15], line 190
    187 save_path = "model_weights_ZDD_250106.pth"
    188 device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
--> 190 train_model_inputs(
    191     model=model,
    192     train_loader=train_loader,
    193     val_loader=val_loader,
    194     criterion=criterion,
    195     optimizer=optimizer,
    196     num_epochs=100,
    197     device=device,
    198     log_dir="logs",
    199     save_path=save_path
    200 )

Cell In[15], line 114
    111 model.train()
    112 train_loss = 0.0
...
     51 label = torch.tensor(self.labels[idx], dtype=torch.float32)
---> 52 eqp_id = torch.tensor(self.eqp_ids[idx], dtype=torch.long)  # 임베딩에 사용될 ID
     53 return features, eqp_id, label

RuntimeError: value cannot be converted to type int64 without overflow
