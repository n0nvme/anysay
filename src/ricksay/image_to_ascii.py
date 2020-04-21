from PIL import Image
from sty import bg, fg


def convert_color_char(rgba0, rgba1):
    top = rgba0[:3]
    bottom = rgba1[:3]
    char = "▄"
    if rgba0[3] == 0:
        top = fg.rs
    if rgba1[3] == 0:
        bottom = bg.rs
        char = " "

    result = bg(*top) + fg(*bottom) + char + fg.rs + bg.rs
    return result


def image_to_ascii(image: Image):
    result = ""
    for y in range(0, image.size[1], 2):
        string = ""
        for x in range(image.size[0]):
            if image.size[1] - y != 1:
                rgba1 = image.getpixel((x, y + 1))
            else:
                rgba1 = image.getpixel((0, 0))

            rgba0 = image.getpixel((x, y))
            string += convert_color_char(rgba0, rgba1)
        result += string + "\n"
    return result
