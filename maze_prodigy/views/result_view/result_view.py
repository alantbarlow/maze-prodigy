from dataclasses import dataclass
from typing import TYPE_CHECKING

from customtkinter import CTkFrame, CTkButton, CTkToplevel, CTkLabel
from PIL import Image, ImageTk

from ..view import View
from .progress_frame import ProgressFrame
from .star_frame import StarFrame


if TYPE_CHECKING:
    from typing import Callable
    
    from customtkinter import CTk as Window


class ResultView(View):

    def __init__(
            self, 
            window: "Window", 
            time_percentage: float, 
            move_percentage: float, 
            main_menu_button_command: "Callable[..., None]"
        ):
        super().__init__()

        popup_window = CTkToplevel(master = window)
        popup_window.attributes('-fullscreen', True)
        popup_window.geometry("{}x{}".format(
            window.winfo_width(), 
            window.winfo_height(), 
        ))
        popup_window.wait_visibility()
        popup_window.attributes('-alpha', 0.6)
        
        frame = CTkFrame(popup_window, fg_color = "grey14")
        frame.pack(expand = True)

        StarFrame(frame, move_percentage, time_percentage).pack(pady = 50)
        ProgressFrame(frame, "Completion", 1.0).pack(pady = 20, padx = 50)
        ProgressFrame(frame, "Speed", time_percentage).pack(pady = 20, padx = 50)
        ProgressFrame(frame, "Accuracy", move_percentage).pack(pady = 20, padx = 50)
        CTkButton(frame, text = "Back to Main Menu", command = main_menu_button_command).pack(pady = 50)

        self.__popup_window = popup_window
 

    def destroy(self):
        self.__popup_window.destroy()

    def get_state(self):
        raise NotImplementedError