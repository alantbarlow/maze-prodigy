from pkgutil import get_data
from typing import TYPE_CHECKING
from io import BytesIO

from customtkinter import CTkImage
from PIL import Image, ImageTk

if TYPE_CHECKING:
    from common import Dimensions


def get_image(file_name: str, dimensions: "Dimensions", canvas_mode: bool = False ) -> CTkImage | ImageTk.PhotoImage:
    image_data = get_data(__name__, file_name)
    image = Image.open(BytesIO(image_data))
    
    if canvas_mode:
        return ImageTk.PhotoImage(image.resize((dimensions.width, dimensions.height)))

    else:
        return CTkImage(dark_image = image, size = (dimensions.width, dimensions.height))
    
