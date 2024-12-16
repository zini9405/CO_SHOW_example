def main():
    # 데이터 경로 설정
    csv_file = 'all.csv'
    save_path = "model_weights_multi_all.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    RECIPE_ID = {...}  # 생략 (기존 코드와 동일)
    EQP_ID_MODULE_NAME = {...}  # 생략 (기존 코드와 동일)

    recipe_mapping = map_to_numeric(RECIPE_ID)
    eqp_mapping = map_to_numeric(EQP_ID_MODULE_NAME)

    # 데이터셋 로드 및 전처리
    df = pd.read_csv(csv_file).dropna()
    df = df.sort_values("HST_REG_DTTM")

    if "RECIPE_ID" in df.columns:
        df["RECIPE_ID"] = df["RECIPE_ID"].map(recipe_mapping)
    if "EQP_ID_MODULE_NAME" in df.columns:
        df["EQP_ID_MODULE_NAME"] = df["EQP_ID_MODULE_NAME"].map(eqp_mapping)

    # 데이터 필터링 (선택적으로 필터 적용)
    recipe_filter = {'CAN3_01_CA', 'CIS_P+_CA'}  # 원하는 Recipe만 사용
    eqp_filter = {'CENC10A', 'CENC10B'}  # 원하는 Equipment만 사용
    df = filter_data(df, recipe_filter=recipe_filter, eqp_filter=eqp_filter)

    # feature_names 정의: 제외 열 제외한 나머지 열 이름
    exclude_columns = ['SFQR_AFS2', 'STEP_NAME', "WAF_ID", "HST_REG_DTTM", 'STEP_ID']
    feature_names = [col for col in df.columns if col not in exclude_columns]

    dataset = CustomDataset(df)

    # Train/Test Split
    train_dataset, val_dataset = train_val_split(dataset, val_ratio=0.2)
    test_loader = DataLoader(val_dataset, batch_size=512, shuffle=False)

    # 모델 초기화
    model = FullMultiLevelTransformer(input_dim=len(feature_names), d_model=256, nhead=4, num_layers=4, dim_feedforward=512)

    # 테스트 실행
    predictions, true_labels = test_model(model, test_loader, device, save_path, dataset.quantile_transformer)

    # 예측 정확도 확인
    print(f"R2 Score: {r2_score(true_labels, predictions)}")

    # 예측 결과 시각화
    visualize_predictions(predictions, true_labels)

    # SHAP 분석
    shap_analysis(model, dataset, device, feature_names)