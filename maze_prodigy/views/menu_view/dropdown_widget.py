from typing import TYPE_CHECKING

from customtkinter import CTkFrame, CTkOptionMenu, CTkLabel

if TYPE_CHECKING:
    from typing import Callable


class DropdownWidget(CTkFrame):
    def __init__(self, parent_frame: CTkFrame, label_text: str, default_value: str, values: list[str], command: 'Callable[[str], None]' = None):
        super().__init__(parent_frame)

        label = CTkLabel(
            master = self,
            text = label_text
        )
        selector = CTkOptionMenu(
            master = self,
            values = values,
            font = ("roboto", 18),
            dropdown_font = ("roboto", 16),
            command = command
        )
        selector.set(default_value)

        label.pack(pady = 15)
        selector.pack()