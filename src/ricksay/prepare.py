import os
import re

from PIL import Image

from .resize import resize
from .image_to_ascii import image_to_ascii


IMAGE_FORMATS = [r".png$", r".jpg$"]
WORKDIR = os.path.join(os.getenv("HOME"), ".config/ricksay")
SOURCEDIR = os.path.join(WORKDIR, "source")
RESIZEDIR = os.path.join(WORKDIR, "ready")
DONEDIR = os.path.join(os.getenv("HOME"), ".config/ricksay/ricks")


def check_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def save_ascii(image, filename):
    result = image_to_ascii(image)
    # ricks = os.listdir(DONEDIR)
    new_rick = os.path.join(DONEDIR, filename)
    with open(new_rick, "w") as file:
        file.write(result)


def prepare(files_path):
    check_dir(WORKDIR)
    check_dir(DONEDIR)
    for file in os.listdir(files_path):
        for im_format in IMAGE_FORMATS:
            if re.search(im_format, file):
                im = Image.open(os.path.join(files_path, file))
                resultfile = resize(im)
                # filename = os.path.join(RESIZEDIR, os.path.split(file)[1])
                # resultfile.save(filename)
                save_ascii(resultfile, file)
                break
