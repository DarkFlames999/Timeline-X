try:
    import rich.traceback
    rich.traceback.install()
except ImportError:
    print("rich module (pip install rich) was not installed and is not necessary, but is suggested")

try:
    import pygame

    if not hasattr(pygame, "FRect"):
        raise ImportError("Requires Pygame-CE from (pip install pygame-ce) - Got (pip install pygame).")
except ImportError:
    raise ImportError("Engine requires pygame-ce to run (pip install pygame-ce).")

try:
    import win32gui
    import win32con
    import win32api
except ImportError:
    raise ImportError("Engine requires pywin32 to run (pip install pywin32).")

try:
    import colorama
except ImportError:
    raise ImportError("Engine requires colorama (pip install colorama).")

try:
    import xml
except ImportError:
    raise ImportError("Engine requires XML for Adobe Animate Animations (pip install xml-python).")

# Assuming XML was successful
try:
    import lxml
except ImportError:
    raise ImportError("Engine ALSO (since you already have xml) requires LXML for Adobe Animate Animations (pip install lxml).")

try:
    import json
except ImportError:
    raise ImportError("Engine requires json for ASEPRITE Animations (..Since there's no pip installation for it.. i think you're kinda screwed not gonna lie -Irshaad).")

try:
    import multipledispatch
except ImportError:
    raise ImportError("Engine requires multipledispatch (pip install multipledispatch).")

try:
    import pytweening
except ImportError:
    raise ImportError("Engine requires pytweening (pip install pytweening).")

# Sets modified pygame classes
from . import pygame_mod


from .main import *
from .sprite import *
from .timer import *
from .tween import *
from .utils import *
from .text import *
from . import types