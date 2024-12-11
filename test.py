# Train 데이터 저장
train_data = [train_dataset[i] for i in range(len(train_dataset))]
train_df = pd.DataFrame(train_data)
train_df.to_csv("train_data.csv", index=False)

# Validation 데이터 저장
val_data = [val_dataset[i] for i in range(len(val_dataset))]
val_df = pd.DataFrame(val_data)
val_df.to_csv("val_data.csv", index=False)

print("Train/Validation 데이터가 CSV로 저장되었습니다.")