---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[31], line 204
    202 if __name__ == "__main__":
    203     set_seed(42)
--> 204     main()

Cell In[31], line 187
    184 save_path = "model_weights_ZDD1111.pth"
    185 device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
--> 187 train_model_inputs(
    188     model=model,
    189     train_loader=train_loader,
    190     val_loader=val_loader,
    191     criterion=nn.HuberLoss(delta=1.0),
    192     optimizer=optimizer,
    193     num_epochs=100,
    194     device=device,
    195     log_dir="logs",
    196     save_path=save_path
    197 )
    199 feature_names = df.columns.tolist()
    200 visualize_attention_maps(model, feature_names)

Cell In[31], line 99
...
---> 50     features = torch.tensor(self.features[idx], dtype=torch.float32)
     51     label = torch.tensor(self.labels[idx], dtype=torch.float32)
     52     eqp_id = torch.tensor(self.eqp_ids[idx], dtype=torch.long)

TypeError: can't convert np.ndarray of type numpy.object_. The only supported types are: float64, float32, float16, complex64, complex128, int64, int32, int16, int8, uint64, uint32, uint16, uint8, and bool.
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
