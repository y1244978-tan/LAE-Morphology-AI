import numpy as np
import torch
from torch.utils.data import Dataset
import pandas as pd
from astropy.io import fits

from image_loader import (
    create_f277w_dict,
    create_obj_dict,
    create_asy_dict,
    make_crop
)


class GalaxyDataset(Dataset):

    def __init__(self, csv_path):

        self.df = pd.read_csv(csv_path)

        self.f277w_dict = create_f277w_dict()

        self.obj_dict = create_obj_dict()

        self.asy_dict = create_asy_dict()
    
    def __len__(self):

        return len(self.df)

    def __getitem__(self, idx):

        row = self.df.iloc[idx]

        obj_id = int(row["id"])

        f277w_path = self.f277w_dict[obj_id]
        obj_path = self.obj_dict[obj_id]
        asy_path = self.asy_dict[obj_id]

        f277w = make_crop(
            f277w_path,
            zoom_size=100
        ).astype("float32")

        obj = make_crop(
            obj_path,
            zoom_size=100
        ).astype("float32")

        asy = make_crop(
            asy_path,
            zoom_size=100
        ).astype("float32")

        image = np.stack(
            [f277w, obj, asy],
            axis=0
        )

        label = [
            int(row["detectable"]),
            int(row["bright_neighbor"]),
            int(row["multiple_component"]),
            int(row["point_source"]),
        ]

        image = torch.tensor(
            image,
            dtype=torch.float32
        )

        label = torch.tensor(
            label,
            dtype=torch.float32
        )

        return {
            "id": obj_id,
            "image": image,
            "label": label
        }