import os
import re

from PIL import Image

from .resize import resize
from .image_to_ascii import image_to_ascii


IMAGE_FORMATS = [r".png$", r".jpg$"]
WORKDIR = os.path.join(os.getenv("HOME"), ".config/anysay/pics")


def check_dir():
    if not os.path.isdir(WORKDIR):
        os.makedirs(WORKDIR)


def save_ascii(ascii_image, filename):
    new_pic = os.path.join(WORKDIR, filename)

    while os.path.isfile(new_pic):
        print(
            f"{filename} is exist. Enter new file name or leave blank to rewrite file:"
        )
        new_filename = input()

        if new_filename == "":
            break

        new_pic = os.path.join(WORKDIR, new_filename)

    with open(new_pic, "w") as f:
        f.write(ascii_image)


def add_files(filesname: list, debug=False):
    check_dir()

    if type(filesname) is str:
        filesname = [filesname]

    for filename in filesname:
        if os.path.isdir(filename):
            if debug:
                print([os.path.join(filename, f) for f in os.listdir(filename)])

            for filename in [os.path.join(filename, f) for f in os.listdir(filename)]:
                save_file(filename, debug=debug)
        elif os.path.isfile(filename):
            save_file(filename, debug=debug)
        else:
            print(f"Cannot access to {filename}: no such file or directory")


def prepare_file(filename, debug=False):
    for im_format in IMAGE_FORMATS:
        if debug:
            print(filename)

        if re.search(im_format, filename, flags=re.IGNORECASE):
            im = Image.open(filename)

            if type(im.getpixel((0, 0))) is int:
                im = im.convert("RGBA")

            width, height = im.size

            if width > 64 and height > 64:
                im = resize(im, debug)
            im = image_to_ascii(im)

            break
    
    return im


def save_file(filename, debug=False):
    ascii_image = prepare_file(filename, debug=debug)

    if ascii_image:
        save_ascii(ascii_image, os.path.split(filename)[-1])
