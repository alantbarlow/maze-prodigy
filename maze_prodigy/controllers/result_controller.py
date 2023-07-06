from typing import TYPE_CHECKING

from controllers import Controller
from views import ResultView

if TYPE_CHECKING:
    from app import App


class ResultController(Controller):
    
    def __init__(self, app: "App", target_time: int, completed_time: int, target_moves: int, completed_moves: int) -> None:
        super().__init__()

        time_percentage = min(1.0, max(0.0, 1 - ((completed_time - target_time) / target_time)))
        move_percentage = min(1.0, max(0.0, 1 - ((completed_moves - target_moves) / target_moves)))

        self.__view = ResultView(app.window, time_percentage, move_percentage, app.go_back_to_main_menu)

    def destroy(self):
        self.__view.destroy()
        del self
    