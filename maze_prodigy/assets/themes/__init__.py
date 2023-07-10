from os import path
import sys


def get_theme_path(file_name: str):

    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
        return path.join(bundle_dir, file_name)
    else:
        current_path = path.abspath(path.dirname(__file__))
        return path.join(current_path, file_name)