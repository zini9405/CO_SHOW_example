    dataset = CustomDataset(df)
    # test_loader = DataLoader(dataset, batch_size=512, shuffle=False)
    train_dataset, val_dataset = train_val_split(dataset, val_ratio=0.8)
