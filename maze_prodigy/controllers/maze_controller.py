from typing import TYPE_CHECKING

from .controller import Controller
from .result_controller import ResultController
from common import Dimensions
from models import MazeModel
from views import MazeView


if TYPE_CHECKING:
    from app import App



class MazeController(Controller):

    def __init__(self, app: "App", difficulty: str):
        super().__init__()

        self.__app = app
        maze_dimensions = self.__calculate_maze_dimensions(app)

        self.__model = MazeModel(maze_dimensions, difficulty)
        self.__model_state = self.__model.get_state()

        self.__target_move_count = self.__model_state.number_of_moves_to_solve

        self.__target_time = round(self.__target_move_count * 0.35)

        self.__view = MazeView(
            window = app.window,
            safe_area_padding = self.__app.get_state().safe_area_padding,
            maze_dimensions = maze_dimensions, 
            starting_cell = self.__model_state.starting_cell,
            ending_cell = self.__model_state.ending_cell,
            maze_cells = self.__model_state.maze_cells,
            target_time = self.__target_time,
            target_move_count = self.__target_move_count,
            main_menu_button_command = self.__app.go_back_to_main_menu,
            show_results_page = self.__initialize_results_controller
        )

    
    def destroy(self):
        self.__view.destroy()
        del self
        

    def __calculate_maze_dimensions(self, app: "App") -> Dimensions:
        app_state = app.get_state()
        drawable_length = app_state.window_dimensions.height - (app_state.safe_area_padding * 2)
        return Dimensions(
            height = drawable_length,
            width = drawable_length
        )
    
    def __initialize_results_controller(self):
        view_state = self.__view.get_state()
        result_controller = ResultController(
            app = self.__app, 
            target_time = self.__target_time,
            completed_time = view_state.time_elapsed,
            target_moves = self.__target_move_count,
            completed_moves = view_state.move_count
        )
        self.__app.set_controller(result_controller)