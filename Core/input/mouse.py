from Core.input.key import Key
import pygame


class Mouse:
    def __init__(self):
        self.__DesktopPos =    pygame.Vector2(pygame.mouse.get_pos(True))
        self.__Pos =        pygame.Vector2(pygame.mouse.get_pos())
        self.__Delta =      pygame.Vector2(pygame.mouse.get_rel())

        self.LMB =          Key()
        self.RMB =          Key()
        self.MMB =          Key()

        self.SideB1 =       Key()
        self.SideB2 =       Key()

        self.__Visible =    True

        self.MouseWheel =   pygame.Vector2()  # To be binded with the engine

    def onWheel(self, e):
        self.MouseWheel = pygame.Vector2(e.precise_x, e.precise_y)

    def update(self, dt):
        self.__DesktopPos = pygame.Vector2(pygame.mouse.get_pos(True))
        self.__Pos = pygame.Vector2(pygame.mouse.get_pos())
        self.__Delta = pygame.Vector2(pygame.mouse.get_rel())

        pressed =   pygame.mouse.get_just_pressed()
        held =      pygame.mouse.get_pressed(5)
        released =  pygame.mouse.get_just_released()

        def updateKey(k, i):
            k.Pressed = pressed[i]
            k.Released = released[i]
            k.Held = held[i]

            k.update(dt)

        updateKey(self.LMB, 0)
        updateKey(self.MMB, 1)
        updateKey(self.RMB, 2)

        updateKey(self.SideB1, 3)
        updateKey(self.SideB2, 4)

    @property
    def Pos(self):
        return self.__Pos

    @property
    def Delta(self):
        return self.__Delta

    @Pos.setter
    def Pos(self, value):
        pygame.mouse.set_pos(self.__Pos)
        self.__Pos = pygame.Vector2(value)

    @property
    def Visible(self):
        return self.__Visible

    @Visible.setter
    def Visible(self, value):
        self.__Visible = value
        pygame.mouse.set_visible(self.__Visible)

    @property
    def DesktopPos(self):
        return self.__DesktopPos





