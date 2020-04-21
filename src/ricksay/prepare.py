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
    with open(new_pic, "w") as file:
        file.write(ascii_image)

def add_files(files: list, debug=False):
    check_dir()
    if type(files) is str:
        files = [files]
    for file in files:
        if os.path.isdir(file):
            if debug: print([os.path.join(file, f) for f in os.listdir(file)])
            for file in [os.path.join(file, f) for f in os.listdir(file)]:
                save_file(file, debug=debug)
        elif os.path.isfile(file):
            save_file(file, debug=debug)


def prepare_file(file, debug=False):
    for im_format in IMAGE_FORMATS:
        if debug: print(file)
        if re.search(im_format, file, flags=re.IGNORECASE):
            im = Image.open(file)
            if type(im.getpixel((0, 0))) is int:
                im = im.convert('RGBA')
            width, height = im.size
            if width > 64 and height > 64:
                im = resize(im, debug)
            im = image_to_ascii(im)
            break
    return im


def save_file(file, debug=False):
    ascii_image = prepare_file(file, debug=debug)
    if ascii_image:
        save_ascii(ascii_image, os.path.split(file)[-1])
