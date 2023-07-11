from os import path
import sys
    

def get_theme_path(file_name: str):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(path.dirname(__file__))
    return path.join(base_path, file_name)