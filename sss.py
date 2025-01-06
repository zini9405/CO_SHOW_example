def main():
    csv_file = 'all_minmax.csv'  # 실제 CSV 파일 경로로 변경
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    EQP_ID_MODULE_NAME = {'CENC10A', 'CENC10B', 'CENC11A', 'CENC11B', 'CENC12A', 'CENC12B', 'CENC13A', 'CENC13B',
                          'CENC14A', 'CENC14B', 'CENC15A', 'CENC15B', 'CENC16A', 'CENC16B', 'CENC17A', 'CENC17B'}
    eqp_mapping = map_to_numeric(EQP_ID_MODULE_NAME)

    # 데이터 로드 및 전처리
    df = pd.read_csv(csv_file)
    df = df.dropna(subset=['ZDDFRONTMEAN_01_AFS2', 'ZDDFRONTMEAN_01_AFS2_SUB'])
    df.fillna(0, inplace=True)
    df = df.sort_values("HST_REG_DTTM")
    df["EQP_ID_MODULE_NAME"] = df["EQP_ID_MODULE_NAME"].map(eqp_mapping)

    dataset = CustomDataset(df, eqp_mapping)
    train_dataset, val_dataset = train_val_split(dataset, val_ratio=0.2)
    train_loader = DataLoader(train_dataset, batch_size=512, shuffle=True)

    # 모델 초기화
    model = FullMultiLevelTransformer(input_dim=32, eqp_vocab_size=len(eqp_mapping), d_model=256, nhead=4, num_layers=4, dim_feedforward=512)
    model.to(device)

    # Forward 실행을 위한 샘플 데이터 추출
    sample_features, sample_eqp_ids, _ = next(iter(train_loader))
    sample_features, sample_eqp_ids = sample_features.to(device), sample_eqp_ids.to(device)

    # Forward 실행
    _ = model(sample_features, sample_eqp_ids)

    # Attention Scores 시각화
    visualize_attention_scores(model, dataset.feature_names)