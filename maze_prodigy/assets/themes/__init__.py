from os import path


def get_theme_path(file_name: str):
    
    current_path = path.abspath(path.dirname(__file__))
    return path.join(current_path, file_name)