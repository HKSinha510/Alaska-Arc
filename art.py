from PIL import Image, ImageDraw, ImageChops
from random import randint, random
import colorsys

def random_color():  #generating random colors
    h = random()
    s = 1
    v = 1

    float_rgb = colorsys.hsv_to_rgb(h, s, v)
    rgb = [int(x * 255) for x in float_rgb]

    return tuple(rgb)

def fade_colors(start_color, end_color, factor: float):  #Shifting from start color to end color
    reciprocal = 1 - factor
    return (
        int(start_color[0] * reciprocal + end_color[0] * factor),
        int(start_color[1] * reciprocal + end_color[1] * factor),
        int(start_color[2] * reciprocal + end_color[2] * factor)
    )

def test():
    img = Image.open('test.png')
    rgba = img.convert("RGBA")
    datas = rgba.getdata()
    
    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:  # finding black colour by its RGB value
            # storing a transparent value when we find a black colour
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)  # other colours remain unchanged
    
    rgba.putdata(newData)
    rgba.save("Final.png", "PNG")

def generate_art():
    print("Generating Art")
    target_size_px = 512
    scale_factor = 5
    image_size_px = target_size_px * scale_factor
    padding = int((3/100) * image_size_px)
    background_color = (0,0,0)
    image = Image.new("RGB", (image_size_px, image_size_px), background_color)

    draw = ImageDraw.Draw(image)
    points = []

    #generating points
    print("Generating points")
    for _ in range(0, 10):
        random_point = (randint(padding, image_size_px - padding), randint(padding, image_size_px - padding))
        points.append(random_point)

    #drawing box
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])
    #draw.rectangle((min_x, min_y, max_x, max_y), outline=(255, 0, 0), width=10)

    #centering the image
    print("Centering the image")
    delta_x = min_x - (image_size_px - max_x)
    delta_y = min_y - (image_size_px - max_y)

    for i, point in enumerate(points):
        points[i] = (point[0] - delta_x // 2, point[1] - delta_y // 2)

    #drawing box
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])
    #draw.rectangle((min_x, min_y, max_x, max_y), outline=(0, 255, 0), width=10)

    #making the art
    print("Drawing lines")
    thickness = 0
    n_points = len(points) - 1
    start_color = random_color()
    end_color = random_color()
    for i, point in enumerate(points):
        #overlay_canvas
        overlay_image = Image.new("RGB", (image_size_px, image_size_px), background_color)
        overlay_draw = ImageDraw.Draw(overlay_image)

        p1 = point

        if i == n_points:
            p2 = points[0]

        else:
            p2 = points[i + 1]

        line_xy = (p1, p2)
        factor = i / n_points
        line_color = fade_colors(start_color, end_color, factor)
        thickness += int(padding / scale_factor)
        overlay_draw.line(line_xy, line_color, width = thickness)
        image = ImageChops.add(image, overlay_image)

    image = image.resize((1024,1024), resample=Image.ANTIALIAS)

    print("Saving the file")
    image.save("test.png")
    test()

if __name__ == "__main__":
    generate_art()
    