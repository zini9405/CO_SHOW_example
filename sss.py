def main():
    # 데이터 경로 설정
    csv_file = 'all_minmax.csv'  # 실제 CSV 파일 경로로 변경하세요
    save_path = "model_weights_ZDD1111.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    RECIPE_ID = {'CAN3_01_CA', 'CAN3_01_CB', 'CIS_CA', 'CIS_CB', ...}
    EQP_ID_MODULE_NAME = {'CENC10A', 'CENC10B', 'CENC11A', 'CENC11B', ...}

    recipe_mapping = map_to_numeric(RECIPE_ID)
    eqp_mapping = map_to_numeric(EQP_ID_MODULE_NAME)

    df = pd.read_csv(csv_file)

    # 필요 없는 열 제거 및 전처리
    df = df.dropna(subset=['ZDDFRONTMEAN_01_AFS2', 'ZDDFRONTMEAN_01_AFS2_SUB'])
    df.fillna(0, inplace=True)
    df = df.sort_values("HST_REG_DTTM")

    if "RECIPE_ID" in df.columns:
        df["RECIPE_ID"] = df["RECIPE_ID"].map(recipe_mapping)

    dataset = CustomDataset(df, eqp_mapping)

    # 모델 로드
    model = FullMultiLevelTransformer(input_dim=1, eqp_vocab_size=len(eqp_mapping), d_model=256, nhead=4, num_layers=4, dim_feedforward=512)
    model.load_state_dict(torch.load(save_path))
    model.to(device)
    model.eval()

    # 변수 이름 가져오기
    feature_names = df.drop(columns=[
        'WAF_ID', 'HST_REG_DTTM', 'SFQR_AFS2', 'ESFQR2_MAX_AFS2', 'ZDDFRONTMEAN_01_AFS2',
        'ESFQD_ZONE1MEAN_AFS2', 'ESFQD_ZONE1MAX_AFS2', 'ESFQD2_ZONE1MEAN_AFS2', 'ESFQD2_ZONE1MAX_AFS2',
        'SFQR_AFS2_SUB', 'ESFQR2_MAX_AFS2_SUB', 'ESFQD_ZONE1MEAN_AFS2_SUB', 'ESFQD_ZONE1MAX_AFS2_SUB',
        'ESFQD2_ZONE1MEAN_AFS2_SUB', 'ESFQD2_ZONE1MAX_AFS2_SUB', 'EQP_ID_MODULE_NAME'
    ]).columns.tolist()

    # 예측값 및 중요도 저장
    predictions = []
    variable_importances = []

    for i in tqdm(range(len(dataset)), desc="Processing Data"):
        features, eqp_id, _ = dataset[i]
        features = features.unsqueeze(0).to(device)  # 배치 차원 추가
        eqp_id = eqp_id.unsqueeze(0).to(device)

        with torch.no_grad():
            output, attention_scores = model(features, eqp_id)
            output = output.squeeze().cpu().item()
            predictions.append(output)

            # 마지막 레이어의 Attention Scores 사용
            final_layer_attention_scores = attention_scores[-1]  # (1, nhead, seq_len, seq_len)
            sample_importance = compute_variable_importance(final_layer_attention_scores).cpu().numpy()
            variable_importances.append(sample_importance)

    # 결과를 데이터프레임에 추가
    df["pred"] = predictions
    variable_importances = np.array(variable_importances)  # (num_samples, num_features)

    for idx, feature_name in enumerate(feature_names):
        df[f"{feature_name}_importance"] = variable_importances[:, idx]

    # CSV 저장
    output_csv = "all_minmax_with_predictions_and_importance.csv"
    df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")


if __name__ == "__main__":
    main()