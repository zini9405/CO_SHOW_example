from sklearn.preprocessing import LabelEncoder

if "EQP_ID" in df.columns:
    eqp_encoder = LabelEncoder()
    df["EQP_ID"] = eqp_encoder.fit_transform(df["EQP_ID"])
    
    # LabelEncoder의 classes_ 속성을 사용하여 매핑 딕셔너리 생성
    eqp_mapping = {label: idx for idx, label in enumerate(eqp_encoder.classes_)}
    print(eqp_mapping)
else:
    eqp_encoder = None