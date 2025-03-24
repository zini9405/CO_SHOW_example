def __getitem__(self, idx):
    features = torch.tensor(self.features[idx], dtype=torch.float32)
    eqp_id = torch.tensor(self.eqp_ids[idx], dtype=torch.long)
    label = torch.tensor(int(self.labels[idx].squeeze()), dtype=torch.long)

    # 디버깅 출력
    print("features.shape:", features.shape)
    print("eqp_id:", eqp_id)
    print("label:", label)

    return features, eqp_id, label