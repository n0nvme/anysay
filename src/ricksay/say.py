import os
import random


def say():
    ricks_path = os.path.join(os.getenv("HOME"), ".config/ricksay/ricks/")
    if not os.path.exists(ricks_path):
        print("NO SUCH PATH")
        return ""
    ricks = os.listdir(ricks_path)
    random_rick = random.randint(0, len(ricks) - 1)
    random_rick = f"{ricks_path}/{ricks[random_rick]}"
    # print(random_rick)
    with open(random_rick, "r") as f:
        print(f.read())
