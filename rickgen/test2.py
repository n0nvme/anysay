from PIL import Image

imPath = "pickle.png"

im = Image.open(imPath)

half = Image.new("RGBA", tuple([int(d / 11) for d in im.size]))

for i in range(im.size[0]):
    for j in range(im.size[1]):
        if i % 11 == 0 and j % 11 == 0:
            try:
                half.putpixel((int(i / 11), int(j / 11)), im.getpixel((i, j)))
            except:
                pass

half.save("test4.png")

