import pygame

__all__ = [
    'Frame',
    'FrameGroup',
    'AnimSelector'
]

class Frame:
    def __init__(self, image: pygame.Surface = pygame.Surface((0, 0)), offset: pygame.Vector2 = pygame.Vector2()):
        self.Image: pygame.Surface = image.copy().convert_alpha()
        self.Offset: pygame.Vector2 = offset.copy()

class FrameGroup(list[Frame]):
    def __init__(self, *frames: Frame):
        super().__init__(frames)

    def add(self, *frames: Frame):
        self.extend(frames)

    def remove(self, *frames: Frame):
        for frame in self:
            if frame not in self: continue
            self.remove(frame)

class AnimSelector(dict[str, FrameGroup]):
    def __init__(self, **groups: FrameGroup):
        super().__init__(**groups)
        self.Selected = list(groups.keys())[0]
        self.Index = 0

    @property
    def SelectedGroup(self) -> FrameGroup:
        return self.get(self.Selected, FrameGroup())

    @property
    def SelectedFrame(self) -> Frame:
        try:
            return self.SelectedGroup[self.Index]
        except IndexError:
            return Frame()
