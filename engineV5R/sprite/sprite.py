from ..main.engine import Base
from ..utils import load, wrappers as wrp, util
from .. import types
from pygame.sprite import Sprite as PySprite, Group as PyGroup, GroupSingle as PyGSingle
import pygame


class _Vector:
    def __init__(self):
        self.__Velocity: pygame.Vector2 = pygame.Vector2(0,0)
        self.__Acceleration: pygame.Vector2 = pygame.Vector2(0,0)

        self.__Directional: types.SPRITE_DIRECTIONAL = 'Positional'

    @property
    def Velocity(self) -> pygame.Vector2:
        return self.__Velocity

    @property
    def Acceleration(self) -> pygame.Vector2:
        return self.__Acceleration

    @property
    def Directional(self) -> types.SPRITE_DIRECTIONAL:
        return self.__Directional

    @Velocity.setter
    @wrp.propConvertTo(pygame.Vector2)
    def Velocity(self, new: pygame.typing.Point):
        self.__Velocity = new

    @Acceleration.setter
    @wrp.propConvertTo(pygame.Vector2)
    def Acceleration(self, new: pygame.typing.Point):
        self.__Acceleration = new

    @Directional.setter
    @wrp.propConvertTo(lambda x: x if util.valueInLiteral(x, types.SPRITE_DIRECTIONAL) else 'Positional')
    def Directional(self, new: types.SPRITE_DIRECTIONAL):
        self.__Directional = new


