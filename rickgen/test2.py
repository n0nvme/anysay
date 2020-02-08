from PIL import Image

imPath = "pickle.png"

im = Image.open(imPath)

scale_factor = 11

half = Image.new("RGBA", tuple([int(d / scale_factor) for d in im.size]))

for i in range(im.size[0]):
    for j in range(im.size[1]):
        if i % scale_factor == 0 and j % scale_factor == 0:
            try:
                half.putpixel(
                    (int(i / scale_factor), int(j / scale_factor)), im.getpixel((i, j))
                )
            except:
                pass

half.save("test4.png")

