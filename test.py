import pandas as pd
import os
import numpy as np
import glob

# 1. RECIPE_ID와 EQP_ID_MODULE_NAME 매핑
def map_to_numeric(values):
    mapping = {val: idx for idx, val in enumerate(sorted(values))}
    return mapping

RECIPE_ID = {
    'CAN3_01_CA', 'CAN3_01_CB', 'CIS_CA', 'CIS_CB', 'CIS_P+_CA', 'CIS_P+_CB', 
    'CIS_P+_CXT5_CB', 'CIS_P+_GLX5_CA', 'CIS_P+_GLX5_CB', 'CIS_P+_HUA4_CA',
    'CIS_P+_HUA4_CB', 'CIS_P+_ICR5_CB', 'CIS_P+_ONS6_CA', 'CIS_P+_ONS6_CB',
    # ... (중략, 전체 리스트 포함)
    'TSMC_CA', 'TSMC_CB', 'UMC_R0_CA', 'UMC_R0_CB'
}
EQP_ID_MODULE_NAME = {
    'CENC10A', 'CENC10B', 'CENC11A', 'CENC11B', 'CENC12A', 'CENC12B',
    # ... (중략, 전체 리스트 포함)
    'ZCENC04A', 'ZCENC04B'
}

recipe_mapping = map_to_numeric(RECIPE_ID)
eqp_mapping = map_to_numeric(EQP_ID_MODULE_NAME)

# 2. 장비별 CSV 처리
final_directory = "final"  # Replace with your actual directory path
output_directory = "processed"  # Output directory for processed files
os.makedirs(output_directory, exist_ok=True)

all_files = glob.glob(os.path.join(final_directory, "*.csv"))

for file in all_files:
    # Load CSV
    df = pd.read_csv(file)
    
    # Ensure HST_REG_DTTM is sorted
    df = df.sort_values("HST_REG_DTTM")
    
    # Drop unnecessary columns
    df = df.drop(columns=["STEP_NAME", "WAF_ID", "HST_REG_DTTM"], errors="ignore")
    
    # Replace RECIPE_ID and EQP_ID_MODULE_NAME with numeric values
    if "RECIPE_ID" in df.columns:
        df["RECIPE_ID"] = df["RECIPE_ID"].map(recipe_mapping)
    if "EQP_ID_MODULE_NAME" in df.columns:
        df["EQP_ID_MODULE_NAME"] = df["EQP_ID_MODULE_NAME"].map(eqp_mapping)
    
    # Fill missing values with a placeholder value
    df = df.fillna(-9999)
    
    # Split into 12-step sequences
    num_rows = len(df)
    step_size = 12
    num_sequences = num_rows // step_size
    
    processed_data = []
    for i in range(num_sequences):
        sequence = df.iloc[i * step_size:(i + 1) * step_size].values
        processed_data.append(sequence)
    
    # Convert to 3D array (Num Sequences, Steps, Features)
    processed_data = np.array(processed_data)
    
    # Save processed data
    output_file = os.path.join(output_directory, os.path.basename(file).replace(".csv", "_processed.npy"))
    np.save(output_file, processed_data)

print(f"Processed data saved in {output_directory}")