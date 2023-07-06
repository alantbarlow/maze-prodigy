from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..model import Model
from common import Point

if TYPE_CHECKING:
    from common import Direction


class MazeCellModel(Model):

    def __init__(self, top_left_point:Point, bottom_right_point:Point):

        self.__state = self.__MazeCellModelState(
            top_left_point = top_left_point,
            bottom_right_point = bottom_right_point,
            center_point = (top_left_point + bottom_right_point) / 2
        )


    def get_state(self) -> "MazeCellModel.__MazeCellModelState":
        return self.__state
    
    
    def set_state(
            self, 
            has_been_visited: bool | None = None, 
            unblocked_directions: frozenset["Direction"] | None = None, 
            drawn_directions: frozenset["Direction"] | None = None
        ):
        new_has_been_visited = has_been_visited if has_been_visited is not None else self.__state.has_been_visited
        new_unblocked_directions = unblocked_directions if unblocked_directions is not None else self.__state.unblocked_directions
        new_drawn_directions = drawn_directions if drawn_directions is not None else self.__state.drawn_directions
    
        self.__state = self.__MazeCellModelState(
            top_left_point = self.__state.top_left_point,
            bottom_right_point = self.__state.bottom_right_point,
            center_point = self.__state.center_point,
            has_been_visited = new_has_been_visited,
            unblocked_directions = new_unblocked_directions,
            drawn_directions = new_drawn_directions
        )

    
    @dataclass(frozen = True)
    class __MazeCellModelState():
        top_left_point: Point
        bottom_right_point: Point
        center_point: Point
    
        has_been_visited: bool = False
        unblocked_directions: frozenset["Direction"] = frozenset()
        drawn_directions: frozenset["Direction"] = frozenset()