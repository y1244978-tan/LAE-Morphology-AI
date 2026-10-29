import torch

from config import CSV_FILE
from dataset import GalaxyDataset
from model import create_model

model = create_model()

model.load_state_dict(
    torch.load(
        "../models/resnet18_f277w.pth",
        map_location="cpu"
    )
)

model.eval()

dataset = GalaxyDataset(CSV_FILE)

for i in [250,251,252,253,254]:

    print(f"\n===== {i} =====")

    sample = dataset[i]

    image = sample["image"].unsqueeze(0)

    output = model(image)

    print(output.shape)

print("DONE")