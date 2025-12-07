from __future__ import annotations
from .. import types
from ..utils import load, wrappers as wrp, util
from ..sprite.group import Group
from ..sprite.sprite import Sprite
from ..main.window import Window
from .message import MessageGroup
import pygame


__all__ = [
    'Font',
    'Text'
]


class Font(types.FONT):
    def __init__(self, fontData: types.FONT):
        super().__init__(**fontData)

    @classmethod
    def fromFolder(cls, file: str, folder: str='font') -> Font:
        return cls(load.font(file, folder))

    @classmethod
    def fromPath(cls, path: str) -> Font:
        return cls(load.font(path))


class Text(Group):
    def __init__(self, font: Font):
        super().__init__()

        self.__Font: Font = font
        self.Messages: MessageGroup = MessageGroup()

        self.__Pos: pygame.Vector2 = pygame.Vector2(0,0)
        self.__Scale: pygame.Vector2 = pygame.Vector2(1, 1)
        self.__Spacing: pygame.Vector2 = pygame.Vector2(0,0)

        self.Angle: float = 0
        self.FlipX: bool = False
        self.FlipY: bool = False

        self.Error: list[str] = []
        self.ErrorClearOnRender: bool = False

    def render(self, window: Window | int):
        self.empty()

        win = Window.getInstances()[window-1] if isinstance(window, int) else window if isinstance(window,
                                                                                                 Window) else None
        if win is None:
            raise ValueError("Window Not Found with Window Type", window)

        if self.ErrorClearOnRender: self.Error.clear()
        pos = self.__Pos.copy()

        def newline():
            nonlocal pos, self
            pos.x = self.__Pos.x
            pos += pygame.Vector2(0, (self.__Font.get('A', self.__Font.get('a')).size[1] * self.Scale.y) + self.__Spacing.y).rotate(self.Angle)

        def space():
            nonlocal pos, self
            pos += pygame.Vector2((self.__Font.get('A', self.__Font.get('a')).size[0] * self.Scale.x) + self.__Spacing.x, 0).rotate(self.Angle)

        for msg in self.Messages[::(-1 if self.FlipX else 1)]:
            for i, char in enumerate(msg.Text[::(-1 if self.FlipX else 1)]):
                if char == '\n':
                    newline()
                    continue

                if char == ' ':
                    space()
                    continue

                if char in self.Error: continue

                try:
                    self.__Font[char].copy()
                except KeyError:
                    util.warn("Font could not grab char", char)
                    self.Error.append(char)
                    continue

                spr = Sprite(self.__Font[char].copy())
                spr.RenderType = 'bottomleft'
                spr.Pos = pos.copy()

                spr.Color = pygame.Color(msg)
                spr.Blend = pygame.BLEND_RGBA_MULT

                spr.Size = pygame.Vector2(spr.Size.x * self.Scale.x, spr.Size.y * self.Scale.y)

                spr.Angle = self.Angle
                spr.FlipX = self.FlipX
                spr.FlipY = self.FlipY

                spr.add(self)
                win.Sprites.add(*self)

                pos += pygame.Vector2(spr.Size.x + self.__Spacing.x, 0).rotate(self.Angle)

                if msg.CharFunc:
                    msg.CharFunc(spr)

    @property
    def Pos(self) -> pygame.Vector2:
        return self.__Pos

    @Pos.setter
    @wrp.propConvertTo(pygame.Vector2)
    def Pos(self, value: pygame.typing.Point):
        self.__Pos = value

    @property
    def Scale(self) -> pygame.Vector2:
        return self.__Scale

    @Scale.setter
    @wrp.propConvertTo(pygame.Vector2)
    def Scale(self, value: pygame.Vector2):
        self.__Scale = value

    @property
    def Spacing(self) -> pygame.Vector2:
        return self.__Spacing

    @Spacing.setter
    @wrp.propConvertTo(pygame.Vector2)
    def Spacing(self, value: pygame.Vector2):
        self.__Spacing = value

    @property
    def Font(self) -> Font:
        return self.__Font

    @Font.setter
    def Font(self, font: Font):
        self.__Font = font
