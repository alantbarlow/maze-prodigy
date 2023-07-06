from dataclasses import dataclass
from typing import TYPE_CHECKING
import random

from ..model import Model
from .maze_cell_grid_model import MazeCellGridModel
from common import Direction, Dimensions, GridIndex, GridSize

if TYPE_CHECKING:
    from .maze_cell_model import MazeCellModel
    

class MazeModel(Model):
    
    __BORDER_PERCENTAGE_OF_MAZE_CELL = 1.00
    __PADDING_PERCENTAGE_OF_MAZE_CELL = 0.75
    __MARGIN_PERCENTAGE_OF_MAZE_CELL = 0.25
    
    def __init__(self, maze_dimensions:Dimensions, difficulty:str):
        
        self.__maze_dimensions = maze_dimensions
        self.__grid_size = self.__set_grid_size(difficulty)
        self.__cell_dimensions = self.__calculate_cell_dimensions()
        self.__maze_padding = self.__cell_dimensions.width * self.__PADDING_PERCENTAGE_OF_MAZE_CELL
        self.__cell_margin = self.__cell_dimensions.width * self.__MARGIN_PERCENTAGE_OF_MAZE_CELL

        maze_cell_grid_model_state = MazeCellGridModel(
            maze_dimensions = self.__maze_dimensions,
            cell_dimensions = self.__cell_dimensions,
            grid_size = self.__grid_size,
            maze_padding = self.__maze_padding,
            cell_margin = self.__cell_margin                            
        ).get_state()
        
        self.__state = self.__MazeModelState(
            maze_cells = maze_cell_grid_model_state.cell_grid,
            starting_cell = maze_cell_grid_model_state.starting_cell,
            ending_cell = maze_cell_grid_model_state.ending_cell,
            number_of_moves_to_solve = None
        )
        
        self.__update_state_of_maze_cells()
        

    def get_state(self) -> "MazeModel.__MazeModelState":
        return self.__state

    
    def __set_grid_size(self, difficulty:str) -> GridSize:
        if difficulty == "Easy":
            return GridSize(20, 20)
        elif difficulty == "Medium":
            return GridSize(30, 30)
        elif difficulty == "Hard":
            return GridSize(40, 40)
        else:
            raise ValueError(f"The difficulty must be either set to 'Easy', 'Medium', or 'Hard' not {difficulty}")
        

    def __calculate_cell_dimensions(self) -> Dimensions:
        border_path_spaces = self.__BORDER_PERCENTAGE_OF_MAZE_CELL * 2
        padding_spaces = self.__PADDING_PERCENTAGE_OF_MAZE_CELL * 2
        margin_spaces = self.__grid_size.columns * (self.__MARGIN_PERCENTAGE_OF_MAZE_CELL * 2)
        
        total_number_of_horrizontal_spaces = border_path_spaces + padding_spaces + margin_spaces + self.__grid_size.columns
        total_number_of_vertical_spaces = border_path_spaces + padding_spaces + margin_spaces + self.__grid_size.rows

        return Dimensions(
            height = self.__maze_dimensions.height / total_number_of_vertical_spaces,
            width = self.__maze_dimensions.width / total_number_of_horrizontal_spaces
        )


    def __unblock_direction_in_cell(self, cell:"MazeCellModel", direction_to_unblock:Direction):
        unblocked_directions = set(cell.get_state().unblocked_directions)
        unblocked_directions.add(direction_to_unblock)

        cell.set_state(
            unblocked_directions = frozenset(unblocked_directions)
        )


    def __unblock_maze_enterence(self):
        self.__unblock_direction_in_cell(self.__state.starting_cell, Direction.DOWN)
        self.__unblock_direction_in_cell(self.__state.maze_cells[0][0], Direction.UP)
        

    def __unblock_maze_exit(self):
        self.__unblock_direction_in_cell(self.__state.ending_cell, Direction.UP)
        self.__unblock_direction_in_cell(self.__state.maze_cells[self.__grid_size.rows - 1][self.__grid_size.columns - 1], Direction.DOWN)
    

    def __pick_random_unvisited_neighbor_at_cell_index(self, cell_index: GridIndex) -> GridIndex:

        neighbors: list[GridIndex] = []

        if cell_index.row != 0:
            neighbors.append(GridIndex(cell_index.row - 1, cell_index.column))

        if cell_index.row != (self.__grid_size.rows - 1):
            neighbors.append(GridIndex(cell_index.row + 1, cell_index.column))

        if cell_index.column != 0:
            neighbors.append(GridIndex(cell_index.row, cell_index.column - 1))

        if cell_index.column != (self.__grid_size.columns - 1):
            neighbors.append(GridIndex(cell_index.row, cell_index.column + 1))

        unvisited_neighbors = [
            neighbor for neighbor in neighbors \
            if not self.__state.maze_cells[neighbor.row][neighbor.column].get_state().has_been_visited
        ]

        if unvisited_neighbors:
            return random.choice(unvisited_neighbors)
        else:
            return None


    """ def __unblock_maze_path_at_index_recursive(self, cell_index: GridIndex = GridIndex(0, 0)):
        
        self.__state.maze_cells[cell_index.row][cell_index.column].set_state(
            has_been_visited = True
        )

        if cell_index == GridIndex(self.__grid_size.rows - 1, self.__grid_size.columns - 1):
            return

        while True:
            neighbor_to_visit = self.__pick_random_unvisited_neighbor_at_cell_index(cell_index)

            if neighbor_to_visit is None:
                break

            current_cell = self.__state.maze_cells[cell_index.row][cell_index.column]
            neighbors_cell = self.__state.maze_cells[neighbor_to_visit.row][neighbor_to_visit.column]

            if neighbor_to_visit.row < cell_index.row:
                self.__unblock_direction_in_cell(current_cell, Direction.UP)
                self.__unblock_direction_in_cell(neighbors_cell, Direction.DOWN)

            elif neighbor_to_visit.row > cell_index.row:
                self.__unblock_direction_in_cell(current_cell, Direction.DOWN)
                self.__unblock_direction_in_cell(neighbors_cell, Direction.UP)

            elif neighbor_to_visit.column < cell_index.column:
                self.__unblock_direction_in_cell(current_cell, Direction.LEFT)
                self.__unblock_direction_in_cell(neighbors_cell, Direction.RIGHT)

            elif neighbor_to_visit.column > cell_index.column:
                self.__unblock_direction_in_cell(current_cell, Direction.RIGHT)
                self.__unblock_direction_in_cell(neighbors_cell, Direction.LEFT)

            self.__unblock_maze_path_at_index_recursive(neighbor_to_visit)"""


    def __unblock_maze_path(self):
        index_stack = self.__traverse_maze(is_initial_traversal = True) 
        random.shuffle(index_stack)

        self.__state = self.__MazeModelState(
            maze_cells = self.__state.maze_cells,
            starting_cell = self.__state.starting_cell,
            ending_cell = self.__state.ending_cell,
            number_of_moves_to_solve = len(index_stack) + 2
        )

        self.__traverse_maze(index_stack)

       

    def __traverse_maze(self, index_stack: list[GridIndex] = None, is_initial_traversal: bool = False) -> list[GridIndex]:
        
        if index_stack is None:
            index_stack = [GridIndex(0, 0)]

        while index_stack:

            current_index = index_stack[-1]
            current_cell = self.__state.maze_cells[current_index.row][current_index.column]

            current_cell.set_state(
                has_been_visited = True
            )

            if (current_cell == self.__state.maze_cells[-1][-1]) and (is_initial_traversal):
                index_stack.pop()
                break

            neighbor_to_visit = self.__pick_random_unvisited_neighbor_at_cell_index(current_index)

            if neighbor_to_visit is None:
                index_stack.pop()
                continue
            
            neighbors_cell = self.__state.maze_cells[neighbor_to_visit.row][neighbor_to_visit.column]

            if neighbor_to_visit.row < current_index.row:
                self.__unblock_direction_in_cell(current_cell, Direction.UP)
                self.__unblock_direction_in_cell(neighbors_cell, Direction.DOWN)

            elif neighbor_to_visit.row > current_index.row:
                self.__unblock_direction_in_cell(current_cell, Direction.DOWN)
                self.__unblock_direction_in_cell(neighbors_cell, Direction.UP)

            elif neighbor_to_visit.column < current_index.column:
                self.__unblock_direction_in_cell(current_cell, Direction.LEFT)
                self.__unblock_direction_in_cell(neighbors_cell, Direction.RIGHT)

            elif neighbor_to_visit.column > current_index.column:
                self.__unblock_direction_in_cell(current_cell, Direction.RIGHT)
                self.__unblock_direction_in_cell(neighbors_cell, Direction.LEFT)

            index_stack.append(neighbor_to_visit)

        return index_stack
    

    def __reset_visited_state_of_each_cell(self):
         for row in self.__state.maze_cells:
            for cell in row:
                cell.set_state(has_been_visited = False)


    def __update_state_of_maze_cells(self):
        self.__unblock_maze_enterence()
        self.__unblock_maze_exit()
        #self.__unblock_maze_path_at_index_recursive()
        self.__unblock_maze_path()
        self.__reset_visited_state_of_each_cell()


    @dataclass(frozen = True)
    class __MazeModelState():
        maze_cells: list[list["MazeCellModel"]]
        starting_cell: "MazeCellModel"
        ending_cell: "MazeCellModel"
        number_of_moves_to_solve: int
