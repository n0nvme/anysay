import argparse
import os

from .say import say
from .resize import resize
from .prepare import prepare


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--prepare",
        help="prepare all image in folder",
        nargs="+",
        type=argparse.FileType,
    )
    parser.add_argument("-s", "--string", default="Hello !!")
    args = parser.parse_args()
    return args

def main():
    args_main = arg_parse()
    if args_main.prepare:
        print(args_main.prepare)
        prepare(args_main.prepare)
    else:
        say()
        print(args_main.string)
