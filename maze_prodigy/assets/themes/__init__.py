from os import path
import sys
    

def get_theme_path(file_name: str):

    if getattr(sys, 'frozen', False):
        base_path = path.join(sys._MEIPASS, "themes")
    else:
        base_path = path.abspath(path.dirname(__file__))
    return path.join(base_path, file_name)