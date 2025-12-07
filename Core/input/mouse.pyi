from .key import Key
import pygame


class Mouse:
    """
    The Mouse Input Class
    """

    __DesktopPos: pygame.Vector2
    __Pos: pygame.Vector2
    __Delta: pygame.Vector2

    LMB: Key = Key()
    RMB: Key = Key()
    MMB: Key = Key()

    SideB1: Key = Key()
    SideB2: Key = Key()

    __Visible: bool = True

    MouseWheel: pygame.Vector2  # Because of those special types of mice with the horizontal scroll

    def onWheel(self, e):
        """
        To be bound with the Engine's Events handler\n
        Handles MouseWheel scroll
        """
        ...

    def update(self, dt):
        """
        Updates Mouse States with Delta Time in Seconds
        """
        ...

    @property
    def Pos(self) -> pygame.Vector2:
        """
        Mouse Position
        """
        ...

    @property
    def Delta(self):
        """
        Change in Mouse Position
        """
        ...

    @Pos.setter
    def Pos(self, value):
        """
        Sets the Mouse Position
        """
        ...

    @property
    def Visible(self):
        """
        Mouse Visibility
        """
        ...

    @Visible.setter
    def Visible(self):
        """
        Sets the Mouse Visibility
        """
        ...

    @property
    def DesktopPos(self):
        """
        Mouse Position With Respect to the Desktop
        """
        ...
