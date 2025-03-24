        self.fc = nn.Linear(d_model, 2) # 2로 수정


class CustomDataset(Dataset):
    def __init__(self, df, eqp_mapping):
        self.data = df
        self.eqp_mapping = eqp_mapping
        self.labels = self.data['SFQR_AFS2'].values
        # 정규 분포로 변환
        # self.quantile_transformer = QuantileTransformer(output_distribution='normal', random_state=42)
        # transformed_labels = self.quantile_transformer.fit_transform(self.labels.reshape(-1, 1)).flatten()

        # 0.5 기준으로 이진 분류 라벨 생성
        self.labels = (self.labels > 0.5).astype(np.int64)

        # Feature 추출
        self.features = self.data.drop(columns=[
            'WAF_ID', 'HST_REG_DTTM', 'SFQR_AFS2', 'ESFQR2_MAX_AFS2', 'ZDDFRONTMEAN_01_AFS2',
            'ESFQD_ZONE1MEAN_AFS2', 'ESFQD2_ZONE1MEAN_AFS2', 'SFQR_AFS2_SUB', 'ESFQR2_MAX_AFS2_SUB', 'ESFQD_ZONE1MEAN_AFS2_SUB',
            'ESFQD2_ZONE1MEAN_AFS2_SUB', 'EQP_ID_MODULE_NAME'
        ]).values
        # Equipment ID 인코딩
        self.eqp_ids = self.data['EQP_ID_MODULE_NAME'].map(self.eqp_mapping).values

    def __len__(self):
        return len(self.data)

    # def __getitem__(self, idx):
    #     features = torch.tensor(self.features[idx], dtype=torch.float32)
    #     label = torch.tensor(self.labels[idx], dtype=torch.long)
    #     print(label.shape)
    #     eqp_id = torch.tensor(self.eqp_ids[idx], dtype=torch.long)
    #     return features, eqp_id, label
    
    def __getitem__(self, idx):
        features = torch.tensor(self.features[idx], dtype=torch.float32)
        eqp_id = torch.tensor(self.eqp_ids[idx], dtype=torch.long)
        # label = torch.tensor(self.labels[idx], dtype=torch.long).unsqueeze(0)
        label = int(self.labels[idx])

        # 디버깅 출력
        print("features.shape:", features.shape)
        print("eqp_id:", eqp_id)
        print("label:", label)

        return features, eqp_id, label


# 데이터 매핑 함수
def map_to_numeric(values):
    mapping = {val: idx for idx, val in enumerate(sorted(values))}
    return mapping

def train_val_split(dataset, val_ratio=0.2):
    val_size = int(len(dataset) * val_ratio)
    train_size = len(dataset) - val_size
    
    indices = list(range(len(dataset)))
    train_indices = indices[:train_size]
    val_indices = indices[train_size:]

    train_dataset = Subset(dataset, train_indices)
    val_dataset = Subset(dataset, val_indices)
    # train_dataset = dataset[:train_size]  # 앞부분을 train으로
    # val_dataset = dataset[train_size:]  # 뒷부분을 val로
    
    return train_dataset, val_dataset


loss = criterion(outputs, batch_labels)


criterion = nn.CrossEntropyLoss()
