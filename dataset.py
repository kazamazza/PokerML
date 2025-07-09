import pandas as pd
import torch
from torch.utils.data import Dataset

class PokerDataset(Dataset):
    def __init__(self, features_path: str, labels_path: str, label_map: dict):
        self.features = pd.read_csv(features_path)
        self.labels = pd.read_csv(labels_path)["label"]
        self.label_map = label_map

        self.X = self.encode_features(self.features)
        self.y = self.encode_labels(self.labels)

    def encode_features(self, df: pd.DataFrame):
        df = pd.get_dummies(df, columns=["hero_hand", "board_texture", "action_history", "street"])

        # Force numeric conversion, fill NaNs, and set float32 type
        df = df.apply(pd.to_numeric, errors="coerce").fillna(0).astype("float32")

        return torch.tensor(df.values, dtype=torch.float32)

    def encode_labels(self, labels: pd.Series):
        encoded = [self.label_map.get(lbl, -1) for lbl in labels]

        # Filter out invalid labels (where value is -1)
        valid_indices = [i for i, y in enumerate(encoded) if y != -1]
        self.X = self.X[valid_indices]  # Keep only matching features
        return torch.tensor([encoded[i] for i in valid_indices], dtype=torch.long)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]