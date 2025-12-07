import ctypes
from ctypes import Structure, c_uint8, c_int, c_void_p, byref
from ctypes.util import find_library

__all__ = [
    'get_hwnd_from_window'
]

# reference url: https://wiki.libsdl.org/SDL2/SDL_GetWindowFromID

sdl = ctypes.CDLL(find_library("SDL2"))

sdl.SDL_GetWindowFromID.argtypes = [c_int]
sdl.SDL_GetWindowFromID.restype = c_void_p


# kindly ignore the naming convention for classes as of now
class SDL_version(Structure):  # noqa
    _fields_ = [("major", c_uint8), ("minor", c_uint8), ("patch", c_uint8)]


class HWND_Info(Structure):  # noqa
    _fields_ = [("window", c_void_p)]


class InfoUnion(ctypes.Union):
    _fields_ = [("win", HWND_Info), ("pad", ctypes.c_char * 512)]


class SDL_SysWMinfo(Structure):  # noqa
    _fields_ = [
        ("version", SDL_version),
        ("subsystem", c_int),
        ("info", InfoUnion)
    ]


sdl.SDL_GetWindowWMInfo.argtypes = [c_void_p, ctypes.POINTER(SDL_SysWMinfo)]
sdl.SDL_GetWindowWMInfo.restype = c_int


def get_hwnd_from_window(window):
    sdl_window = sdl.SDL_GetWindowFromID(window.id)
    if not sdl_window:
        return None
    wm_info = SDL_SysWMinfo()
    wm_info.version = SDL_version(2, 0, 0)
    if sdl.SDL_GetWindowWMInfo(sdl_window, byref(wm_info)):
        return wm_info.info.win.window
    return None