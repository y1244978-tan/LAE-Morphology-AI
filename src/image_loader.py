import glob

BASE_PATH = (
    r"../images_all"
)

def get_f277w_files():

    return glob.glob(
        BASE_PATH + r"\images_all_*\**\*.fits",
        recursive=True
    )

def get_obj_files():

    return glob.glob(
        BASE_PATH + r"\images_obj_all_*\**\*.fits",
        recursive=True
    )

def get_asy_files():

    return glob.glob(
        BASE_PATH + r"\images_asy_all_*\**\*.fits",
        recursive=True
    )

#csvのIDと画像の一致
import re

def create_f277w_dict():

    fits_dict = {}

    for file in get_f277w_files():

        match = re.search(
            r"id(\d+)\.fits",
            file
        )

        if match:
            obj_id = int(match.group(1))
            fits_dict[obj_id] = file

    return fits_dict

def create_obj_dict():

    fits_dict = {}

    for file in get_obj_files():

        match = re.search(
            r"id(\d+)\.fits",
            file
        )

        if match:

            obj_id = int(match.group(1))

            fits_dict[obj_id] = file

    return fits_dict

def create_asy_dict():

    fits_dict = {}

    for file in get_asy_files():

        match = re.search(
            r"id(\d+)\.fits",
            file
        )

        if match:

            obj_id = int(match.group(1))

            fits_dict[obj_id] = file

    return fits_dict

#画像の切り出し
from astropy.io import fits
import numpy as np


def make_crop(fits_path, zoom_size=100):

    image = fits.getdata(fits_path)

    center_y = image.shape[0] // 2
    center_x = image.shape[1] // 2

    half = zoom_size // 2

    crop = image[
        center_y-half:center_y+half,
        center_x-half:center_x+half
    ]

    return crop
