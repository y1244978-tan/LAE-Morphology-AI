import torch
import torch.nn as nn

from torch.utils.data import (
    DataLoader,
    random_split
)

from dataset import GalaxyDataset
from model import create_model


# --------------------
# Dataset
# --------------------

from config import CSV_FILE

dataset = GalaxyDataset(
    CSV_FILE
)

train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size

train_dataset, test_dataset = random_split(
    dataset,
    [train_size, test_size]
)

print(
    f"Train: {len(train_dataset)}"
)

print(
    f"Test : {len(test_dataset)}"
)


# --------------------
# DataLoader
# --------------------

train_loader = DataLoader(
    train_dataset,
    batch_size=4,
    shuffle=True
)

test_loader = DataLoader(
    test_dataset,
    batch_size=4,
    shuffle=False
)




# --------------------
# Model
# --------------------

model = create_model()

criterion = nn.BCEWithLogitsLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)


# --------------------
# Training
# --------------------

print("\n===== Training =====")


model.train()

for epoch in range(20):

    total_loss = 0.0

    for batch in train_loader:

        images = batch["image"]

        labels = batch["label"]

        outputs = model(images)

        loss = criterion(
            outputs,
            labels
        )

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    avg_loss = (
        total_loss /
        len(train_loader)
    )

    print(
        f"Epoch {epoch+1}: "
        f"Average Loss = {avg_loss:.4f}"
    )


# --------------------
# Evaluation
# --------------------

misclassified = []

model.eval()

correct = [0, 0, 0, 0]
total = 0

with torch.no_grad():

    for batch in test_loader:

        images = batch["image"]
        labels = batch["label"]
        ids = batch["id"]

        outputs = model(images)

        probs = torch.sigmoid(
            outputs
        )

        preds = (
            probs > 0.5
        ).float()

        for j in range(4):

            correct[j] += (
                preds[:, j]
                ==
                labels[:, j]
            ).sum().item()

        total += labels.shape[0]

        for i in range(len(ids)):

            if not torch.equal(
                preds[i],
                labels[i]
            ):

                misclassified.append({
                    "id": int(ids[i]),
                    "true": labels[i].tolist(),
                    "pred": preds[i].tolist()
                })

import pandas as pd
from pathlib import Path

csv_name = Path(CSV_FILE).stem

date = csv_name.split("_")[-1]

mis_file = (
    f"../data/misclassified_{date}.csv"
)

pd.DataFrame(
    misclassified
).to_csv(
    mis_file,
    index=False
)

print(
    f"\n誤分類数: {len(misclassified)}"
)

print(
    f"{mis_file} 保存完了"
)


names = [
    "Detectable",
    "Bright Neighbor",
    "Multiple Component",
    "Point Source"
]

print("\n===== TEST ACCURACY =====")

for name, c in zip(
    names,
    correct
):

    acc = c / total * 100

    print(
        f"{name:20s}: "
        f"{acc:.1f}%"
    )


# --------------------
# Save Model
# --------------------

torch.save(
    model.state_dict(),
    "../models/resnet18_f277w.pth"
)

print(
    "\nモデル保存成功"
)

#誤分類サンプル抽出(使うときは True に変更)
SHOW_MISCLASSIFIED = False

if SHOW_MISCLASSIFIED:

    print("\n===== Misclassified =====")

    with torch.no_grad():

        for batch in test_loader:

            images = batch["image"]
            labels = batch["label"]
            ids = batch["id"]

            outputs = model(images)

            probs = torch.sigmoid(outputs)

            preds = (probs > 0.5).float()

            for i in range(len(ids)):

                if not torch.equal(
                    preds[i],
                    labels[i]
                ):

                    print(
                        f"ID={ids[i]}"
                    )

                    print(
                        f"True={labels[i].tolist()}"
                    )

                    print(
                        f"Pred={preds[i].tolist()}"
                    )

                    print()