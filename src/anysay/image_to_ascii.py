from PIL import Image
from sty import bg, fg, rs
from tqdm import tqdm

import logging

from colored import attr as attr_c
from colored import bg as bg_c
from colored import fg as fg_c


logger = logging.getLogger(__name__)


def convert_truecolor_char(rgba0, rgba1):
    top = rgba0[:3]
    bottom = rgba1[:3]
    char = "▄"
    if len(rgba0) > 3 and rgba0[3] == 0:
        top = fg.rs
    if len(rgba1) > 3 and rgba1[3] == 0:
        bottom = bg.rs
        char = " "

    logger.debug(f"top color: {rgba0} botom color: {rgba1}")
    result = bg(*top) + fg(*bottom) + char + rs.all
    return result


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def convert_256_color_char(hex_bg, hex_fg):
    color = fg_c(hex_fg) + bg_c(hex_bg)
    res = attr_c("reset")
    char = "▄"
    result = color + char + res
    return result


def image_to_ascii(image: Image, color):
    result = ""

    for y in range(0, image.size[1], 2):
        string = ""
        for x in range(image.size[0]):
            if image.size[1] - y != 1:
                rgba1 = image.getpixel((x, y + 1))
            else:
                rgba1 = image.getpixel((0, 0))

            rgba0 = image.getpixel((x, y))
            if color == "xterm256":
                hex_bg = rgb2hex(*rgba0)
                hex_fg = rgb2hex(*rgba1)
                string += convert_256_color_char(hex_bg, hex_fg)
            elif color == "truecolor":
                string += convert_truecolor_char(rgba0, rgba1)
        result += string + "\n"
    return result
