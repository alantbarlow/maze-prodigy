from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..model import Model
from .maze_cell_model import MazeCellModel
from common import Point

if TYPE_CHECKING:
    from common import Dimensions, GridSize


# The primary job of this class is to manage the list of cells

class MazeCellGridModel(Model):

    def __init__(
            self, 
            maze_dimensions: "Dimensions",
            cell_dimensions: "Dimensions",
            grid_size: "GridSize",
            maze_padding: int,
            cell_margin: int
        ):
        
        self.__maze_dimensions = maze_dimensions
        self.__maze_padding = maze_padding
        self.__cell_margin = cell_margin
        self.__cell_height = cell_dimensions.height
        self.__cell_width = cell_dimensions.width

        self.__state = self.__MazeCellGridModelState(
            cell_grid = self.__create_cell_grid(grid_size.rows, grid_size.columns),
            starting_cell = self.__create_starting_cell(),
            ending_cell = self.__create_ending_cell()
        )

    def get_state(self) -> "MazeCellGridModel.__MazeCellGridModelState":
        return self.__state
    

    def __create_cell_grid(self, number_of_rows:int, number_of_columns:int) -> list[list[MazeCellModel]]:

        cell_grid: list[list[MazeCellModel]] = []
        
        # add maze cells based on number or rows and columns
        for row_index in range(number_of_rows):
            cell_grid.append([])
            for column_index in range(number_of_columns):
                cell_grid[row_index].append(None)
                cell_grid = self.__add_cell_to_grid_at_index(row_index, column_index, cell_grid)

        return cell_grid


    def __add_cell_to_grid_at_index(self, row_index:int, column_index:int, cell_grid:list[list[MazeCellModel]]) -> list[list[MazeCellModel]]:
        
        if cell_grid[row_index][column_index] == None:
        
            if column_index == 0:
                top_left_x = self.__cell_width + self.__maze_padding + self.__cell_margin
            else:
                previous_cell_in_column_state = cell_grid[row_index][column_index - 1].get_state()
                top_left_x = previous_cell_in_column_state.bottom_right_point.x + (self.__cell_margin * 2)
            
            if row_index == 0:
                top_left_y = self.__cell_height + self.__maze_padding + self.__cell_margin
            else:
                previous_cell_in_row_state = cell_grid[row_index - 1][column_index].get_state()
                top_left_y = previous_cell_in_row_state.bottom_right_point.y + (self.__cell_margin * 2)

            top_left_point = Point(
                x = top_left_x,
                y = top_left_y
            )
            bottom_right_point = Point(
                x = top_left_x + self.__cell_width,
                y = top_left_y + self.__cell_height
            ) 
            
            cell = MazeCellModel(top_left_point, bottom_right_point)
            cell_grid[row_index][column_index] = cell
            return cell_grid


    def __create_starting_cell(self) -> MazeCellModel:

        top_left_point_x = self.__maze_padding + self.__cell_margin + self.__cell_width

        top_left_point = Point(
            x = top_left_point_x,
            y = 0
        )
        bottom_right_point = Point(
            x = top_left_point_x + self.__cell_width,
            y = self.__cell_height
        )
        return MazeCellModel(top_left_point, bottom_right_point)


    def __create_ending_cell(self) -> MazeCellModel:

        bottom_right_point_x = self.__maze_dimensions.width - self.__cell_width - self.__maze_padding - self.__cell_margin

        top_left_point = Point(
            x = bottom_right_point_x - self.__cell_width,
            y = self.__maze_dimensions.height - self.__cell_height
        )
        bottom_right_point = Point(
            x = bottom_right_point_x,
            y = self.__maze_dimensions.height
        )
        return MazeCellModel(top_left_point, bottom_right_point)
    

    @dataclass(frozen = True)
    class __MazeCellGridModelState():
        cell_grid: list[list[MazeCellModel]]
        starting_cell: MazeCellModel
        ending_cell: MazeCellModel