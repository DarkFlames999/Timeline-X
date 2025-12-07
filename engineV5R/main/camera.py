from ..utils import wrappers as wrp, util
from .. import types
from typing import Type, Optional
from .engine import Base
import pygame

__all__ = ['Camera']

class Camera(Base, pygame.FRect):
    def __init__(self, windowID: int, *args):
        Base.__init__(self)
        pygame.FRect.__init__(self, *args)
        from .window import Window
        self.Window = Window.getInstances()[windowID-1]

        self.WorldPos: pygame.Vector2 = pygame.Vector2()
        self.Zoom: float = 1

        self.Track: Optional[Type['types.SPRITABLE']] = None
        self.TrackFocusFactor: float = 0.05
        self.Angle: float = 0

        self.__RenderType: types.RECT_POS_RENDER = 'center'

    @property
    def RenderType(self) -> types.RECT_POS_RENDER:
        return self.__RenderType

    @RenderType.setter
    @wrp.propConvertTo(lambda x: x if util.valueInLiteral(x, types.RECT_POS_RENDER) else 'center')
    def RenderType(self, value: types.RECT_POS_RENDER):
        self.__RenderType = value

    def worldPosTrack(self) -> pygame.Vector2:
        if not util.exists(self.Track):
            return pygame.Vector2()

        target = pygame.Vector2(getattr(self.Track.Rect, self.__RenderType, (0, 0)))
        return target * self.TrackFocusFactor + self.WorldPos * (1-self.TrackFocusFactor)

    def locate(self, pos: pygame.Vector2) -> pygame.Vector2:
        return pygame.Vector2(getattr(self, self.__RenderType, (0, 0))) + ((pos + self.WorldPos) * self.Zoom).rotate(self.Angle) -  self.WorldPos

    def renderSurface(self, surface: pygame.Surface, dest: pygame.typing.Point, size: pygame.typing.Point = (64, 64), color: pygame.typing.ColorLike = pygame.Color('white'), area: pygame.FRect = None, blend: int = 0, angle: float = 0, flipX: bool = False, flipY: bool = False, transparency: int = 255, renderType: types.RECT_POS_RENDER = 'center') -> tuple[pygame.Surface, pygame.FRect, pygame.Mask, pygame.Vector2]:
        image = surface.convert_alpha()

        if area:
            image = image.subsurface(area)

        image = util.transformSurface(image, pygame.Vector2(size), angle, flipX, flipY)
        if color:
            image.fill(color, special_flags=blend)
        image.fill((255, 255, 255, transparency), special_flags=pygame.BLEND_RGBA_MULT)

        pos: pygame.Vector2 = self.locate(pygame.Vector2(dest))

        rect: pygame.FRect = image.get_frect(**{renderType: pos})
        mask: pygame.Mask = pygame.mask.from_surface(image)

        return image, rect, mask, pos

    def renderSprite(self, spr: types.SPRITABLE) -> tuple[pygame.Surface, pygame.FRect, pygame.Mask, pygame.Vector2]:
        image, rect, mask, pos = spr.image, spr.rect, spr.mask, spr.Pos + spr.Offset
        newPos: pygame.Vector2 = self.locate(pos)

        setattr(rect, spr.RenderType, newPos)
        mask = pygame.mask.from_surface(image)

        return image, rect, mask, pos

    def renderSprite2(self, *groups):
        for group in groups:
            group.update()


    def drawSurface(self, surface: pygame.Surface, dest: pygame.typing.Point, size: pygame.typing.Point = (64, 64),
                    color: pygame.typing.ColorLike = pygame.Color('white'), area: pygame.FRect = None, blend: int = 0,
                    angle: float = 0, flipX: bool = False, flipY: bool = False, transparency: int = 255,
                    renderType: types.RECT_POS_RENDER = 'center'):
        self.Window.screen.blit(
            *self.renderSurface(surface, dest, size, color, area, blend, angle, flipX, flipY, transparency, renderType)[
             :2])  # Surface & FRect

    def drawSprite(self, spr: types.SPRITABLE):
        self.Window.screen.blit(*self.renderSprite(spr)[:2])
