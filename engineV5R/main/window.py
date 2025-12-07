from ..utils.util import debug
from .temp_hwnd import get_hwnd_from_window
from typing import Self
import win32gui, win32con, win32api
import pygame

__all__ = [
    'Window'
]

class Window(pygame.Window):
    __Instances: list[Self] = []

    @classmethod
    def getInstances(cls) -> list[Self]:
        return cls.__Instances

    def __new__(cls, title: str = "pygame window",
             size: pygame.typing.SequenceLike[float] = (640, 480),
             position: int | pygame.typing.SequenceLike[float] = pygame.WINDOWPOS_UNDEFINED,
             *,
             fullscreen: bool = None,
             fullscreen_desktop: bool = None,
             opengl: bool = None,
             vulkan: bool = None,
             hidden: bool = None,
             borderless: bool = None,
             resizable: bool = None,
             minimized: bool = None,
             maximized: bool = None,
             mouse_grabbed: bool = None,
             keyboard_grabbed: bool = None,
             input_focus: bool = None,
             mouse_focus: bool = None,
             allow_high_dpi: bool = None,
             mouse_capture: bool = None,
             always_on_top: bool = None,
             utility: bool = None) -> Self:

        debug("Initializing Window as __new__")
        instance = super().__new__(cls)
        cls.__Instances.append(instance)
        debug(f"Initialized as Window{cls.__Instances.index(instance)+1}")
        return instance

    def __init__(self, title: str = "pygame window",
             size: pygame.typing.SequenceLike[float] = (640, 480),
             position: int | pygame.typing.SequenceLike[float] = pygame.WINDOWPOS_UNDEFINED,
             *,
             fullscreen: bool = None,
             fullscreen_desktop: bool = None,
             opengl: bool = None,
             vulkan: bool = None,
             hidden: bool = None,
             borderless: bool = None,
             resizable: bool = None,
             minimized: bool = None,
             maximized: bool = None,
             mouse_grabbed: bool = None,
             keyboard_grabbed: bool = None,
             input_focus: bool = None,
             mouse_focus: bool = None,
             allow_high_dpi: bool = None,
             mouse_capture: bool = None,
             always_on_top: bool = None,
             utility: bool = None) -> None:

        super().__init__(title, size, position, fullscreen=fullscreen, fullscreen_desktop=fullscreen_desktop, opengl=opengl, vulkan=vulkan, hidden=hidden, borderless=borderless, resizable=resizable, minimized=minimized, maximized=maximized, mouse_grabbed=mouse_grabbed, keyboard_grabbed=keyboard_grabbed, input_focus=input_focus, mouse_focus=mouse_focus, allow_high_dpi=allow_high_dpi, mouse_capture=mouse_capture, always_on_top=always_on_top, utility=utility)
        debug("Initializing Class as __init__")
        debug("Attempting to Get HWND of Window")
        self.__hwnd = get_hwnd_from_window(self)
        debug("HWND of Window", self.id, "is:", self.__hwnd)
        self.__ogStyle: None = win32gui.GetWindowLong(self.__hwnd, win32con.GWL_EXSTYLE)
        self.__invisible: bool = False
        self.__fullscreen: bool = False

        from ..types import FUNCTION
        self.onClose: FUNCTION | None = None

        from ..sprite.group import Group
        self.__Sprites = Group()

        from .camera import Camera
        self.__Cameras: list[Camera] = []
        self.__MainCamera: Camera = self.createCamera(0, 0, *self.size)

        debug("Initialized Convert Format")
        self.get_surface()

    def update(self):
        self.__MainCamera.size = self.size

    def draw(self):
        self.Sprites.update()
        self.Sprites.draw(self.screen)

    def createCamera(self, x, y, w, h):
        from .camera import Camera
        c = Camera(self.id, x, y, w, h)
        self.__Cameras.append(c)
        return c

    def removeCamera(self, cam):
        if cam in self.__Cameras:
            self.__Cameras.remove(cam)

    def addCamera(self, cam):
        if cam in self.__Cameras:
            self.__Cameras.append(cam)

    def destroy(self):
        self.__Instances.remove(self)
        self.__Cameras.clear()
        self.__Sprites.empty()
        super().destroy()

    @property
    def fullscreen(self) -> bool:
        return self.__fullscreen

    @fullscreen.setter
    def fullscreen(self, value: bool):
        if value == self.__fullscreen: return
        self.__fullscreen = value

        if value:
            self.set_fullscreen(True)
        else:
            self.set_windowed()

    @property
    def invisible(self) -> bool:
        return self.__invisible

    @invisible.setter
    def invisible(self, value: bool):
        if value == self.__invisible: return
        self.__invisible = value

        if value:
            self.borderless = True
            win32gui.SetWindowLong(self.__hwnd, win32con.GWL_EXSTYLE, self.__ogStyle | win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST)
            win32gui.SetLayeredWindowAttributes(self.__hwnd, 0, 255, win32con.LWA_COLORKEY)
            debug("Set Window to Invisible")
        else:
            self.borderless = False
            win32gui.SetLayeredWindowAttributes(self.__hwnd, win32api.RGB(255, 255, 255), 255, win32con.LWA_COLORKEY)
            win32gui.SetWindowLong(self.__hwnd, win32con.GWL_EXSTYLE, self.__ogStyle)
            debug("Set Window to Normal")

    @property
    def screen(self) -> pygame.Surface:
        return self.get_surface()

    @property
    def Sprites(self):
        return self.__Sprites

    @property
    def Cameras(self):
        return self.__Cameras

    @property
    def MainCamera(self):
        return self.__MainCamera