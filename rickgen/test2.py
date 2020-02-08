from PIL import Image

imPath = "pickle.png"

im = Image.open(imPath)

factor = 11

half = Image.new("RGBA", tuple([int(d / factor) for d in im.size]))

for i in range(im.size[0]):
    for j in range(im.size[1]):
        if i % factor == 0 and j % factor == 0:
            try:
                half.putpixel((int(i / factor), int(j / factor)), im.getpixel((i, j)))
            except:
                pass

half.save("test4.png")

