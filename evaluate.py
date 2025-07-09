import torch
from torch.utils.data import random_split, DataLoader
from dataset import PokerDataset
from model import PokerStrategyModel
import argparse
from sklearn.metrics import classification_report, confusion_matrix

def evaluate(street: str, stake: str = "10", batch_size: int = 32):
    label_map = {"fold": 0, "call": 1, "raise": 2}
    reverse_label_map = {v: k for k, v in label_map.items()}

    features_path = f"data/features/NL{stake}/{street}/features.csv"
    labels_path = f"data/features/NL{stake}/{street}/labels.csv"

    # Load full dataset and split
    full_dataset = PokerDataset(features_path, labels_path, label_map)
    test_size = int(0.2 * len(full_dataset))
    train_size = len(full_dataset) - test_size
    _, test_dataset = random_split(full_dataset, [train_size, test_size])
    test_loader = DataLoader(test_dataset, batch_size=batch_size)

    model_path = f"models/NL{stake}/{street}.pt"
    input_dim = full_dataset.X.shape[1]
    output_dim = len(label_map)

    model = PokerStrategyModel(input_dim=input_dim, output_dim=output_dim)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    y_true = []
    y_pred = []

    with torch.no_grad():
        for x_batch, y_batch in test_loader:
            out = model(x_batch)
            preds = torch.argmax(out, dim=1)

            y_true.extend(y_batch.tolist())
            y_pred.extend(preds.tolist())

    labels = list(label_map.values())
    target_names = list(label_map.keys())

    print("📊 Classification Report:")
    print(classification_report(y_true, y_pred, labels=labels, target_names=target_names))

    print("🧱 Confusion Matrix:")
    print(confusion_matrix(y_true, y_pred, labels=labels))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("street", type=str, help="e.g. flop")
    parser.add_argument("--stake", type=str, default="10")
    args = parser.parse_args()

    evaluate(args.street, stake=args.stake)