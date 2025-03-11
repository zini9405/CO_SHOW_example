# Main 실행
def main():
    # === 1. STEP.csv 불러오기 ===
    file_path = "STEP.csv"  # 파일 경로 설정
    scaler_path = 'scalers_.pkl'
    df = pd.read_csv(file_path, encoding="utf-8")
    
    df = df.dropna(subset=['GBIR_AFS2'])

    df.fillna(0, inplace=True)

    df.dropna(axis=0)

    # === 2. BASE_DT, WAF_ID, STEP_ID 정렬 ===
    df = df.sort_values(by=["BASE_DT", "WAF_ID", "STEP_ID"], ascending=[True, True, True])

    df = standardize_new_data(df, scaler_path)

    # === 3. EQP_ID를 숫자로 변환 (임베딩할 예정) ===
    if "EQP_ID" in df.columns:
        eqp_encoder = LabelEncoder()
        df["EQP_ID"] = eqp_encoder.fit_transform(df["EQP_ID"])
    else:
        eqp_encoder = None

    # === 4. 필요없는 열 제거 ===
    drop_columns = ["GBIR_AFS2", "WAF_ID", "BASE_DT", "PAD_TEMP_STEP_MEAN"]
    feature_columns = [col for col in df.columns if col not in drop_columns]

    # === 5. 90:10 비율로 train/test 데이터 분할 ===
    waf_ids = df["WAF_ID"].unique()
    train_ids, val_ids = train_test_split(waf_ids, test_size=0.1, shuffle=False)  # 순서 유지
    train_df = df[df["WAF_ID"].isin(train_ids)]
    val_df = df[df["WAF_ID"].isin(val_ids)]

    # === 7. Dataset 및 DataLoader 생성 ===
    train_dataset = WaferDataset(train_df, eqp_encoder, feature_columns)
    val_dataset = WaferDataset(val_df, eqp_encoder, feature_columns)

    train_loader = DataLoader(train_dataset, batch_size=512, shuffle=True, collate_fn=lambda x: x)
    val_loader = DataLoader(val_dataset, batch_size=512, shuffle=False, collate_fn=lambda x: x)      

    model = FullMultiLevelTransformer(input_dim=1, eqp_vocab_size=len(set(df["EQP_ID"])), d_model=256, nhead=4, num_layers=4, dim_feedforward=512)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    save_path = "model_weights_GBIR_25312.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_model_inputs(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        criterion=nn.HuberLoss(delta=1.0),
        optimizer=optimizer,
        num_epochs=2000,
        device=device,
        save_path=save_path
    )

if __name__ == "__main__":
    set_seed(42)
    main()
