import torch.nn as nn
from torchvision.models import resnet18


def create_model():

    model = resnet18()

    model.fc = nn.Linear(
        model.fc.in_features,
        4
    )

    return model