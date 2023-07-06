from typing import Optional, Tuple, Union
from customtkinter import CTkLabel
from PIL import Image, ImageTk
from customtkinter import CTkLabel

from assets.images import get_image
from common import Dimensions



class Star(CTkLabel):

    __width = 50
    __height = 50

    def __init__(self, master: any, is_completed: bool):
        super().__init__(master, width = self.__width, height = self.__height, text = "")

        image_file = "star_outline.png"
        if is_completed:
            image_file = "star.png"

        self.__image = get_image(image_file, Dimensions(self.__height, self.__width))

        self.configure(image = self.__image)