---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
Cell In[56], line 61
     59 if __name__ == "__main__":
     60     set_seed(42)
---> 61     main()

Cell In[56], line 48
     45 save_path = "model_weights_GBIR_25312.pth"
     46 device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
---> 48 train_model_inputs(
     49     model=model,
     50     train_loader=train_loader,
     51     val_loader=val_loader,
     52     criterion=nn.HuberLoss(delta=1.0),
     53     optimizer=optimizer,
     54     num_epochs=2000,
     55     device=device,
     56     save_path=save_path
     57 )

Cell In[54], line 16
     12 batch_features, batch_eqp_ids, batch_labels = zip(*batch_)
     13 batch_features, batch_eqp_ids, batch_labels = (
     14     torch.stack(batch_features).to(device), torch.stack(batch_eqp_ids).to(device), torch.stack(batch_labels).to(device)
     15 )
---> 16 outputs, attention_scores = model(batch_features, batch_eqp_ids)
     17 # print('batch_labels', batch_labels)
     18 loss = criterion(outputs.squeeze(), batch_labels)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\nn\modules\module.py:1532, in Module._wrapped_call_impl(self, *args, **kwargs)
   1530     return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]
   1531 else:
-> 1532     return self._call_impl(*args, **kwargs)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\nn\modules\module.py:1541, in Module._call_impl(self, *args, **kwargs)
   1536 # If we don't have any hooks, we want to skip the rest of the logic in
   1537 # this function, and just call forward.
   1538 if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks
   1539         or _global_backward_pre_hooks or _global_backward_hooks
   1540         or _global_forward_hooks or _global_forward_pre_hooks):
-> 1541     return forward_call(*args, **kwargs)
   1543 try:
   1544     result = None

Cell In[14], line 88
     87 def forward(self, features, eqp_ids):
---> 88     feature_embed = self.feature_embedding(features)
     90     eqp_embed = self.eqp_embedding(eqp_ids).unsqueeze(1)  # (batch_size, 1, d_model)
     92     combined_features = feature_embed + eqp_embed  # Combine feature and equipment embeddings

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\nn\modules\module.py:1532, in Module._wrapped_call_impl(self, *args, **kwargs)
   1530     return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]
   1531 else:
-> 1532     return self._call_impl(*args, **kwargs)

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\nn\modules\module.py:1541, in Module._call_impl(self, *args, **kwargs)
   1536 # If we don't have any hooks, we want to skip the rest of the logic in
   1537 # this function, and just call forward.
   1538 if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks
   1539         or _global_backward_pre_hooks or _global_backward_hooks
   1540         or _global_forward_hooks or _global_forward_pre_hooks):
-> 1541     return forward_call(*args, **kwargs)
   1543 try:
   1544     result = None

File c:\Users\SKsiltron\AppData\Local\Programs\Python\Python312\Lib\site-packages\torch\nn\modules\linear.py:116, in Linear.forward(self, input)
    115 def forward(self, input: Tensor) -> Tensor:
--> 116     return F.linear(input, self.weight, self.bias)

RuntimeError: mat1 and mat2 shapes cannot be multiplied (4608x28 and 1x256)
