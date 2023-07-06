from typing import TYPE_CHECKING

from .controller import Controller
from .maze_controller import MazeController
from views import MenuView

if TYPE_CHECKING:
    from app import App


class MenuController(Controller):

    def __init__(self, app:"App") -> None:
        super().__init__()
        
        self.__app = app
        self.__view = MenuView(
            window = app.window, 
            start_button_command = self.__initialize_maze_controller,
            quit_button_command = self.__quit_game

        )


    def destroy():
        raise NotImplementedError


    def hide_view(self, is_hidden: bool):
        self.__view.set_state(is_hidden = is_hidden)


    def __initialize_maze_controller(self):
        self.hide_view(True)
        selected_difficulty = self.__view.get_state().selected_difficulty
        maze_controller = MazeController(self.__app, selected_difficulty)
        self.__app.set_controller(maze_controller)

    
    def __quit_game(self):
        self.__app.close_window()

        