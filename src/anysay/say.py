import logging
import os
import random

logger = logging.getLogger(__name__)


def say(color):

    if color == "truecolor":
        pics_path = os.path.join(os.getenv("HOME"), ".config/anysay/pics/true_color")

    elif color == "xterm256":
        pics_path = os.path.join(os.getenv("HOME"), ".config/anysay/pics/x256_color")

    elif color == "tty":
        pics_path = os.path.join(os.getenv("HOME"), ".config/anysay/pics/tty_color")

    logger.debug(f"terminal color mode is {color}")
    logger.debug(f"take file from {pics_path}")

    if not os.path.exists(pics_path):
        logger.warning("NO SUCH PATH")
        return None

    pics = os.listdir(pics_path)
    random_pic = random.randint(0, len(pics) - 1)
    random_pic = f"{pics_path}/{pics[random_pic]}"
    logger.debug(f"print pics is {random_pic}")
    with open(random_pic, "r") as f:
        print(f.read())
