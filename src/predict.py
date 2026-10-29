import sys
import torch

from config import CSV_FILE
from dataset import GalaxyDataset
from model import create_model


# --------------------
# Model Load
# --------------------

model = create_model()

model.load_state_dict(
    torch.load(
        "../models/resnet18_f277w.pth",
        map_location="cpu"
    )
)

model.eval()

print("モデル読込成功")


# --------------------
# Dataset
# --------------------

dataset = GalaxyDataset(
    CSV_FILE
)


# --------------------
# Target ID
# --------------------

if len(sys.argv) < 2:

    print(
        "使い方: python predict.py <ID>"
    )

    sys.exit()

target_id = int(
    sys.argv[1]
)

sample = None

for i in range(len(dataset)):

    s = dataset[i]

    if s["id"] == target_id:

        sample = s

        break


if sample is None:

    print(
        f"ID {target_id} not found"
    )

    sys.exit()


# --------------------
# Prediction
# --------------------

image = sample["image"]

with torch.no_grad():

    output = model(
        image.unsqueeze(0)
    )

prob = torch.sigmoid(
    output
)[0]


# --------------------
# Result
# --------------------

labels = [
    "Detectable",
    "Bright Neighbor",
    "Multiple Component",
    "Point Source"
]

print()
print(
    f"ID: {target_id}"
)

print()

for name, p in zip(
    labels,
    prob
):

    print(
        f"{name:20s}: "
        f"{p.item()*100:.1f}%"
    )
    