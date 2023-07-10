from os import path
from typing import TYPE_CHECKING

from customtkinter import CTkImage
from PIL import Image, ImageTk

if TYPE_CHECKING:
    from common import Dimensions


def get_image(file_name: str, dimensions: "Dimensions", canvas_mode: bool = False ) -> CTkImage | ImageTk.PhotoImage:
    current_path = path.abspath(path.dirname(__file__))
    file_path = path.join(current_path, file_name)

    image = Image.open(file_path)
    
    if canvas_mode:
        return ImageTk.PhotoImage(image.resize((dimensions.width, dimensions.height)))

    else:
        return CTkImage(dark_image = image, size = (dimensions.width, dimensions.height))
    
