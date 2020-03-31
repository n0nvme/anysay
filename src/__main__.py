import argparse

import os
import pathlib

from ricksay.prepare import prepare
from ricksay.say import say


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--prepare",
        help="prepare all image in folder",
        nargs="+",
        type=argparse.FileType,
    )
    parser.add_argument(
        "string", help="return random rick with your string", nargs="+", type=str
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args_main = arg_parse()
    # print(args_main)
    if args_main.prepare:
        print(args_main.prepare)
        prepare(args_main.prepare)
    elif args_main.string:
        ricks_path = os.path.join(os.getenv("HOME"), ".config/ricksay/ricks/")
        if os.path.exists(ricks_path):
            say()
            result = ""
            for s in args_main.string:
                result += f"{s} "
            print(result)
        else:
            print('~/.config/ricksay/ricks not found\ngenerating default ricks...')
            prepare(os.path.join(pathlib.Path(__file__).parent.absolute(), '../rickgen'))
            print('ready')
            say()
            result = ""
            for s in args_main.string:
                result += f"{s} "
            print(result)
