import argparse

# import os

# from .resize import resize
from prepare import prepare
from say import say


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
        "string",
        help="return random rick with youre string",
        nargs="+",
        type=str
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args_main = arg_parse()
    print(args_main)
    if args_main.prepare:
        print(args_main.prepare)
        prepare(args_main.prepare)
    elif args_main.string:
        say()
        result = ""
        for s in args_main.string:
            result += f"{s} "
        print(result)
