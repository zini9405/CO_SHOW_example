class CustomDataset(Dataset):
    def __init__(self, df, eqp_mapping):
        self.data = df
        self.eqp_mapping = eqp_mapping

        # 원래 연속형 라벨
        raw_labels = self.data['6900_GBIR_AFS2'].values.reshape(-1, 1)  # shape: (num_samples, 1)

        # 정규화 후 중앙값 기준 이진화
        self.quantile_transformer = QuantileTransformer(output_distribution='normal', random_state=42)
        transformed = self.quantile_transformer.fit_transform(raw_labels).flatten()

        # 중앙값 기준으로 0/1 이진 클래스 생성
        threshold = np.median(transformed)
        self.labels = (transformed > threshold).astype(np.int64)  # shape: (num_samples,)

        # Feature
        self.features = self.data.drop(columns=['BASE_DT', 'EQP_ID', 'WAF_ID', '6900_GBIR_AFS2']).values

        # EQP ID
        self.eqp_ids = self.data['EQP_ID'].map(eqp_mapping).values

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        features = torch.tensor(self.features[idx], dtype=torch.float32)
        label = torch.tensor(self.labels[idx], dtype=torch.long)  # Must be scalar long
        eqp_id = torch.tensor(self.eqp_ids[idx], dtype=torch.long)
        return features, eqp_id, label