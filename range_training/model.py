from torch import nn


class HandRangeModel(nn.Module):
    def __init__(self, input_dim: int, output_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 1326),  # Output: probabilities for all combos
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)