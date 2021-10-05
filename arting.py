from PIL import Image, ImageDraw

ASCII_CHAR = ['@', '#', '$', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
ASCII_CHAR2 = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
width = int(500/2)

def resize_image(image, new_width=width):
    width, height = image.size
    ratio = height / width
    new_height = int((new_width * ratio)/2)
    resize_image = image.resize((new_width, new_height))
    resize_image.save("resized.png")
    return resize_image

def grayify(image):
    grayscale_image = image.convert("L")
    grayscale_image.save("grayscale_image.png")
    return grayscale_image

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHAR2[pixel//25] for pixel in pixels])
    return characters

def main(new_width=width):
    path = "avatar.png"
    try:
        image = Image.open(path)
        image = image.convert("RGBA")
        pixdata = image.load()
        width, height = image.size
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == (0, 0, 0, 0):
                    pixdata[x, y] = (255, 255, 255, 255)

                if pixdata[x, y] == (255, 255, 255, 0):
                    pixdata[x, y] = (255, 255, 255, 255)

    except:
        print(f"{path} is not a image")

    new_image_data = pixels_to_ascii(grayify(resize_image(image)))

    pixels_count = len(new_image_data)
    ascii_image = "\n".join(new_image_data[i:(i + new_width)]for i in range(0, pixels_count, new_width))

    print(ascii_image)

    location = 'ascii.txt'
    open(location, 'w').write(ascii_image)
    
    blank_image = Image.new('RGB', (1500, 1850), 'white')
    img_draw = ImageDraw.Draw(blank_image)
    title_text = open(location, 'r').read()
    img_draw.text((0, 0), title_text, fill='black')
    blank_image.save('drawn_image.jpg')

if __name__ == "__main__":
    main()