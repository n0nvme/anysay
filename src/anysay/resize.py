import logging

from PIL import Image

logger = logging.getLogger(__name__)


def pixel_size(image: Image.Image, noise=3):
    listsize = []
    tempRGB0 = image.getpixel((0, 0))

    # logger.debug(tempRGB0)

    min_y = None
    max_y = None
    height = image.size[1] - 1
    width = image.size[0] - 1

    if type(tempRGB0) is not int and len(tempRGB0) > 3:
        for y in range(height):
            sum_x = 0
            for x in range(width):
                sum_x += image.getpixel((x, y))[3]
            if sum_x != 0 and not min_y:
                min_y = y
            elif sum_x == 0 and min_y and not max_y:
                max_y = y - 1

    if not min_y:
        min_y = 0

    if not max_y:
        max_y = height
    y = min_y

    while y + 2 <= max_y:
        listsize_t = []
        for x in range(width):
            size = 0
            y1 = y

            while tempRGB0 == image.getpixel((x, y1)):
                size += 1
                if width > (x + 1) and height > (y1 + 1):
                    x += 1
                    y1 += 1
                else:
                    break
            else:
                if size > noise:
                    listsize.append(size)
                    listsize_t.append(size)
            tempRGB0 = image.getpixel((x, y))

        maxcount = [0, 0]

        count = 0
        listsize_t.sort()
        if len(listsize_t) > 3:
            tsize = listsize_t[0]
        else:
            tsize = 0

        for size in listsize_t:
            if tsize == size:
                count += 1
            else:
                if maxcount[0] < count:
                    maxcount[0] = count
                    maxcount[1] = tsize

                tsize = size
                count = 0
        else:
            if maxcount[0] < count:
                maxcount[0] = count
                maxcount[1] = tsize
        if maxcount[1] <= noise:
            y += 1
        else:
            y += maxcount[1]

    listsize.sort()
    tsize = 0
    count = 0
    maxcount = [0, 0]

    for size in listsize:
        if tsize == size:
            count += 1
        else:
            tsize = size
            if maxcount[0] < count and tsize > noise:
                maxcount[0] = count
                maxcount[1] = tsize
            count = 0

    # logger.debug(maxcount)

    return maxcount[1] - 1


def resize(source_image: Image.Image, result_name="debug_image.png") -> Image:
    # logger.debug(source_image.size)
    _, height = source_image.size
    scale_factor = pixel_size(source_image)

    if not scale_factor or height // scale_factor > 65:
        scale_factor = height // 56

    logger.debug(f"scale factor image is: {scale_factor}")

    half = Image.new("RGBA", tuple([int(d // scale_factor) for d in source_image.size]))

    for i in range(source_image.size[0]):
        for j in range(source_image.size[1]):
            if i % scale_factor == 0 and j % scale_factor == 0:
                try:
                    half.putpixel(
                        (int(i // scale_factor), int(j // scale_factor)),
                        source_image.getpixel((i, j)),
                    )
                except:
                    pass

    return half


def cut_image(image: Image.Image) -> Image:
    right, bottom = image.size
    print(image.size)
    top = 0
    top_pixel, bottom_pixel, right_pixel, left_pixel = False, False, False, False
    for height_pointer in range(top, bottom):
        x = 0
        image_colors_on_line = [
            image.getpixel((i, height_pointer)) for i in range(right)
        ]
        for color_pixel in image_colors_on_line:
            r, g, b, _ = color_pixel
            color_summ = r + g + b

            if color_summ != 0:
                if not top_pixel:
                    top_pixel = height_pointer

                if not left_pixel:
                    left_pixel = x
                elif x < left_pixel:
                    left_pixel = x

                if x > right_pixel:
                    right_pixel = x

                if bottom_pixel:
                    bottom_pixel = height_pointer
            if color_summ == 0:
                if top_pixel and not bottom_pixel:
                    bottom_pixel = height_pointer
            x += 1
    print(left_pixel, top_pixel, right_pixel, bottom_pixel)

    only_image = image.crop((left_pixel, top_pixel, right_pixel, bottom_pixel))

    return only_image


def asci_border(asci_image: str) -> str:
    result_image = "\n\n"
    image_lines = asci_image.split("\n")

    for line in image_lines:
        result_image += "    " + line + "\n"

    return result_image
