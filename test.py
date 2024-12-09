for file in all_files:
    # Load CSV
    df = pd.read_csv(file)
    
    # Ensure STEP_ID is sorted
    if "STEP_ID" in df.columns:
        df = df.sort_values("STEP_ID")
    
    # Drop unnecessary columns
    df = df.drop(columns=["STEP_NAME", "WAF_ID", "HST_REG_DTTM"], errors="ignore")
    
    # Replace RECIPE_ID and EQP_ID_MODULE_NAME with numeric values
    if "RECIPE_ID" in df.columns:
        df["RECIPE_ID"] = df["RECIPE_ID"].map(recipe_mapping)
    if "EQP_ID_MODULE_NAME" in df.columns:
        df["EQP_ID_MODULE_NAME"] = df["EQP_ID_MODULE_NAME"].map(eqp_mapping)
    
    # Fill missing values with a placeholder value
    df = df.fillna(-9999)
    
    # Split into 13-step sequences and extract labels
    num_rows = len(df)
    step_size = 13
    num_sequences = num_rows // step_size
    
    processed_data = []
    labels = []
    for i in range(num_sequences):
        sequence = df.iloc[i * step_size:(i + 1) * step_size]
        label = sequence.iloc[-1]["SFQR_AFS2"]  # Extract label from the last step of the sequence
        processed_data.append(sequence.values)
        labels.append(label)
    
    # Convert to 3D array (Num Sequences, Steps, Features) and labels
    processed_data = np.array(processed_data)
    labels = np.array(labels)
    
    # Save processed data and labels
    output_data_file = os.path.join(output_directory, os.path.basename(file).replace(".csv", "_data.npy"))
    output_label_file = os.path.join(output_directory, os.path.basename(file).replace(".csv", "_labels.npy"))
    np.save(output_data_file, processed_data)
    np.save(output_label_file, labels)

print(f"Processed data and labels saved in {output_directory}")