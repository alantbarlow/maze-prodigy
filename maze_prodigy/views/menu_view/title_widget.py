from customtkinter import CTkFrame, CTkLabel



class TitleWidget(CTkFrame):
    def __init__(self, parent_frame: CTkFrame, title: str, subtitle: str):
        super().__init__(parent_frame)
        
        CTkLabel(
            master = self,
            text = title,
            font = ("roboto", 50),
        ).pack(pady = 10)
        
        CTkLabel(
            master = self,
            text = subtitle,
        ).pack()
        