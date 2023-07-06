from customtkinter import CTkFrame

from .star import Star


class StarFrame(CTkFrame):
    def __init__(self, master: CTkFrame, move_percentage: float, time_percentage: float):
        super().__init__(master)

        percentage_list = [1.0, move_percentage, time_percentage]
        percentage_list.sort(reverse = True)

        for percentage in percentage_list:
            Star(self, percentage == 1.0).pack(side = "left", padx = 20)
