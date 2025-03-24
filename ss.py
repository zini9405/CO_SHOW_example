# Main 실행
def main():
    csv_file = 'all.csv'
    scaler_path = 'scaler_params.pkl'
    df = pd.read_csv(csv_file)

    # RECIPE_ID = {'MIC_01_CA', 'SL_CA', 'MIC_01_CB', 'CIS_P_SKH6_CB', 'INTEL14_CA', 'SEC_L58_CA', 'CIS_P+_GLX5_CB', 'LOG_TSM3_CB', 'SL_CB', 'CIS_P+_SKH9_CA', 'MXIC_01_CB', 'CIS_P_SKH6_CA', 'TSMC_CB', 'CIS_CB', 'STM_P+_CB', 'S14_CB', 'SMIC4_R0_CA', 'INTEL7_CA', 'GF_01_CA', 'CIS_P+_SMI4_CA', 'GF_02_CB', 'SKH_CIS_P+_CB', 'GF_01_CB', 'CIS_P+_HUA4_CA', 'CIS_P+_CXT5_CB', 'GF_03_CB', 'TSMC2_CB', 'CIS_P+_CA', 'S14_CA', 'CIS_P+_SKH6_CA', 'SKH_CIS_P+_CA', 'L2_CB', 'HUALI_01_CB', 'GF_02_CA', 'CIS_P+_HUA4_CB', 'INTEL2_CB', 'INTEL10_CA', 'TSMC2_CA', 'PSMC_02_CB', 'CIS_P+_ONS6_CB', 'GF_03_CA', 'CAN3_01_CB', 'CIS_P+_SKH9_CB', 'SMIC2_R0_CB', 'PSMC_FSI_CA', 'TSMC_CA', 'CIS_P+_SKH6_CB', 'CIS_P+_PSM4_CA', 'UMC_R0_CA', 'STM_P+_CA', 
    #           'STM_01_CB', 'HUALI_01_CA', 'UMC_R0_CB', 'CIS_P+_ICR5_CB', 'TIX_R1_CB', 'LOG_TSM1_CA', 'TIX_R1_CA', 'INTEL14_CB', 'TIX_R0_CA', 'PSMC_02_CA', 'CIS_P+_UMC4_CB', 'SEC_L58_CB', 'SMIC2_R0_CA', 'SMIC_L7_CA', 'TIX_R0_CB', 'MXIC_01_CA', 'CIS_P+_GLX5_CA', 'CIS_P+_CB', 'STM_01_CA', 'LOG_TSM3_CA', 'CIS_P+_ONS6_CA', 'CIS_CA', 'SKH_CIS_CA', 'CIS_P+_UMC4_CA', 'INTEL7_CB', 'INTEL2_CA', 'SMIC_L7_CB', 'CAN3_01_CA', 'INTEL10_CB', 'LOG_TSM1_CB'}
    

    RECIPE_ID = {'L2_CB', 'GF_03_CA', 'TSMC_CB', 'CIS_P+_PSM4_CA', 'GF_02_CB', 'MXIC_01_CB', 'UMC_R0_CB', 'CIS_P+_SKH6_CA', 'CAN3_01_CA', 'CIS_P+_CB', 'HUALI_01_CA', 'TSMC2_CA', 
                'GF_01_CB', 'SKH_CIS_P+_CA', 'CIS_P+_SKH9_CB', 'CIS_P+_ONS6_CB', 'CIS_P+_ONS6_CA', 'STM_P+_CB', 'SKH_CIS_P+_CB', 'LOG_TSM3_CB', 'LOG_TSM3_CA', 'PSMC_02_CB', 'SL_CA',
                'STM_P+_CA', 'GF_03_CB', 'INTEL7_CB', 'LOG_TSM1_CB', 'CIS_P+_GLX5_CA', 'SEC_L58_CA', 'SMIC2_R0_CA', 'PSMC_FSI_CA', 'CAN3_01_CB', 'PSMC_02_CA', 'MIC_01_CB', 'CIS_P_SKH6_CA', 
                'TIX_R1_CB', 'LOG_TSM1_CA', 'MXIC_01_CA', 'CIS_P+_SKH6_CB', 'CIS_P+_SKH9_CA', 'SMIC4_R0_CA', 'GF_01_CA', 'INTEL14_CA', 'INTEL10_CB', 'GF_02_CA', 'SMIC_L7_CA', 'CIS_P+_UMC4_CA',
                'TIX_R0_CB', 'SL_CB', 'TIX_R1_CA', 'CIS_P_SKH6_CB', 'CIS_P+_GLX5_CB', 'HUALI_01_CB', 'TSMC2_CB', 'CIS_P+_SMI4_CA', 'CIS_P+_HUA4_CA', 'INTEL10_CA', 'SMIC_L7_CB', 'CIS_P+_CA', 
                'CIS_P+_ICR5_CB', 'TSMC_CA', 'SKH_CIS_CA', 'SEC_L58_CB', 'INTEL14_CB', 'CIS_P+_HUA4_CB', 'MIC_01_CA', 'CIS_P+_CXT5_CB', 'STM_01_CB', 'S14_CA', 'CIS_P+_UMC4_CB', 'INTEL2_CB', 'STM_01_CA', 
                'INTEL2_CA', 'CIS_CB', 'SMIC2_R0_CB', 'TIX_R0_CA', 'UMC_R0_CA', 'INTEL7_CA', 'CIS_CA', 'S14_CB'}

    # EQP_ID_MODULE_NAME = {'CENC10A', 'CENC10B', 'CENC11A', 'CENC11B', 'CENC12A', 'CENC12B', 'CENC13A', 'CENC13B', 'CENC14A', 'CENC14B', 'CENC15A', 'CENC15B', 'CENC16A', 'CENC16B', 'CENC17A', 'CENC17B', 'CENC31A', 'CENC31B', 'CENC32A',
    # 'CENC32B', 'CENC33A', 'CENC33B', 'CENC34A', 'CENC34B', 'CENC35A', 'CENC35B', 'CENC36A', 'CENC36B', 'CENC41A', 'CENC41B', 'CENC42A', 'CENC42B', 'CENC43A', 'CENC43B', 'CENC44A', 'CENC44B', 'CENC45A', 'CENC45B',
    # 'CENC46A', 'CENC46B', 'CENC47A', 'CENC47B', 'CENC48A', 'CENC48B', 'CENC5A', 'CENC5B', 'CENC6A', 'CENC6B', 'CENC7A', 'CENC7B', 'CENC8A', 'CENC8B', 'CENC9A', 'CENC9B', 'ZCENC01A', 'ZCENC01B', 'ZCENC02A', 'ZCENC02B',
    # 'ZCENC03A', 'ZCENC03B', 'ZCENC04A', 'ZCENC04B'}

    EQP_ID_MODULE_NAME = {'CENC42B', 'ZCENC04A', 'CENC33B', 'CENC12A', 'CENC10A', 'CENC13A', 'CENC8B', 'CENC48A', 'CENC41B', 'ZCENC02A', 'CENC17B', 'CENC34A', 'CENC48B', 'CENC14B', 'CENC46B', 
                          'ZCENC03A', 'CENC8A', 'CENC14A', 'CENC15B', 'CENC16B', 'CENC33A', 'CENC31B', 'CENC47B', 'CENC43B', 'CENC17A', 'ZCENC01B', 'CENC11B', 'ZCENC03B', 'ZCENC04B', 'CENC35B', 
                          'CENC35A', 'CENC11A', 'CENC9B', 'CENC34B', 'CENC44B', 'CENC42A', 'CENC36A', 'CENC16A', 'CENC31A', 'CENC32A', 'CENC10B', 'CENC45A', 'CENC43A', 'CENC44A', 'CENC7B', 'CENC36B', 
                          'CENC12B', 'CENC7A', 'CENC15A', 'CENC46A', 'CENC6B', 'CENC6A', 'CENC13B', 'CENC9A', 'CENC41A', 'ZCENC01A', 'CENC5A', 'CENC5B', 'CENC45B', 'ZCENC02B', 'CENC32B', 'CENC47A'}

    recipe_mapping = map_to_numeric(RECIPE_ID)
    eqp_mapping = map_to_numeric(EQP_ID_MODULE_NAME)

    df = standardize_new_data(df, scaler_path)
    
    # df = df.dropna(subset=['SFQR_AFS2', 'SFQR_AFS2_SUB'])
    df = df.dropna(subset=['ZDDFRONTMEAN_01_AFS2', 'ZDDFRONTMEAN_01_AFS2_SUB'])

    df.fillna(0, inplace=True)

    # print(df.isnull().sum())
    
    df = df.sort_values("HST_REG_DTTM")

    df = df.drop(columns=['ESFQD2_ZONE1MAX_AFS2', 'ESFQD2_ZONE1MAX_AFS2_SUB', 'ESFQD_ZONE1MAX_AFS2', 'ESFQD_ZONE1MAX_AFS2_SUB'])

    df.dropna(axis=0)

    print(set(df['RECIPE_ID']))

    if "RECIPE_ID" in df.columns:
        df["RECIPE_ID"] = df["RECIPE_ID"].map(recipe_mapping)

    dataset = CustomDataset(df, eqp_mapping)

    train_dataset, val_dataset = train_val_split(dataset, val_ratio=0.2)
    
    train_loader = DataLoader(train_dataset, batch_size=512, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=512, shuffle=False)

    model = FullMultiLevelTransformer(input_dim=1, eqp_vocab_size=len(eqp_mapping), d_model=256, nhead=4, num_layers=4, dim_feedforward=512)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    save_path = "model_weights_epi_250324.pth"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    criterion = nn.CrossEntropyLoss()

    train_model_inputs(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        criterion=criterion,
        optimizer=optimizer,
        num_epochs=2000,
        device=device,
        save_path=save_path
    )

if __name__ == "__main__":
    set_seed(42)
    main()
