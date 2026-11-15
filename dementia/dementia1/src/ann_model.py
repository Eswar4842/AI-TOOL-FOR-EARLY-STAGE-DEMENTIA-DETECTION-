import torch.nn as nn


class ANN(nn.Module):

    def __init__(self, input_dim):

        super().__init__()

        self.model = nn.Sequential(

            nn.Linear(
                input_dim,
                128
            ),

            nn.ReLU(),

            nn.Dropout(
                0.30
            ),

            nn.Linear(
                128,
                64
            ),

            nn.ReLU(),

            nn.Dropout(
                0.25
            ),

            nn.Linear(
                64,
                32
            ),

            nn.ReLU(),

            nn.Dropout(
                0.20
            ),

            nn.Linear(
                32,
                16
            ),

            nn.ReLU(),

            nn.Linear(
                16,
                1
            ),

            nn.Sigmoid()

        )

    def forward(
        self,
        x
    ):

        return self.model(
            x
        )