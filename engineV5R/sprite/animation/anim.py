from ...utils import load
from ..sprite import Sprite, _Vector
from .base import AnimSelector, FrameGroup, Frame
from typing import Self


__all__ = [
    'Animation',
    'VectorAnimation'
]


class Animation(Sprite):
    def __init__(self, anim: AnimSelector, fps: float = 24):
        self.Animation: AnimSelector = anim
        self.FPS: float = fps
        self.CurTime: float = 0

        self.Playing: bool = False
        self.Paused: bool = False
        self.Completed: bool = False
        self.Loop: bool = False

        super().__init__(self.CurFrame.Image.copy().convert_alpha())

    def animate(self):
        if self.Paused or self.Completed or not self.Playing: return
        if self.CurTime >= 1 / self.FPS:
            self.Index += 1
            if self.Index >= len(self.CurGroup):
                if not self.Loop:
                    self.Index = len(self.CurGroup) - 1
                    self.Completed = True
                    self.Playing = False
                    self.Paused = False
                else:
                    self.Index = 0

            self.setImage(self.CurFrame.Image.copy().convert_alpha())
            self.Offset = self.CurFrame.Offset.copy()
            self.CurTime = 0

        self.CurTime += self.Engine.SDeltaTime

    def play(self, anim: str, loop: bool = False, fps: int = None):
        self.CurTime = 0

        self.Playing = True
        self.Paused = False
        self.Completed = False

        self.Loop = loop
        self.FPS = fps or self.FPS

        self.CurAnim = anim
        self.Index = 0

    def pause(self):
        self.Paused = True

    def resume(self):
        self.Paused = False

    @property
    def CurAnim(self) -> str:
        return self.Animation.Selected

    @CurAnim.setter
    def CurAnim(self, value: str):
        self.Animation.Selected = value

    @property
    def Index(self) -> int:
        return self.Animation.Index

    @Index.setter
    def Index(self, value: int):
        self.Animation.Index = value

    @property
    def CurGroup(self) -> FrameGroup:
        return self.Animation.SelectedGroup

    @property
    def CurFrame(self) -> Frame:
        return self.Animation.SelectedFrame

    @classmethod
    def fromFolder(cls, file: str, folder: str = 'animation') -> Self:
        return cls(load.animation(file, folder))

    @classmethod
    def fromPath(cls, path: str) -> Self:
        return cls(load.animation(path))


class VectorAnimation(Animation, _Vector):
    def __init__(self, anim: AnimSelector, fps: float = 24):
        super().__init__(anim, fps)