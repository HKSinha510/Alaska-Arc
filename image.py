from PIL import Image, ImageOps, ImageChops

x = Image.open('avatar.png')

ax = x.convert("RGB")

print(ax.mode)

invert = ImageOps.invert(ax)

invert.save('check.png')