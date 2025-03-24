# 모델 훈련 루프
def train_model_inputs(model, train_loader, val_loader, criterion, optimizer, num_epochs, device, save_path):
    model.to(device)
    best_val_loss = float('inf')

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        train_pbar = tqdm(train_loader, desc=f"Training Epoch {epoch + 1}/{num_epochs}")
        for batch_features, batch_eqp_ids, batch_labels in train_pbar:
            batch_features, batch_eqp_ids, batch_labels = (
                batch_features.to(device), batch_eqp_ids.to(device), batch_labels.to(device)
            )
            print(batch_labels.shape)
            outputs, attention_scores = model(batch_features, batch_eqp_ids)
            # print('batch_labels', batch_labels)
            loss = criterion(outputs.squeeze(), batch_labels)
            # print(loss)
            # print(batch_features)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            train_pbar.set_postfix(loss=loss.item())

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            val_pbar = tqdm(val_loader, desc=f"Validation Epoch {epoch + 1}/{num_epochs}")
            for batch_features, batch_eqp_ids, batch_labels in val_pbar:
                batch_features, batch_eqp_ids, batch_labels = (
                    batch_features.to(device), batch_eqp_ids.to(device), batch_labels.to(device)
                )
                outputs, attention_scores = model(batch_features, batch_eqp_ids)
                loss = criterion(outputs.squeeze(), batch_labels)
                val_loss += loss.item()

        avg_val_loss = val_loss / len(val_loader)

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), save_path)
            print(f"Best model saved with validation loss: {best_val_loss:.4f}")

# Full Transformer Model
class FullMultiLevelTransformer(nn.Module):
    def __init__(self, input_dim, eqp_vocab_size, d_model=64, nhead=4, num_layers=2, dim_feedforward=128, dropout=0.1):
        super(FullMultiLevelTransformer, self).__init__()
        self.d_model = d_model

        self.eqp_embedding = nn.Embedding(eqp_vocab_size, d_model)  # Embedding for equipment IDs
        self.feature_embedding = nn.Linear(input_dim, d_model)
        self.feature_transformer = nn.ModuleList([
            CustomTransformerEncoderLayer(d_model, nhead, dim_feedforward, dropout)
            for _ in range(num_layers)
        ])
        self.fc = nn.Linear(d_model, 2)

    def forward(self, features, eqp_ids):
        features = features.unsqueeze(2)
        feature_embed = self.feature_embedding(features)

        eqp_embed = self.eqp_embedding(eqp_ids).unsqueeze(1)  # (batch_size, 1, d_model)

        combined_features = feature_embed + eqp_embed  # Combine feature and equipment embeddings

        attention_scores = []

        for layer in self.feature_transformer:
            combined_features, attn_weights = layer(combined_features)
            attention_scores.append(attn_weights)

        pooled = combined_features.mean(dim=1)  # (batch, d_model)
        logits = self.fc(pooled)  # (batch, 2)
        return logits, attention_scores
