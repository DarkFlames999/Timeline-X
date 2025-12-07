from pygame import Clock as _C
from Game_Engine.game_tree import BaseManager


class Clock(BaseManager):
    def __init__(self, fps = 60):
        super().__init__("Clock Manager", "CMG")

        self.__Clock = _C()
        self.FPS = fps
        self.__DeltaTime = 0
        self.__Elapsed = 0

    @property
    def DeltaTime(self):
        return self.__DeltaTime

    @property
    def SDeltaTime(self):
        return self.__DeltaTime / 1000

    @property
    def Elapsed(self):
        return self.__Elapsed

    @property
    def SElapsed(self):
        return self.__Elapsed / 1000

    def tick(self):
        self.__DeltaTime = self.__Clock.tick(self.FPS)
        self.__Elapsed += self.__DeltaTime
        return self.__DeltaTime



