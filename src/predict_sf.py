import pandas as pd
import torch

from config_sf import CSV_FILE
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

print(
    f"データ数: {len(dataset)}"
)


# --------------------
# Prediction
# --------------------

rows = []

with torch.no_grad():

    for i in range(len(dataset)):

        sample = dataset[i]

        obj_id = sample["id"]

        image = sample["image"].unsqueeze(0)

        output = model(image)

        prob = torch.sigmoid(
            output
        )[0]

        rows.append({
            "id": obj_id,
            "detectable": float(prob[0]),
            "bright_neighbor": float(prob[1]),
            "multiple_component": float(prob[2]),
            "point_source": float(prob[3]),
        })

        if (i + 1) % 50 == 0:
            print(
                f"{i+1}/{len(dataset)}"
            )

# --------------------
# Save
# --------------------

df = pd.DataFrame(rows)

df.to_csv(
    "../data/prediction_SF.csv",
    index=False
)

print()
print(
    "prediction_SF.csv 保存完了"
)

# --------------------
# Uncertain
# --------------------

uncertain_rows = []

for _, row in df.iterrows():

    scores = [
        row["detectable"],
        row["bright_neighbor"],
        row["multiple_component"],
        row["point_source"],
    ]

    distance = min(
        abs(s - 0.5)
        for s in scores
    )

    if distance < 0.10:

        uncertain_rows.append(row)

uncertain_df = pd.DataFrame(
    uncertain_rows
)

uncertain_df.to_csv(
    "../data/uncertain_SF.csv",
    index=False
)

print(
    f"uncertain_SF.csv 保存完了 "
    f"({len(uncertain_df)} 件)"
)
