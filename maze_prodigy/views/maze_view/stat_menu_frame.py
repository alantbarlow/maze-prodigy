from typing import TYPE_CHECKING

from customtkinter import CTkFrame, CTkButton, CTkLabel

from .stat_widget import StatWidget

if TYPE_CHECKING:
    from typing import Callable


class StatMenuFrame(CTkFrame):

    def __init__(self, parent_frame: CTkFrame, main_menu_button_command: 'Callable[..., None]', target_moves: int, target_time: int):
        super().__init__(parent_frame)

        self.__move_stat = StatWidget(self, "Current Moves", 0, target_moves, "moves")
        self.__move_stat.pack()

        self.__time_stat = StatWidget(self, "Current Time", 0, target_time, "seconds")
        self.__time_stat.pack(pady = 70)

        CTkButton(
            master = self,
            text = "Back to Main Menu",
            command = main_menu_button_command
        ).pack(pady = 20)

        CTkLabel(self, text = "Hint: Use your keyboard's arrow keys to traverse the maze", font = ("Roboto", 14), text_color = "grey30").pack()

    
    @property
    def move_stat(self) -> StatWidget:
        return self.__move_stat


    @property
    def time_stat(self) -> StatWidget:
        return self.__time_stat