import logging
import os

import magic
from PIL import Image
from tqdm import tqdm

from .image_to_ascii import image_to_ascii
from .resize import resize

logger = logging.getLogger(__name__)
# FIXME : move parameters to config file
IMAGE_FORMATS = ["image/png", "image/jpeg"]
WORKDIR = os.path.join(os.getenv("HOME"), ".config/anysay/pics")
xterm256 = os.path.join(WORKDIR, "x256_color")
truecolor = os.path.join(WORKDIR, "true_color")
# ttycolor = os.path.join(WORKDIR, "tty_color")

colors = {"xterm256": xterm256, "truecolor": truecolor}


def check_dir():
    for DIR in [WORKDIR, xterm256, truecolor]:
        if not os.path.isdir(DIR):
            print(f"mkdir {DIR}")
            os.makedirs(DIR)


def save_ascii(ascii_image, filename, save_dir):
    new_pic = os.path.join(save_dir, filename)

    while os.path.isfile(new_pic):
        print(
            f"{filename} is exist. Enter new file name or leave blank to rewrite file:"
        )
        new_filename = input()

        if new_filename == "":
            break

        new_pic = os.path.join(save_dir, new_filename)

    with open(new_pic, "w") as f:
        f.write(ascii_image)


def normalization_files_list(filesname: list) -> list:
    result = []
    for filename in filesname:
        if os.path.isdir(filename):
            result.extend([os.path.join(filename, f) for f in os.listdir(filename)])
        elif os.path.isfile(filename):
            result.append(filename)
        else:
            print(f"Cannot access to {filename}: no such file or directory")
    return result


def add_files(filesname: list):
    check_dir()

    if type(filesname) is str:
        filesname = [filesname]

    filesname = normalization_files_list(filesname)
    logger.debug(filesname)
    for filename in tqdm(filesname, desc="Files"):
        save_file(filename)


def prepare_file(filename, color):
    file_type = magic.from_file(filename, mime=True)
    logger.debug(f"{filename}, {file_type}")

    if file_type in IMAGE_FORMATS:
        im = Image.open(filename)
        logger.debug(f"First pixel is {im.getpixel((0, 0))}")
        logger.debug(f"Picure color type: {im.mode}")
        logger.debug(f"Requirement color is {color}")

        if type(im.getpixel((0, 0))) is int:
            im = im.convert("RGB")
        width, height = im.size

        if width > 64 and height > 64:
            im = resize(im)
            logger.debug(f"color after resize { im.getpixel((0, 0))}")

        if color == "xterm256":
            im = im.convert("RGB")
        im = image_to_ascii(im, color)
    else:
        im = "Invalid file type"

    return im


def save_file(filename):
    for color in tqdm(
        colors, desc=f"generating file {os.path.split(filename)[-1]}", leave=False
    ):
        ascii_image = prepare_file(filename, color=color)

        if ascii_image:
            save_ascii(ascii_image, os.path.split(filename)[-1], save_dir=colors[color])
