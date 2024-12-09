# 4. Masked MSE Loss
def masked_mse_loss(output, target):
    return torch.mean((output - target) ** 2)

criterion=masked_mse_loss

def test_model(model, test_loader, device, load_path):
    model.load_state_dict(torch.load(load_path))
    model.to(device)
    model.eval()
    test_loss = 0.0
    test_accuracy = 0.0
    predictions = []
    true_labels = []
    with torch.no_grad():
        for batch_data, batch_labels in tqdm(test_loader, desc="Testing"):
            batch_data = batch_data.to(device)
            batch_labels = batch_labels.to(device)
            outputs = model(batch_data).squeeze()
            loss = criterion(outputs.squeeze(), batch_labels)
            test_loss += loss.item()

            accuracy = calculate_accuracy(outputs.squeeze(), batch_labels)
            test_accuracy += accuracy
            predictions.extend(outputs)
            true_labels.extend(batch_labels)
    avg_test_loss = test_loss / len(test_loader)
    avg_test_accuracy = test_accuracy / len(test_loader)
    
    print(f"test Loss: {avg_test_loss:.4f}, test Accuracy: {avg_test_accuracy:.4f}")

    return predictions, true_labels
