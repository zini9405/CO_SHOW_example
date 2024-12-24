df = data[['MAIN_RUNTIME', 'DD_USE_NUM', 'SLURRY_USE_NUM', 'PAD_COUNT', 'CARRIER_MTL_USE_NUM', 'GBIR']]



quantile_transformer = QuantileTransformer(output_distribution='normal', random_state=42)
self.quantile_transformer.fit_transform(self.labels.reshape(-1, 1)).flatten()
