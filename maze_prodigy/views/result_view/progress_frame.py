from customtkinter import CTkFrame, CTkLabel

from .custom_progress_bar import CustomProgressBar


class ProgressFrame(CTkFrame):
    def __init__(self, master: CTkFrame, title: str, progress_percentage: float):
        super().__init__(master)

        CTkLabel(self, text = title).pack(anchor = "w")
        CustomProgressBar(self, progress_percentage).pack(pady = 10)