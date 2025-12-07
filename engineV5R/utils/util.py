from .. import types
from colorama import init, Fore
from typing import Any, _SpecialForm, get_args
import sys
import os
import pygame

init(autoreset=False)

__all__ = [
    "isRunningDebugger",
    "getStack",
    "getTimeFormat",
    "getBasename",
    "sendFore",
    "debug",
    "warn",
    "error",
    "xml",
    "json",
    "pathExists",
    "exists",
    "existsOr",
    "existThenCall",
    "valueInLiteral",
    "transformSurface",
]

def isRunningDebugger() -> bool:
    """Return if the debugger is currently active"""
    if 'pdb' in sys.modules:
        return True
    elif 'IPython' in sys.modules:
        return True
    elif 'pydevd' in sys.modules:
        return True
    elif 'ptvsd' in sys.modules:
        return True
    elif 'PYDEVD_LOAD_VALUES_ASYNC' in os.environ:
        return True
    return False

def getStack() -> list:
    """Returns the Stack of the program"""
    import inspect
    return inspect.stack()

def getTimeFormat() -> str:
    """Returns the Time Format of Hours:Minutes:Seconds"""
    import datetime
    return datetime.datetime.now().strftime("%H:%M:%S")

def getBasename(path: str) -> str:
    """Returns the BaseName of the path"""
    return os.path.basename(path)

def sendFore(foreType: str, prefix: str, *args: any, sep: str=' ', end: str='\n') -> None:
    print(foreType + prefix + sep.join(map(str, args)) + Fore.RESET, end=end)

def debug(*args) -> None:
    """Prints debug messages"""
    if not isRunningDebugger(): return
    sendFore(Fore.LIGHTGREEN_EX, f"[ USER DEBUG ] {getBasename(getStack()[2].filename)} {getTimeFormat()} - ", *args)

def warn(*args) -> None:
    """Prints warning messages"""
    sendFore(Fore.LIGHTYELLOW_EX, f"[ USER WARN ] {getBasename(getStack()[2].filename)} {getTimeFormat()} - ", *args)

def error(*args) -> None:
    """Prints error messages"""
    sendFore(Fore.LIGHTRED_EX, f"[ USER ERROR ] {getBasename(getStack()[2].filename)} {getTimeFormat()} - ", *args)

def transformSurface(surf: pygame.Surface, size: pygame.typing.Point, angle: float=0, flipX: bool=False, flipY: bool=False) -> pygame.Surface:
    return pygame.transform.flip(pygame.transform.rotate(pygame.transform.scale(surf, size), angle), flipX, flipY)

from xml.etree.ElementTree import Element
def xml(path: str) -> Element:
    """Basic Loading of XML Files"""
    from xml.etree.ElementTree import parse
    from lxml.etree import XMLParser

    return parse(path, XMLParser(recover=True)).getroot()

def json(path: str) -> dict:
    """Basic Loading of JSON Files"""
    from json import load
    with open(path, 'r') as f:
        data = f
        f.close()
    return load(data)

def pathExists(path: str) -> bool:
    """Checks if Path Exists"""
    return os.path.exists(path)

def exists(__obj: object) -> bool:
    """Check if Object is not None"""
    return __obj is not None

def existsOr[_T](__obj: object, default: _T) -> _T:
    return __obj if exists(__obj) else default

def existThenCall(__obj: types.OPT_CALL) -> Any:
    if not exists(__obj): return None
    return __obj()

def valueInLiteral(arg: Any, literal: _SpecialForm) -> bool:
    return arg in get_args(literal)

