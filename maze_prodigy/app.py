from dataclasses import dataclass
from typing import TYPE_CHECKING
import sys

import customtkinter
from screeninfo import get_monitors, Enumerator

from assets.themes import get_theme_path
from controllers import MenuController, MazeController, ResultController
from common import Dimensions, Stateful

if TYPE_CHECKING:
    from controllers import Controller


class App(Stateful):

    __APP_TITLE = "Maze Solver"

    def __init__(self):

        self.__window = self.__create_and_configure_window()
        self.__menu_controller = MenuController(self)
        self.__maze_controller: MazeController = None
        self.__result_controller: ResultController = None

        self.__state = self.__AppState(
            title = self.__APP_TITLE,
            window_dimensions = Dimensions(self.__window.winfo_height(), self.__window.winfo_width()),
            safe_area_padding = 40
        )


    def launch_and_wait_until_closed(self):
        self.__window.mainloop()


    def set_controller(self, controller: "Controller"):
        if isinstance(controller, MazeController):
            self.__maze_controller = controller
        elif isinstance(controller, ResultController):
            self.__result_controller = controller

    
    def go_back_to_main_menu(self):
        if hasattr(self.__maze_controller, "destroy"):
            self.__maze_controller.destroy()

        if hasattr(self.__result_controller, "destroy"):
            self.__result_controller.destroy()
        
        self.__menu_controller.hide_view(False)

    
    def close_window(self):
        self.__window.destroy()


    @property
    def window(self) -> customtkinter.CTk:
        return self.__window
    

    def get_state(self) -> "App.__AppState":
        return self.__state


    def __create_and_configure_window(self) -> customtkinter.CTk:
        window = customtkinter.CTk()

        customtkinter.set_default_color_theme(get_theme_path("basic_theme.json"))
        customtkinter.set_appearance_mode("dark")

        window.title(self.__APP_TITLE)
        window.attributes("-fullscreen", True)

        if not getattr(sys, 'frozen', False):
            screen = Dimensions(window.winfo_screenheight(), window.winfo_screenwidth())
            window.geometry("{}x{}".format(screen.width, screen.height))

        window.resizable(width = False, height = False)
        return window
    

    @dataclass(frozen = True)
    class __AppState():
        title: str
        window_dimensions: Dimensions
        safe_area_padding: int