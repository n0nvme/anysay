import os
import random


def say(color, debug=False):

    if color == "truecolor":
        pics_path = os.path.join(os.getenv("HOME"), ".config/anysay/pics/true_color")

    elif color == "xterm256":
        pics_path = os.path.join(os.getenv("HOME"), ".config/anysay/pics/x256_color")

    elif color == "tty":
        pics_path = os.path.join(os.getenv("HOME"), ".config/anysay/pics/tty_color")

    if debug:
        print(f"color mode is {color}")
        print(f"take file from {pics_path}")
    if not os.path.exists(pics_path):
        print("NO SUCH PATH")
        return None

    pics = os.listdir(pics_path)
    random_pic = random.randint(0, len(pics) - 1)
    random_pic = f"{pics_path}/{pics[random_pic]}"
    if debug:
        print(f"print pics is {random_pic}")
    with open(random_pic, "r") as f:
        print(f.read())
