from dataclasses import dataclass
from typing import TYPE_CHECKING

from customtkinter import CTkFrame, CTkButton, CTkProgressBar

from views.result_view.custom_progress_bar import CustomProgressBar

from ..view import View
from .dropdown_widget import DropdownWidget
from .title_widget import TitleWidget

if TYPE_CHECKING:
    from typing import Callable
    
    from customtkinter import CTk as Window


class MenuView(View):

    __DEFAULT_DIFFICULTY = "Medium"

    def __init__(self, window:"Window", start_button_command: 'Callable[..., None]', quit_button_command: 'Callable[..., None]'):

        self.__window = window
        self.__start_button_command = start_button_command
        self.__quit_button_command = quit_button_command

        self.__root_frame = CTkFrame(window)
        self.__root_frame.pack(expand = True)

        self.__configure_root_frame()

        self.__state = self.__MenuViewState(
            selected_difficulty = self.__DEFAULT_DIFFICULTY,
            is_hidden = False
        )

        
    def get_state(self) -> 'MenuView.__MenuViewState':
        return self.__state
    

    def set_state(self, is_hidden: bool):
        self.__state = self.__MenuViewState(
            selected_difficulty = self.__state.selected_difficulty,
            is_hidden = is_hidden
        )
        
        if is_hidden: 
            self.__root_frame.pack_forget()
        else:
            self.__root_frame.pack(expand = True)


    def __handle_difficulty_change(self, difficulty: str):
        self.__state = self.__MenuViewState(
            selected_difficulty = difficulty,
            is_hidden = self.__state.is_hidden
        )

    
    def __configure_root_frame(self):

        TitleWidget(
            parent_frame = self.__root_frame,
            title = self.__window.title(),
            subtitle = "A simple maze simulator"
        ).pack()

        DropdownWidget(
            parent_frame= self.__root_frame,
            label_text = "Select Difficulty:",
            default_value = "Medium",
            values = ["Easy", "Medium", "Hard"],
            command = self.__handle_difficulty_change
        ).pack(pady = 100)
        
        CTkButton(
            master = self.__root_frame,
            text = "New Game",
            command = self.__start_button_command
        ).pack(pady = 10)
        
        CTkButton(
            master = self.__root_frame,
            text = "Quit",
            command = self.__quit_button_command
        ).pack(pady = 10)

        

    @dataclass(frozen = True)
    class __MenuViewState():
        selected_difficulty: str
        is_hidden: bool