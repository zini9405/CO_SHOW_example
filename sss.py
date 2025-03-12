# === 3. EQP_ID를 숫자로 변환 (임베딩할 예정) ===
if "EQP_ID" in df.columns:
    eqp_encoder = LabelEncoder()
    df["EQP_ID"] = eqp_encoder.fit_transform(df["EQP_ID"])
else:
    eqp_encoder = None

array([ 3,  3,  3, ..., 28, 28, 28], dtype=int64) 결과 아래와 같이 나오게 해줘



{'BPDPD100': 0,
 'BPDPD101': 1,
 'BPDPD102': 2,
 'BPDPD103': 3,
 'BPDPD104': 4,
 'BPDPD105': 5,
 'BPDPD106': 6,
 'BPDPD107': 7,
 'BPDPD108': 8,
 'BPDPD109': 9,
 'BPDPD111': 10,
 'BPDPD112': 11,
 'BPDPD113': 12,
 'BPDPD114': 13,
 'BPDPD115': 14,
 'BPDPD116': 15,
 'BPDPD117': 16,
 'BPDPD118': 17,
 'BPDPD119': 18,
 'BPDPD74': 19,
 'BPDPD80': 20,
 'BPDPD81': 21,
 'BPDPD82': 22,
 'BPDPD83': 23,
 'BPDPD84': 24,
...
 'BPDPD95': 35,
 'BPDPD96': 36,
 'BPDPD97': 37,
 'BPDPD98': 38,
 'BPDPD99': 39}
