import pygame

__all__ = [
    'Runtime'
]

class Runtime:
    def __init__(self, fps: float = 60) -> None:
        self.FPS: float = fps
        self.__Elapsed: int = 0

        self.__Clock: pygame.Clock = pygame.Clock()

    def tick(self):
        self.__Elapsed += self.__Clock.tick(self.FPS)

    def getTime(self) -> int:
        return self.__Clock.get_time()

    def getRawTime(self) -> int:
        return self.__Clock.get_rawtime()

    def getGameFPS(self) -> float:
        return self.__Clock.get_fps()

    @property
    def MSElapsed(self) -> int:
        return self.__Elapsed

    @property
    def SElapsed(self) -> float:
        return self.__Elapsed / 1000

