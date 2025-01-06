---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[3], line 209
    207 if __name__ == "__main__":
    208     set_seed(42)
--> 209     main()

Cell In[3], line 192
    189 save_path = "model_weights_ZDD1111.pth"
    190 device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
--> 192 train_model_inputs(
    193     model=model,
    194     train_loader=train_loader,
    195     val_loader=val_loader,
    196     criterion=nn.HuberLoss(delta=1.0),
    197     optimizer=optimizer,
    198     num_epochs=100,
    199     device=device,
    200     log_dir="logs",
    201     save_path=save_path
    202 )
    204 feature_names = df.columns.tolist()
    205 visualize_attention_maps(model, feature_names)

Cell In[3], line 108
...
   1707     if name in modules:
   1708         return modules[name]
-> 1709 raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

AttributeError: 'TransformerEncoderLayer' object has no attribute 'attn'
