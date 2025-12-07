from __future__ import annotations
from typing import Callable
import pygame

__all__ = [
    'Engine',
    'Base'
]

class Engine:
    __Instance: Engine = None
    __id: int = None

    def __new__(cls, fps: int = 60) -> Engine:
        from ..utils.util import debug, exists, warn
        if not exists(cls.__Instance):
            debug("Creating Engine __new__")
            cls.__Instance = super().__new__(cls)
            cls.__id = id(cls.__Instance)
            debug("Set Engine ID to", cls.__id)
            return cls.__Instance
        warn("Engine already initialized")
        return cls.__Instance

    @classmethod
    def getEngine(cls) -> Engine:
        from ..utils.util import exists
        if not exists(cls.__Instance):
            return cls.__new__(cls)
        return cls.__Instance

    def __init__(self, fps: int = 60) -> None:
        import time
        a = time.time()
        from ..utils.util import debug
        debug("Initializing Engine from __init__ with id:", self.__id)
        debug("Initializing Pygame")

        self.Init: tuple[int, int] = pygame.init()

        debug(f"Pygame Initialized With {self.Init[0]} Initializations Passed & {self.Init[1]} Initializations Failed")

        self.Active: bool = True

        debug("Engine Set To Active")
        debug("Initializing Engine Imports")

        # Imports
        from .window import Window
        from .state import States
        from .runtime import Runtime
        from .event import EventHandler
        from .handlers import TimerHandler, SequenceHandler, TweenHandler

        debug("Made Lazy Imports")

        self.__Events: EventHandler = EventHandler()
        self.__States: States = States()
        self.__Runtime: Runtime = Runtime(fps)

        self.__TimerHandler: TimerHandler = TimerHandler()
        self.__SequenceHandler: SequenceHandler = SequenceHandler()
        self.__TweenHandler: TweenHandler = TweenHandler()

        self.__Window: Window = Window()

        def closeMain():
            self.Active = False

        self.__Window.onClose = closeMain

        debug("Initialized Engine Imports")
        debug("Initialized Engine In", time.time() - a, "seconds")

    def updateFirst(self):
        for win in self.WindowInstances:
            win.screen.fill((0, 0, 0))
            win.update()

    def updateClass(self):
        self.Events()
        self.TimerHandler()
        self.SequenceHandler()
        self.TimerHandler()

    def update(self):
        self.updateFirst()

        self.updateClass()

        self.States()

        self.draw()

        self.updateLast()

    def draw(self):
        for win in self.WindowInstances:
            win.draw()

    def updateLast(self):
        self.Runtime.tick()
        for win in self.WindowInstances:
            win.flip()

    def run(self):
        while self.Active:
            self.update()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def Events(self):
        return self.__Events

    @property
    def States(self):
        return self.__States

    @property
    def Runtime(self):
        return self.__Runtime

    @property
    def TimerHandler(self):
        return self.__TimerHandler

    @property
    def SequenceHandler(self):
        return self.__SequenceHandler

    @property
    def TweenHandler(self):
        return self.__TweenHandler

    @property
    def Window(self):
        return self.__Window

    @property
    def Screen(self) -> pygame.Surface:
        return self.__Window.screen

    @property
    def GameFPS(self) -> float:
        return self.__Runtime.getGameFPS()

    @property
    def MSDeltaTime(self) -> int:
        return self.__Runtime.getTime()

    @property
    def SDeltaTime(self) -> float:
        return self.__Runtime.getTime() / 1000

    @property
    def FPS(self) -> float:
        return self.__Runtime.FPS

    @FPS.setter
    def FPS(self, value: float):
        self.__Runtime.FPS = value

    @property
    def MainState(self) -> Callable:
        return self.__States.MainState

    @MainState.setter
    def MainState(self, state: Callable):
        self.__States.MainState = state

    @property
    def CurState(self) -> Callable:
        return self.__States.CurState

    @CurState.setter
    def CurState(self, state: Callable):
        self.__States.CurState = state

    @property
    def WindowInstances(self):
        return self.__Window.getInstances()

    @property
    def MSElapsed(self):
        return self.__Runtime.MSElapsed

    @property
    def SElapsed(self):
        return self.__Runtime.SElapsed


class Base:
    def __init__(self):
        self.Engine = Engine.getEngine()