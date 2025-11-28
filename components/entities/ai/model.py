import torch
import torch.nn as nn
import torch.nn.functional as F


class MahjongCNN(nn.Module):
    def __init__(self, in_channels=86):
        super().__init__()
        # 3 conv blocks, kernels 5x2, 100 filters, no padding

        # Block 1
        self.conv1 = nn.Conv2d(in_channels, 100, kernel_size=(5, 2), padding=0)
        self.bn1 = nn.BatchNorm2d(100)
        self.drop1 = nn.Dropout2d(0.5)
        # Block 2
        self.conv2 = nn.Conv2d(100, 100, kernel_size=(5, 2), padding=0)
        self.bn2 = nn.BatchNorm2d(100)
        self.drop2 = nn.Dropout2d(0.5)
        # Block 3
        self.conv3 = nn.Conv2d(100, 100, kernel_size=(5, 2), padding=0)
        self.bn3 = nn.BatchNorm2d(100)
        self.drop3 = nn.Dropout2d(0.5)

        # Get flattened size
        with torch.no_grad():
            dummy = torch.zeros(1, in_channels, 34, 4)
            dummy = self._forward_convs(dummy)
            flat_size = dummy.view(1, -1).shape[1]

        self.fc = nn.Linear(flat_size, 300)

        # Different output heads
        self.head_discard = nn.Linear(300, 34)
        self.head_chi = nn.Linear(300, 4)
        self.head_pon = nn.Linear(300, 2)
        self.head_riichi = nn.Linear(300, 2)

    def _forward_convs(self, x):
        # x: (B, in_channels, 34, 4)
        x = self.drop1(F.relu(self.bn1(self.conv1(x))))
        x = self.drop2(F.relu(self.bn2(self.conv2(x))))
        x = self.drop3(F.relu(self.bn3(self.conv3(x))))
        return x

    def forward(self, x):
        # x: (B, in_channels, 34, 4)
        x = self._forward_convs(x)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc(x))

        out_discard = self.head_discard(x)
        out_chi = self.head_chi(x)
        out_pon = self.head_pon(x)
        out_riichi = self.head_riichi(x)

        return out_discard, out_chi, out_pon, out_riichi
