from customtkinter import CTkFrame, CTkLabel


class StatWidget(CTkFrame):
    def __init__(self, parent_frame: CTkFrame, stat_title: str, stat: int, stat_target: int, stat_discriptor: str):
        super().__init__(parent_frame)

        CTkLabel(self, text = stat_title, font=("roboto", 24)).pack(pady = 10)

        self.__secondary_frame = CTkFrame(self)

        self.__stat_label = CTkLabel(self.__secondary_frame, text = str(stat), font=("roboto", 50))
        self.__stat_label.pack(side = "left")
        
        CTkLabel(self.__secondary_frame, text = f" / {stat_target}").pack(side = "left")

        self.__secondary_frame.pack()

        CTkLabel(self, text = stat_discriptor).pack()
        
        
    @property
    def stat_label_text(self) -> str:
        return self.__stat_label.cget("text")
    
    @stat_label_text.setter
    def stat_label_text(self, new_text):
        self.__stat_label.configure(text = new_text)