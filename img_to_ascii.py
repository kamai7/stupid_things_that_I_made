from PIL import Image, ImageDraw, ImageFont


class Asciizer:
    def __init__(self,path_to_img, path_to_font):
        self.img_path = path_to_img
        self.result = ""
        self.charset = " .:;+*#%@"
        self.characters_size = 20
        self.keep_pixels_color = False
        self.color_space = 255
        self.path_to_font = path_to_font
        self.font = ImageFont.truetype(path_to_font, size=self.characters_size)
    
    def convert(self,  divider=1, color_space=255, grayscale = False, keep_pixels_color = False, charachters_size = 20, characters_format = True):
        self.characters_size = charachters_size
        self.keep_pixels_color = keep_pixels_color
        self.color_space = color_space
        self.font = self.font = ImageFont.truetype(self.path_to_font, size=self.characters_size)
        try:
            img = Image.open(self.img_path)
        except ValueError as e:
            print("Image not found:", e)

        width = divider/(self.font.getmetrics()[0]/self.font.getlength("#")) if characters_format else divider
        img = img.resize((int(img.width/width), int(img.height/divider)))
        self.result = self.ascii(img, width/divider)

        if grayscale:
            self.result = self.result.convert("L")
        return self.result
    
    def save(self,save_name):
        try:
            self.result.save(f"{save_name}.png")
        except (ValueError, KeyError, NameError) as e:
            print("Name not valid:", e)

    def ascii(self, img, length_ratio):
        char_height = int(self.font.getmetrics()[0])
        char_length = int(char_height*length_ratio)
        img_loaded = self.set_color(img).load()
        ret = Image.new("RGB", (img.width*char_length, img.height*char_height), "black")
        draw = ImageDraw.Draw(ret)
        for i in range(img.width):
            for j in range(img.height):
                index_r = (img_loaded[i,j][0]//(255//len(self.charset))) - 1
                index_g = (img_loaded[i,j][1]//(255//len(self.charset))) - 1
                index_b = (img_loaded[i,j][2]//(255//len(self.charset))) - 1
                symbol_index = max(index_r, index_g, index_b)
                symbol = self.charset[symbol_index]
                draw.text((i*char_length, j*char_height), symbol, font=self.font, fill=(img_loaded[i,j][0], img_loaded[i,j][1], img_loaded[i,j][2]))
        return ret
       
    def set_color(self, img):
        img_loaded = img.load()
        color_divider = 255//self.color_space
        for i in range(img.width):
            for j in range(img.height):
                new_r = (img_loaded[i,j][0]//color_divider) * color_divider
                new_g = (img_loaded[i,j][1]//color_divider) * color_divider
                new_b = (img_loaded[i,j][2]//color_divider) * color_divider
                img_loaded[i,j] = (new_r, new_g, new_b)
        return img

ascii = Asciizer("base\\base1.png", "CascadiaMono-Regular.ttf")
img = ascii.convert(divider=32)
img.show()
ascii.save("results\\matchCharacters")
img2 = ascii.convert(divider=32, characters_format=False)
img2.show()
ascii.save("results\\matchPixels")