class Sprite(Base, PySprite):
    def __init__(self, image: types.SURFACE, *groups: PyGroup | PyGSingle):
        Base.__init__(self)

        self.__SGroup: PyGSingle = PyGSingle()
        PySprite.__init__(self, *groups, self.__SGroup)

        self.__OGImage: pygame.Surface = None
        self.__OGRect: types.RECT = None
        self.__OGMask: pygame.Mask = None

        self.__CImage: pygame.Surface = None  # Color Cache
        self.__OImage: pygame.Surface = None  # Opacity Cache
        self.__SImage: pygame.Surface = None  # Scale Cache
        self.__RImage: pygame.Surface = None  # Rotate Cache
        self.__FImage: pygame.Surface = None  # Flip Cache

        self.__Image: pygame.Surface = None
        self.__Rect: types.RECT = None
        self.__Mask: pygame.Mask = None

        self.__Color: pygame.Color | None = None
        self.__Blend: int = 0
        self.__Opacity: float = 255

        self.__Pos: pygame.Vector2 = pygame.Vector2(0,0)
        self.__Size: pygame.Vector2 = pygame.Vector2(0,0)
        self.__Offset: pygame.Vector2 = pygame.Vector2(0,0)

        self.__RenderType: types.RECT_POS_RENDER = 'center'

        self.__Angle: float = 0
        self.__FlipX: bool = False
        self.__FlipY: bool = False

        # Setup
        self.setImage(image)
        self.__Size = pygame.Vector2(self.__OGRect.size)
        self.loadCache(color=True)

    def loadCache(self, *, color: bool = False, opacity: bool = False, rotate: bool = False, scale: bool = False, flip: bool = False, final: bool = False):
        if color:
            self.__createColorCache()
        if color or opacity:
            self.__createOpacityCache()
        if color or opacity or scale:
            self.__createScaleCache()
        if color or opacity or scale or rotate:
            self.__createRotateCache()
        if color or opacity or scale or rotate or flip:
            self.__createFlipCache()
        if color or opacity or scale or rotate or flip or final:
            self.__createFinalCache()

    def __createColorCache(self):
        self.__CImage = self.__OGImage.copy().convert_alpha()
        if self.__Color is not None:
            self.__CImage.fill(self.__Color, special_flags=self.__Blend)

    def __createOpacityCache(self):
        self.__OImage = self.__CImage.copy()
        self.__OImage.fill((255, 255, 255, self.__Opacity), special_flags=pygame.BLEND_RGBA_MULT)

    def __createScaleCache(self):
        self.__SImage = pygame.transform.scale(self.__OImage.copy(), self.__Size)

    def __createRotateCache(self):
        self.__RImage = pygame.transform.rotate(self.__SImage.copy(), self.__Angle)

    def __createFlipCache(self):
        self.__FImage = pygame.transform.flip(self.__RImage.copy(), self.__FlipX, self.__FlipY)

    def __createFinalCache(self):
        self.__Image = self.__FImage.copy().convert_alpha()
        self.__Rect = self.__Image.get_frect(**{self.__RenderType: self.__Pos + self.__Offset})
        self.__Mask = pygame.mask.from_surface(self.__Image)

    def setImage(self, image: types.SURFACE, keepSize: bool = False):
        self.__OGImage = load.image(image).copy().convert_alpha()
        self.__OGRect = image.get_frect(**{'size': self.__Size if keepSize else self.__OGImage.size})
        self.__OGMask = pygame.mask.from_surface(self.__OGImage)

    def update(self, *args, **kwargs):
        pass

    @property
    def Pos(self) -> pygame.Vector2:
        return self.__Pos

    @Pos.setter
    @wrp.propConvertTo(pygame.Vector2)
    def Pos(self, pos: pygame.typing.Point):
        self.__Pos = pos

    @property
    def Size(self) -> pygame.Vector2:
        return self.__Size

    @Size.setter
    @wrp.onChanged('__Size')
    @wrp.propConvertTo(pygame.Vector2)
    def Size(self, size: pygame.typing.Point):
        self.__Size = size
        self.loadCache(scale=True)

    @property
    def Offset(self) -> pygame.Vector2:
        return self.__Offset

    @Offset.setter
    @wrp.propConvertTo(pygame.Vector2)
    def Offset(self, offset: pygame.typing.Point):
        self.__Offset = offset

    @property
    def RenderType(self) -> types.RECT_POS_RENDER:
        return self.__RenderType

    @RenderType.setter
    @wrp.propConvertTo(lambda x: x if util.valueInLiteral(x, types.RECT_POS_RENDER) else 'center')
    def RenderType(self, renderType: types.RECT_POS_RENDER):
        self.__RenderType = renderType

    @property
    def Color(self) -> pygame.Color:
        return self.__Color

    @Color.setter
    @wrp.propConvertTo(pygame.Color)
    def Color(self, color: pygame.typing.ColorLike):
        if color == self.__Color: return
        self.__Color = color
        self.loadCache(color=True)

    @property
    def Blend(self) -> int:
        return self.__Blend

    @Blend.setter
    @wrp.propConvertTo(int)
    def Blend(self, blend: int):
        if blend == self.__Blend: return
        self.__Blend = blend
        self.loadCache(color=True)

    @property
    def Opacity(self) -> float:
        return self.__Opacity

    @Opacity.setter
    @wrp.propConvertTo(lambda x: pygame.math.clamp(x, 0, 255))
    def Opacity(self, opacity: float):
        if opacity == self.__Opacity: return
        self.__Opacity = opacity
        self.loadCache(opacity=True)

    @property
    def Angle(self) -> float:
        return self.__Angle

    @Angle.setter
    @wrp.propConvertTo(float)
    def Angle(self, angle: float):
        if angle == self.__Angle: return
        self.__Angle = angle
        self.loadCache(rotate=True)

    @property
    def FlipX(self) -> bool:
        return self.__FlipX

    @FlipX.setter
    @wrp.propConvertTo(bool)
    def FlipX(self, flipX: bool):
        if flipX == self.__FlipX: return
        self.__FlipX = flipX
        self.loadCache(flip=True)

    @property
    def FlipY(self) -> bool:
        return self.__FlipY

    @FlipY.setter
    @wrp.propConvertTo(bool)
    def FlipY(self, flipY: bool):
        if flipY == self.__FlipY: return
        self.__FlipY = flipY
        self.loadCache(flip=True)

    # Pygame Stuff
    @property
    def image(self) -> pygame.Surface:
        return self.__Image

    @property
    def rect(self) -> types.RECT:
        return self.image.get_frect(**{self.__RenderType: self.__Pos + self.__Offset})

    @property
    def mask(self) -> pygame.Mask:
        return pygame.mask.from_surface(self.image)

    @property
    def GroupSingle(self) -> PyGSingle:
        return self.__SGroup


class VectorSprite(Sprite, _Vector):
    def __init__(self, image: types.SURFACE, *groups: PyGroup | PyGSingle):
        super().__init__(image, *groups)
