from PIL import Image


def pixel_size(image):
    print("start pixel size")
    minimalsize0 = 1_000_000
    minimalsize1 = 0
    count = 0
    tempRGB0 = image.getpixel((0, 0))
    print(type(tempRGB0))
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            tempRGB1 = image.getpixel((x, y))

            if tempRGB0 == tempRGB1:
                x1 = x
                y1 = y
                while tempRGB0 == image.getpixel((x1, y1)):
                    minimalsize1 += 1
                    if image.size[0] > (x1 + 1):
                        x1 += 1
                        if image.size[1] > (y1 + 1):
                            y1 += 1
                        else:
                            break
                    else:
                        break
                else:
                    x = x1
                    y = y1
            if minimalsize1 > 9:
                if minimalsize1 == minimalsize0:
                    if count == 3:
                        return minimalsize1
                    else:
                        count += 1
                else:
                    if minimalsize1 < minimalsize0:
                        print(minimalsize1)
                        minimalsize0 = minimalsize1

            minimalsize1 = 0
            x = x1
            y = y1


def alternative_min_pixel_size(image):
    listsize = []
    noise = 2
    tempRGB0 = image.getpixel((0, 0))
    min_y = None
    max_y = None
    height = image.size[1] - 1
    width = image.size[0] - 1
    if len(image.getpixel((0, 0))) > 3:
        for y in range(height):
            sum_x = 0
            for x in range(width):
                sum_x += image.getpixel((x, y))[3]
                print(image.getpixel((x, y)))
            if sum_x != 0 and not min_y:
                min_y = y
            elif sum_x == 0 and min_y and not max_y:
                max_y = y - 1
    if not min_y:
        min_y = 0
    if not max_y:
        max_y = height

    print(f"{min_y}, {max_y}")

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
                print(size)
            tempRGB0 = image.getpixel((x, y))

        maxcount = [0, 0]

        count = 0
        listsize_t.sort()
        print(listsize_t)
        if len(listsize_t) > 1:
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
        print(f"old y {y}, incres by {maxcount[1]}")
        if maxcount[1] == 0 :
            y += 1
        else:
            y += maxcount[1]
        print(f"max count {maxcount[0]}, size {maxcount[1]} ")
        print(f"size image{image.size}")
        print(f"in algirtm {x},{y}")
        print(f"{min_y}, {max_y}")
    
    listsize.sort()
    print(listsize)
    tsize = 0
    print(f"abc {sum(listsize) // len(listsize)}")
    print(f"mediana {listsize[len(listsize) // 2]}")
    count = 0
    maxcount = [0, 0]
    for size in listsize:
        if tsize == size:
            count += 1
        else:
            tsize = size
            if maxcount[0] < count and tsize > 3:
                maxcount[0] = count
                maxcount[1] = tsize
            count = 0
    print(maxcount)

    return maxcount[1] - 1


def resize(source_image, debug=False, result_name="debug_image.png"):
    print(source_image.size)
    width, height = source_image.size
    scale_factor = pixel_size(source_image)
    scale_factor = alternative_min_pixel_size(source_image)
    if not scale_factor or height // scale_factor > 56:
        scale_factor = height // 56

    print(scale_factor)
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
    if debug:
        half.save(result_name)

    return half


if __name__ == "__main__":
    imPath = "/home/tedkon/project/ricksay/rickgen/source/random/pixelcat2.png"
    source_image = Image.open(imPath)
    resize(source_image, True)
    # alternative_min_pixel_size(source_image)
