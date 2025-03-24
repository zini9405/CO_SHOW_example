torch.Size([1249244])
torch.Size([312310])
Training Epoch 1/2000:   0%|          | 0/1 [00:00<?, ?it/s]
---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
Cell In[27], line 78
     76 if __name__ == "__main__":
     77     set_seed(42)
---> 78     main()

Cell In[27], line 65
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

Cell In[25], line 10
      8 running_loss = 0.0
      9 train_pbar = tqdm(train_loader, desc=f"Training Epoch {epoch + 1}/{num_epochs}")
---> 10 for batch_features, batch_eqp_ids, batch_labels in train_pbar:
...
    211     storage = elem._typed_storage()._new_shared(numel, device=elem.device)
    212     out = elem.new(storage).resize_(len(batch), *list(elem.size()))
--> 213 return torch.stack(batch, 0, out=out)

RuntimeError: stack expects each tensor to be equal size, but got [1249244, 32] at entry 0 and [1249244] at entry 1
