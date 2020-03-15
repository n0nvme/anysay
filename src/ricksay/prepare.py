import os 
import re

from PIL import Image

from resize import resize
from image_to_ascii import image_to_ascii


IMAGE_FORMATS = [r".png$", r".jpg$"]
WORKDIR = os.path.join(os.getenv("HOME"), "project/ricksay/rickgen")
SOURCEDIR = os.path.join(WORKDIR, 'source')
RESIZEDIR = os.path.join(WORKDIR, 'ready')
DONEDIR = os.path.join(os.getenv("HOME"), "project/ricksay/ricks")


def check_dir():
    if not os.path.isdir(RESIZEDIR):
        os.mkdir(RESIZEDIR)


def save_ascii(image):
    result = image_to_ascii(image)
    ricks = os.listdir(DONEDIR)
    new_rick = os.path.join(DONEDIR, f"ricks{len(ricks)}")
    with open(new_rick, 'w') as file:
        file.write(result)


def prepare(files):
    check_dir()
    for file in [fl._mode for fl in files]:
        for im_format in IMAGE_FORMATS:
            if re.search(im_format, file):
                im = Image.open(file)
                resultfile = resize(im)
                filename = os.path.join(RESIZEDIR, os.path.split(file)[1])
                resultfile.save(filename)
                save_ascii(resultfile)
                break


if __name__ == "__main__":
    check_dir()
    files = os.listdir(os.path.join(os.getenv("HOME"), WORKDIR))
    prepare(files)
