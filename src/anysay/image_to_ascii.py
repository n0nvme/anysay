from PIL import Image
from sty import bg, fg, rs
from tqdm import tqdm

import logging

from colored import attr as attr_c
from colored import bg as bg_c
from colored import fg as fg_c

from .resize import asci_border


logger = logging.getLogger(__name__)


def convert_truecolor_char(top_color, bottom_color):
    top = top_color[:3]
    bottom = bottom_color[:3]
    if len(top_color) > 3 and len(bottom_color) > 3:
        if top_color[3] == bottom_color[3]:
            if top_color[0] == 0:
                top = bg.rs
                char = " "
            else:
                char = "█"

        elif top_color[3] == 0:
            top = bg.rs
            char = "▄"
        else:
            bottom = top
            top = bg.rs
            char = "▀"

    # logger.debug(f"top color: {rgba0} botom color: {rgba1}")
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


def pixel_to_asci(top_color, bottom_color, colors_term):

    if colors_term == "xterm256":
        hex_bg = rgb2hex(*top_color)
        hex_fg = rgb2hex(*bottom_color)
        char = convert_256_color_char(hex_bg, hex_fg)
    elif colors_term == "truecolor":
        char = convert_truecolor_char(top_color, bottom_color)

    return char


def image_to_ascii(image: Image, colors_term) -> str:
    asci_image = ""
    for y in range(0, image.size[1], 2):
        string = ""
        for x in range(image.size[0]):
            if image.size[1] - y != 1:
                rgba1 = image.getpixel((x, y + 1))
            else:
                rgba1 = image.getpixel((0, 0))

            rgba0 = image.getpixel((x, y))
            string += pixel_to_asci(rgba0, rgba1, colors_term)
        asci_image += string + "\n"

    asci_image = asci_border(asci_image)
    return asci_image


def bordered_message(mes: str, border_color, colors_term) -> str:
    midle_char = pixel_to_asci(border_color, border_color, colors_term)
    top_angle_char = pixel_to_asci(border_color, (0, 0, 0, 0), colors_term)
    top_char = pixel_to_asci((0, 0, 0, 0), border_color, colors_term)
    bottom_angle_char = top_char
    bottom_char = top_angle_char

    messages_lines = mes.split("\n")
    max_line_len = max([len(line) for line in messages_lines])

    border_message = (
        f"\n\n  {top_angle_char}{top_char * (max_line_len + 3)}{top_angle_char}\n"
    )

    for line in messages_lines:
        addition_spaces = " " * (max_line_len - len(line))
        border_message += f" {midle_char}  {line}{addition_spaces}   {midle_char}\n"

    border_message += (
        f"  {bottom_angle_char}{bottom_char * (max_line_len + 3)}{bottom_angle_char}\n"
    )

    return border_message
