RuntimeError                              Traceback (most recent call last)
Cell In[32], line 78
     76 if __name__ == "__main__":
     77     set_seed(42)
---> 78     main()

Cell In[32], line 65
     62 device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
     63 criterion = nn.CrossEntropyLoss()
---> 65 train_model_inputs(
     66     model=model,
     67     train_loader=train_loader,
     68     val_loader=val_loader,
     69     criterion=criterion,
     70     optimizer=optimizer,
     71     num_epochs=2000,
     72     device=device,
     73     save_path=save_path
     74 )

Cell In[30], line 22
     19 print(outputs.shape)
     20 # print('batch_labels', batch_labels)
     21 # loss = criterion(outputs.squeeze(), batch_labels)
...
   3084 if size_average is not None or reduce is not None:
   3085     reduction = _Reduction.legacy_get_string(size_average, reduce)
-> 3086 return torch._C._nn.cross_entropy_loss(input, target, weight, _Reduction.get_enum(reduction), ignore_index, label_smoothing)

RuntimeError: 0D or 1D target tensor expected, multi-target not supported
