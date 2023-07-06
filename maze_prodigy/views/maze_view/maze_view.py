import time, random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from customtkinter import CTkFrame, CTkCanvas, CTkLabel

from ..view import View
from common import Direction, Dimensions, GridIndex, Point
from .stat_menu_frame import StatMenuFrame

if TYPE_CHECKING:
    from typing import Callable

    from customtkinter import CTk as Window

    from models import MazeCellModel
    
    

# the primary job of this class is to handle drawing to the canvas and presenting the maze to the user

class MazeView(View):
    
    def __init__(
            self, 
            window: "Window", 
            safe_area_padding: int,
            maze_dimensions: Dimensions, 
            starting_cell: "MazeCellModel", 
            ending_cell: "MazeCellModel", 
            maze_cells: list[list["MazeCellModel"]],
            target_time: int,
            target_move_count: int,
            main_menu_button_command: "Callable[..., None]",
            show_results_page: "Callable[..., None]"
        ):

        self.__window = window
        self.__starting_cell = starting_cell
        self.__ending_cell = ending_cell
        self.__maze_cells = maze_cells
        self.__show_results_page = show_results_page
        self.__visited_points_in_path: set[tuple[Point]] = set()
        self.__timer_id = None


        self.__root_frame = CTkFrame(window)

        self.__stat_menu = StatMenuFrame(self.__root_frame, main_menu_button_command, target_move_count, target_time)
        self.__stat_menu.pack(side = "left", expand = True, padx = 40)

        self.__canvas = CTkCanvas(
            master = self.__root_frame, 
            bg = window.cget("background"), 
            width = maze_dimensions.width, 
            height = maze_dimensions.height,
            highlightthickness = 0
        )
        self.__canvas.pack(side = "right", padx = 40)

        self.__root_frame.pack(padx = safe_area_padding, pady = safe_area_padding)

        self.__state = self.__MazeViewState(
            player_position = GridIndex(-1, 0),
            move_count = 0,
            time_elapsed = -1,
        )

        self.__create_maze_path()
        self.__draw_start_and_end_hint_text()
        self.__player_object = self.__create_and_bind_player_object()
        self.__update_timer_recursive()


    def destroy(self):
        self.__root_frame.destroy()
        self.__window.after_cancel(self.__timer_id)


    def get_state(self) -> 'MazeView.__MazeViewState':
        return self.__state
    

    def __get_cell_from_grid_index(self, grid_index: GridIndex) -> "MazeCellModel":
        cell: "MazeCellModel"

        if grid_index.row == -1:
            cell = self.__starting_cell
        
        elif grid_index.row == len(self.__maze_cells):
            cell = self.__ending_cell

        else:
            cell = self.__maze_cells[grid_index.row][grid_index.column]

        return cell
    

    def __update_timer_recursive(self):

        if self.__state.player_position.row != len(self.__maze_cells):
            self.__state = self.__MazeViewState(
                player_position = self.__state.player_position,
                move_count = self.__state.move_count,
                time_elapsed = self.__state.time_elapsed + 1,
            )

            self.__stat_menu.time_stat.stat_label_text = self.__state.time_elapsed
            self.__timer_id = self.__window.after(1000, self.__update_timer_recursive)












    @dataclass(frozen = True)
    class __MazeViewState():
        player_position: GridIndex
        move_count: int
        time_elapsed: int


    











    
    ################## Draw Maze ######################
    
    def __create_maze_path(self):
        starting_cell_state = self.__starting_cell.get_state()
        self.__draw_rectangle(starting_cell_state.top_left_point, starting_cell_state.bottom_right_point)
        self.__create_paths_in_cell_recursive()


    def __create_paths_in_cell_recursive(self, cell_index: GridIndex = GridIndex(-1, 0)):

        current_cell = self.__get_cell_from_grid_index(cell_index)
        current_cell_state = current_cell.get_state()
        
        if current_cell_state.has_been_visited:
            return
        
        current_cell.set_state(has_been_visited = True)

        directions = list(current_cell_state.unblocked_directions)
        random.shuffle(directions)

        for direction in directions:
            
            if direction in current_cell_state.drawn_directions:
                continue

            self.__create_path_to_next_cell(current_cell, direction)
            self.__add_direction_to_drawn_directions(current_cell, direction)

            next_cell_index_row: int
            next_cell_index_column: int
            opposite_direction: Direction

            if current_cell == self.__starting_cell:
                next_cell_index_row = 0
                next_cell_index_column = 0
                opposite_direction = Direction.UP

            else:

                next_cell_index_row = cell_index.row
                next_cell_index_column = cell_index.column
                
                if direction == Direction.UP:
                    next_cell_index_row -= 1
                    opposite_direction = Direction.DOWN
                
                elif direction == Direction.DOWN:

                    if current_cell == self.__maze_cells[len(self.__maze_cells) - 1][len(self.__maze_cells[0]) - 1]:
                        continue

                    next_cell_index_row += 1
                    opposite_direction = Direction.UP

                elif direction == Direction.LEFT:
                    next_cell_index_column -= 1
                    opposite_direction = Direction.RIGHT

                elif direction == Direction.RIGHT:
                    next_cell_index_column += 1
                    opposite_direction = Direction.LEFT

            next_cell_index = GridIndex(next_cell_index_row, next_cell_index_column)
            next_cell = self.__maze_cells[next_cell_index_row][next_cell_index_column]
            
            self.__add_direction_to_drawn_directions(next_cell, opposite_direction)
            self.__create_paths_in_cell_recursive(next_cell_index)



    def __add_direction_to_drawn_directions(self, cell: "MazeCellModel", direction: Direction):

        drawn_directions = set(cell.get_state().drawn_directions)
        drawn_directions.add(direction)

        cell.set_state(drawn_directions = frozenset(drawn_directions))



    def __create_path_to_next_cell(self, starting_cell: "MazeCellModel", direction: Direction):

        cell_state = starting_cell.get_state()

        x1 = cell_state.top_left_point.x
        y1 = cell_state.top_left_point.y
        x2 = cell_state.bottom_right_point.x
        y2 = cell_state.bottom_right_point.y

        number_of_rectangles_to_draw = 3
        is_starting_cell = False
        is_last_cell = False

        if (starting_cell == self.__starting_cell):
            number_of_rectangles_to_draw = 4
            is_starting_cell = True
        
        elif (starting_cell == self.__maze_cells[len(self.__maze_cells) - 1][len(self.__maze_cells[0]) - 1]) and (direction == Direction.DOWN):
            number_of_rectangles_to_draw = 2
            is_last_cell = True

        rectangle_dimensions: Dimensions = self.__calculate_path_rectangle_dimensions(
            is_starting_cell, 
            is_last_cell,  
            number_of_rectangles_to_draw
        )

        for _ in range(number_of_rectangles_to_draw):
            
            if direction == Direction.UP:
                y2 = y1
                y1 -= rectangle_dimensions.height
                
            elif direction == Direction.DOWN:
                y1 = y2
                y2 += rectangle_dimensions.height

            elif direction == Direction.LEFT:
                x2 = x1
                x1 -= rectangle_dimensions.width

            elif direction == Direction.RIGHT:
                x1 = x2
                x2 += rectangle_dimensions.width  
        
            self.__draw_rectangle(Point(x1, y1), Point(x2, y2))
              

    def __calculate_path_rectangle_dimensions(
            self, 
            is_starting_cell: bool, 
            is_last_cell: bool, 
            number_of_rectangles_to_draw: int
        ) -> Dimensions:

        starting_point = self.__maze_cells[0][0].get_state().bottom_right_point
        horrizontal_ending_point = self.__maze_cells[0][1].get_state().bottom_right_point
        vertial_ending_point = self.__maze_cells[1][0].get_state().bottom_right_point

        if is_starting_cell:
            vertial_ending_point = starting_point
            starting_point = self.__starting_cell.get_state().bottom_right_point

        if is_last_cell:
            starting_point = self.__maze_cells[len(self.__maze_cells) - 1][len(self.__maze_cells[0]) - 1].get_state().bottom_right_point
            vertial_ending_point = self.__ending_cell.get_state().bottom_right_point

        width = (horrizontal_ending_point.x - starting_point.x) / number_of_rectangles_to_draw
        height = (vertial_ending_point.y - starting_point.y) / number_of_rectangles_to_draw

        return Dimensions(height, width)
    

    def __animate(self):
        self.__window.update()
        self.__window.update_idletasks()


    def __draw_rectangle(self, top_left_point: Point, bottom_right_point: Point, animate: bool = False):

        self.__canvas.create_rectangle(
            top_left_point.x,
            top_left_point.y,
            bottom_right_point.x,
            bottom_right_point.y,
            fill = "#DCE4EE",
            outline = ""
        )

        if animate:
            self.__animate()


    def __draw_start_and_end_hint_text(self):

        enterance_x = self.__starting_cell.get_state().bottom_right_point.x + 10
        enterance_y = self.__maze_cells[0][0].get_state().top_left_point.y - 3

        font_size = int(enterance_y) - 7

        enterence_label = CTkLabel(self.__root_frame, text = "Enterance",  font = ("Roboto", font_size), height = 0)
        self.__canvas.create_window(enterance_x, enterance_y, anchor = "sw", window = enterence_label)

        exit_x = self.__ending_cell.get_state().top_left_point.x - 10
        exit_y = self.__maze_cells[-1][-1].get_state().bottom_right_point.y + 3

        exit_label = CTkLabel(self.__root_frame, text = "Exit",  font = ("Roboto", font_size), height = 0)
        self.__canvas.create_window(exit_x, exit_y, anchor = "ne", window = exit_label)










    ###################### Create Player Object ############################

    def __create_and_bind_player_object(self) -> int:
        cell_state = self.__starting_cell.get_state()
        cell_width = cell_state.bottom_right_point.x - cell_state.top_left_point.x
        player_object_radius = cell_width * 0.35

        player_object_center_point = self.__starting_cell.get_state().center_point
        player_object_top_left_point = player_object_center_point - player_object_radius
        player_object_bottom_right_point = player_object_center_point + player_object_radius
        player_object = self.__canvas.create_oval(
            player_object_top_left_point.x,
            player_object_top_left_point.y,
            player_object_bottom_right_point.x,
            player_object_bottom_right_point.y,
            fill = "#3B8ED0",
            outline = ""
        )

        self.__canvas.bind("<Up>", lambda event: self.__get_unblocked_neighbor_of_player_object_in_direction(Direction.UP))
        self.__canvas.bind("<Down>", lambda event: self.__get_unblocked_neighbor_of_player_object_in_direction(Direction.DOWN))
        self.__canvas.bind("<Left>", lambda event: self.__get_unblocked_neighbor_of_player_object_in_direction(Direction.LEFT))
        self.__canvas.bind("<Right>", lambda event: self.__get_unblocked_neighbor_of_player_object_in_direction(Direction.RIGHT))
        self.__canvas.focus_set()

        return player_object


    def __get_unblocked_neighbor_of_player_object_in_direction(self, direction: Direction):

        current_position = self.__state.player_position
        current_cell = self.__get_cell_from_grid_index(current_position)

        if direction in current_cell.get_state().unblocked_directions:
            new_position_row = current_position.row
            new_position_column = current_position.column

            if direction == Direction.UP:
                new_position_row -= 1
            
            elif direction == Direction.DOWN:
                new_position_row += 1

            elif direction == Direction.LEFT:
                new_position_column -= 1

            elif direction == Direction.RIGHT:
                new_position_column += 1

            new_position = GridIndex(new_position_row, new_position_column)
            self.__move_player_object_to_position(new_position)    


    def __move_player_object_to_position(self, new_position: GridIndex):

        current_position = self.__state.player_position
        current_center_point = self.__get_cell_from_grid_index(current_position).get_state().center_point
        new_center_point = self.__get_cell_from_grid_index(new_position).get_state().center_point

        distance_to_move_x = new_center_point.x - current_center_point.x
        distance_to_move_y = new_center_point.y - current_center_point.y

        self.__canvas.move(self.__player_object, distance_to_move_x, distance_to_move_y)
        self.__draw_line(current_center_point, new_center_point)

        self.__state = self.__MazeViewState(
            player_position = new_position,
            move_count = self.__state.move_count + 1,
            time_elapsed = self.__state.time_elapsed,
        )

        self.__stat_menu.move_stat.stat_label_text = self.__state.move_count
        self.__animate()

        if new_position.row == len(self.__maze_cells):
            time.sleep(1.0)
            self.__show_results_page()


    def __draw_line(self, start_point: Point, end_point: Point):
        axis_point_x = self.__adjust_line_length_on_axis(
            axis_point_1 = int(start_point.x),
            axis_point_2 = int(end_point.x)
        )
        axis_point_y = self.__adjust_line_length_on_axis(
            axis_point_1 = int(start_point.y),
            axis_point_2 = int(end_point.y)
        )
        
        start_point = Point(axis_point_x[0], axis_point_y[0])
        end_point = Point(axis_point_x[1], axis_point_y[1])
        points = (start_point, end_point)
        reversed_points = (end_point, start_point)
        color: str
        
        if (points not in self.__visited_points_in_path) and (reversed_points not in self.__visited_points_in_path):
            self.__visited_points_in_path.add(points)
            color = "#3B8ED0"
        else:
            self.__visited_points_in_path.discard(points)
            self.__visited_points_in_path.discard(reversed_points)
            color = "light grey"

        self.__canvas.create_line(
            start_point.x, 
            start_point.y, 
            end_point.x, 
            end_point.y,
            fill = color,
            width = 5
        )
        self.__canvas.tag_raise(self.__player_object)

    
    def __adjust_line_length_on_axis(self, axis_point_1: int, axis_point_2: int) -> tuple[int, int]:
        number_to_add = 3
        number_to_subtract = 2
        
        if axis_point_1 < axis_point_2:
                axis_point_1 -= number_to_subtract
                axis_point_2 += number_to_add

        elif axis_point_1 > axis_point_2:
                axis_point_1 += number_to_add
                axis_point_2 -= number_to_subtract

        return (axis_point_1, axis_point_2)
