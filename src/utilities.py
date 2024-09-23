from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage


def convert_png_to_photoImage(png: str, size: tuple[int, int]) -> PhotoImage:
    img_file = Image.open(png)
    img_file = img_file.resize(size)
    img_file = ImageTk.PhotoImage(img_file)
    return img_file
