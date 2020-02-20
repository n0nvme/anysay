import argparse
import os

from .say import say
from .resize import resize
from .prepare import prepare
from .say import say


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
        "-s",
        "--say",
        help="return random rick with youre string",
        nargs="+",
        type=str,
    )
    args = parser.parse_args()
    return args

def main():
    args_main = arg_parse()
    if args_main.prepare:
        print(args_main.prepare)
        prepare(args_main.prepare)
    if args_main.say:
        say()
        print(args_main.say)
