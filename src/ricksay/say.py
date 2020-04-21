import os
import random


def say(debug=False):
    pics_path = os.path.join(os.getenv("HOME"), ".config/anysay/pics/")

    if not os.path.exists(pics_path):
        print("NO SUCH PATH")
        return None

    pics = os.listdir(pics_path)
    random_pic = random.randint(0, len(pics) - 1)
    random_pic = f"{pics_path}/{pics[random_pic]}"

    with open(random_pic, "r") as f:
        print(f.read())
