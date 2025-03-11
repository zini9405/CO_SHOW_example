---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Cell In[46], line 47
     44 for batch_ in train_pbar:
     45     batch_features, batch_eqp_ids, batch_labels = zip(*batch_)
     46     batch_features, batch_eqp_ids, batch_labels = (
---> 47         batch_features.to(device), batch_eqp_ids.to(device), batch_labels.to(device)
     48     )
     49 break

AttributeError: 'tuple' object has no attribute 'to'
