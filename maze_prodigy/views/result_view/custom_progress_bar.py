from typing import TYPE_CHECKING

from customtkinter import CTkCanvas

from assets.images import get_image
from common import Dimensions

if TYPE_CHECKING:
    from customtkinter import CTkFrame




class CustomProgressBar(CTkCanvas):

    __height = 26
    __width = 300
    __background_color = '#4A4D50'
    __progress_color = '#1F6AA5'


    def __init__(self, master: "CTkFrame", progress_percentage: float):
        super().__init__(master, width = self.__width, height = self.__height, highlightthickness = 0, bg = self.__background_color)

        self.create_rectangle(0, 0, self.__width * progress_percentage, self.__height, fill = self.__progress_color, outline="")

        self.__image = get_image("custom_progress_bar_dark_corners.png", Dimensions(self.__height, self.__width), canvas_mode = True)

        self.create_image(0, 0, anchor="nw", image = self.__image)

        text = f"{round(progress_percentage * 100)}%"
        if progress_percentage == 1:
            text = "Star Awarded"

        self.create_text(self.__width / 2, self.__height / 2, text = text, fill = "#DCE4EE") 

    


        

