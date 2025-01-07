csv_file = 'all_minmax.csv'

df = pd.read_csv(csv_file)

df = df.dropna(subset=['SFQR_AFS2', 'SFQR_AFS2_SUB'])

df.fillna(0, inplace=True)

df = df.sort_values("HST_REG_DTTM")


grouped = df.groupby('EQP_ID_MODULE_NAME')
result = grouped['SFQR_AFS2'].agg(['mean'])
result
