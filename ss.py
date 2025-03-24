---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[17], line 78
     76 if __name__ == "__main__":
     77     set_seed(42)
---> 78     main()

Cell In[17], line 54
     50     df["RECIPE_ID"] = df["RECIPE_ID"].map(recipe_mapping)
     52 dataset = CustomDataset(df, eqp_mapping)
---> 54 train_dataset, val_dataset = train_val_split(dataset, val_ratio=0.2)
     56 train_loader = DataLoader(train_dataset, batch_size=512, shuffle=True)
     57 val_loader = DataLoader(val_dataset, batch_size=512, shuffle=False)

Cell In[14], line 10
      7 val_size = int(len(dataset) * val_ratio)
      8 train_size = len(dataset) - val_size
---> 10 train_dataset = dataset[:train_size]  # 앞부분을 train으로
     11 val_dataset = dataset[train_size:]  # 뒷부분을 val로
     13 return train_dataset, val_dataset

Cell In[13], line 27
     25 def __getitem__(self, idx):
     26     features = torch.tensor(self.features[idx], dtype=torch.float32)
---> 27     label = torch.tensor(int(self.labels[idx]), dtype=torch.long)
     28     eqp_id = torch.tensor(self.eqp_ids[idx], dtype=torch.long)
     29     return features, eqp_id, label

TypeError: only length-1 arrays can be converted to Python scalars
