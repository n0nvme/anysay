import argparse

import os
import pathlib


from .prepare import prepare_file, add_files
from .say import say


def arg_parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--add_files",
        help="add files or dir to convert and save to ~/.config/anysay/",
        nargs="+",
    )
    parser.add_argument(
        "-p",
        "--preview",
        help="print without save image from file",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "string",
        help="return random pics with your string",
        nargs="*",
        type=str,
        default=None,
    )
    parser.add_argument("-V", "--verbose", help="Debug info", action="store_true")
    args = parser.parse_args()
    return args


def main():
    args_main = arg_parse()
    debug = args_main.verbose
    if debug:
        print(args_main)

    if args_main.add_files:

        if debug:
            print(args_main.add_files)
        add_files(args_main.add_files)

    elif args_main.preview:
        print(prepare_file(args_main.preview.name))

    elif args_main.string:

        pics_path = os.path.join(os.getenv("HOME"), ".config/anysay/pics/")

        if os.path.exists(pics_path) and len(os.listdir(pics_path)) > 0:
            say(debug=debug)
            result = " ".join(args_main.string)
            print(result)

        else:

            print("~/.config/anysay/pics not found\ngenerating default ricks...")
            if debug:
                print(
                    os.path.normpath(
                        os.path.join(
                            pathlib.Path(__file__).parent.absolute(), "default_pics"
                        )
                    )
                )
            add_files(
                os.path.normpath(
                    os.path.join(
                        pathlib.Path(__file__).parent.absolute(), "default_pics"
                    )
                ),
                debug=debug,
            )
            print("ready")
            say(debug=debug)
            result = " ".join(args_main.string)
            print(result)


__all__ = ["main"]
