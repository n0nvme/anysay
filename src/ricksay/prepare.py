import os

import magic
from tqdm import tqdm
from PIL import Image

from .resize import resize
from .image_to_ascii import image_to_ascii

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


def add_files(filesname: list, debug=False):
    check_dir()

    if type(filesname) is str:
        filesname = [filesname]

    filesname = normalization_files_list(filesname)
    if debug:
        print(filesname)
    # outer = tqdm.tqdm(total=len(filesname), desc="Files", position=0)
    for filename in tqdm(filesname, desc="Files"):
        save_file(filename, debug=debug)
        # outer.set_description_str(f"Current file: {filename}")
        # outer.update(1)


def prepare_file(filename, color, debug=False):
    file_type = magic.from_file(filename, mime=True)
    if debug:
        print(f"{filename}, {file_type}")

    if file_type in IMAGE_FORMATS:
        im = Image.open(filename)
        if debug:
            print(im.getpixel((0, 0)))
            print(f"in mode picure: {im.mode}")
            print(f"requirement color is {color}")

        if type(im.getpixel((0, 0))) is int:
            im = im.convert("RGB")

        width, height = im.size

        if width > 64 and height > 64:
            im = resize(im, debug)
        if color == "xterm256":
            im = im.convert("RGB")
        im = image_to_ascii(im, color)
    else:
        im = "Invalid file type"

    return im


def save_file(filename, debug=False):
    for color in tqdm(
        colors, desc=f"generating file {os.path.split(filename)[-1]}", leave=False
    ):
        ascii_image = prepare_file(filename, color=color, debug=debug)

        if ascii_image:
            save_ascii(ascii_image, os.path.split(filename)[-1], save_dir=colors[color])
