from .. import types
import os

__all__ = [
    "ASSETS_FOLDER_PATH",
    "DIRECTORIES",
    "CWD",
    "directory",

    "Folder",
    "File"
]

ASSETS_FOLDER_PATH = "assets"
DIRECTORIES = "image/animation/music/sound/font".split('/')
CWD = os.getcwd()

directory = lambda: os.path.join(CWD, ASSETS_FOLDER_PATH)

class Folder:
    @staticmethod
    def setup() -> bool:
        if not os.path.exists(directory()):
            os.mkdir(directory())

        for folder in DIRECTORIES:
            cPath: str = directory()
            for subfolder in folder.split('\\'):
                path: str = os.path.join(cPath, subfolder)
                if os.path.exists(path): continue
                os.mkdir(path)
                cPath: str = path
        return True

    @staticmethod
    def getFolder(folder: str, awaitItem: bool = True) -> str:
        return os.path.join(directory(), folder) + ("\\" * awaitItem)

class File:
    @staticmethod
    def raw(folder: str, file: str) -> types.OPT_PATH:
        path = Folder.getFolder(folder) + file
        if not os.path.exists(path):
            from .util import error
            error("Path", path, "does not exist.")
            return None
        return path

    @staticmethod
    def image(file: str, folder: str = "images") -> types.OPT_PATH:
        return File.raw(folder, file)

    @staticmethod
    def animation(file: str, folder: str = "animations") -> types.OPT_PATH:
        return File.raw(folder, file)

    @staticmethod
    def music(file: str, folder: str = "musics") -> types.OPT_PATH:
        return File.raw(folder, file)

    @staticmethod
    def sound(file: str, folder: str = "sounds") -> types.OPT_PATH:
        return File.raw(folder, file)

    @staticmethod
    def font(file: str, folder: str = "fonts") -> types.OPT_PATH:
        return File.raw(folder, file)