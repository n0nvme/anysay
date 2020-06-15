import argparse
import logging
import os
import pathlib

from .prepare import add_files, prepare_file
from .say import say

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format="%(message)s")
logger = logging.getLogger(__name__)

# FIXME : move workdirs to config file
WORKDIR = os.path.join(os.getenv("HOME"), ".config/anysay/pics")
xterm256 = os.path.join(WORKDIR, "x256_color")
truecolor = os.path.join(WORKDIR, "true_color")
# ttycolor = os.path.join(WORKDIR, "tty_color")


def get_color_terminal(argument):
    if argument.truecolor:
        color = "truecolor"

    elif argument.xterm256:
        color = "xterm256"

    else:
        color = os.environ.get("COLORTERM")

    if not color:
        color = "tty"

    return color


def arg_parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    color = parser.add_mutually_exclusive_group()
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

    color.add_argument(
        "--truecolor", help="print pic in truecolor mode", action="store_true"
    )
    color.add_argument(
        "--xterm256", help="print pic in xterm256 mode", action="store_true"
    )
    args = parser.parse_args()
    return args


def main():
    args_main = arg_parse()
    if args_main.verbose:
        logger.setLevel(logging.DEBUG)
    logger.debug(args_main)

    color = get_color_terminal(args_main)

    if args_main.add_files:

        logger.debug(args_main.add_files)
        add_files(args_main.add_files)

    elif args_main.preview:
        print(prepare_file(args_main.preview.name, color=color))

    elif args_main.string:
        pictires_exist = True
        for DIR in [xterm256, truecolor]:
            if not os.path.isdir(DIR) or len(os.listdir(DIR)) == 0:
                pictires_exist = False

        if pictires_exist:
            say(color)
            result = " ".join(args_main.string)
            print(result)

        else:
            for DIR in [xterm256, truecolor]:
                if not os.path.isdir(DIR) or len(os.listdir(DIR)) == 0:
                    logger.info(
                        f"not found pictures in {DIR}\ngenerating default pictures to {DIR}..."
                    )
                    logger.debug(
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
                        )
                    )
                    logger.info("ready")
                    say(color)
                    result = " ".join(args_main.string)
                    print(result)


if __name__ == "__main__":
    main()

__all__ = ["main"]
