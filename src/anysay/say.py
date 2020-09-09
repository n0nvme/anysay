import logging
import os
import random

from .image_to_ascii import bordered_message

logger = logging.getLogger(__name__)


def say(color, message):

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
        ascii_image = f.read()
    lines_image = ascii_image.split("\n")
    lines_messages = bordered_message(message, (123, 123, 123, 1), color).split("\n")
    result = ""
    for line_im in lines_image:
        result += f"{line_im}{lines_messages.pop() if lines_messages else ''}\n"

    print(result)
