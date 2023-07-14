from typing import TYPE_CHECKING
from os import path
import sys

from customtkinter import CTkImage
from PIL import Image, ImageTk

if TYPE_CHECKING:
    from common import Dimensions


def get_image(file_name: str, dimensions: "Dimensions", canvas_mode: bool = False ) -> CTkImage | ImageTk.PhotoImage:
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = path.abspath(path.dirname(__file__))

    image_path = path.join(base_path, "images", file_name)
    image = Image.open(image_path)
    
    if canvas_mode:
        return ImageTk.PhotoImage(image.resize((dimensions.width, dimensions.height)))
    else:
        return CTkImage(dark_image = image, size = (dimensions.width, dimensions.height))