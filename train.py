import os
import sys
from torch.utils.data import DataLoader
import torch
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from dataset import PokerDataset
from model import PokerStrategyModel


def train(street: str, stake: str = "10", batch_size=32, epochs=10):
    label_map = {"fold": 0, "call": 1, "raise": 2}  # You can expand this

    features_path = f"data/features/NL{stake}/{street}/features.csv"
    labels_path = f"data/features/NL{stake}/{street}/labels.csv"

    dataset = PokerDataset(features_path, labels_path, label_map)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = PokerStrategyModel(input_dim=dataset.X.shape[1], output_dim=len(label_map))
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    log_dir = f"runs/NL{stake}/{street}"
    writer = SummaryWriter(log_dir=log_dir)

    for epoch in range(epochs):
        total_loss = 0
        correct = 0

        for x_batch, y_batch in loader:
            optimizer.zero_grad()
            out = model(x_batch)
            loss = F.cross_entropy(out, y_batch)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            preds = torch.argmax(out, dim=1)
            correct += (preds == y_batch).sum().item()

        acc = correct / len(dataset)
        writer.add_scalar("Loss/train", total_loss, epoch)
        writer.add_scalar("Accuracy/train", acc, epoch)
        print(f"Epoch {epoch+1} | Loss: {total_loss:.4f} | Accuracy: {acc:.2f}")

    writer.close()

    model_dir = f"models/NL{stake}"
    os.makedirs(model_dir, exist_ok=True)
    model_path = f"{model_dir}/{street}.pt"
    torch.save(model.state_dict(), model_path)
    print(f"✅ Model saved to {model_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please specify the street (e.g. preflop, flop, turn, river)")
        sys.exit(1)

    street_arg = sys.argv[1]
    stake_arg = sys.argv[2] if len(sys.argv) > 2 else "10"
    train(street=street_arg, stake=stake_arg)