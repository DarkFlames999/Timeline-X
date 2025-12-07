from typing import Literal, Optional, Callable, TypeVar, runtime_checkable, Protocol, Dict, List, SupportsInt, SupportsFloat, Type, TYPE_CHECKING, Any
from abc import ABCMeta, abstractmethod
import pygame

__all__ = [
    # Regular
    'OPT_PATH',
    'OPT_CALL',
    'SupportsSimpleArithmetic',
    'SupportsReverseArithmetic',
    'SupportsInPlaceArithmetic',

    # Pygame
    'SURFACE',
    'OPT_SURFACE',
    'RECT',
    'RECT_POS_RENDER',
    'COLOR',
    'FONT',

    # Engine
    'EVENT_TYPES',
    'STATE_HANDLE',
    'TWEEN_FUNC',
    'TWEEN_VALUE_TYPES',
    'TWEEN_PROPS',

    # Imported Engine Files
    'FUNCTION',
    'EVENT_HANDLE',
    'CALL_TIMES',

    # Recursion Imports
    'SPRITE',
    'ANIMATION',
    'SPRITABLE',
    'GROUP',

    'COLLIDE_FUNC',
    'FONT_CHAR_FUNC'
]

# Regular
OPT_PATH = Optional[str]
OPT_CALL = Optional[Callable]

_S = TypeVar("_S", bound="SupportsSimpleArithmetic")
_R = TypeVar("_R", bound="SupportsReverseArithmetic")
_P = TypeVar("_P", bound="SupportsInPlaceArithmetic")
@runtime_checkable
class SupportsSimpleArithmetic(Protocol[_S], metaclass=ABCMeta):
    @abstractmethod
    def __add__(self, other: _S) -> _S: ...

    @abstractmethod
    def __sub__(self, other: _S) -> _S: ...

    @abstractmethod
    def __mul__(self, other: _S) -> _S: ...

    @abstractmethod
    def __truediv__(self, other: _S) -> _S: ...

    @abstractmethod
    def __floordiv__(self, other: _S) -> _S: ...

@runtime_checkable
class SupportsReverseArithmetic(Protocol[_R], metaclass=ABCMeta):
    @abstractmethod
    def __radd__(self, other: _R) -> _R: ...

    @abstractmethod
    def __sub__(self, other: _R) -> _R: ...

    @abstractmethod
    def __mul__(self, other: _R) -> _R: ...

    @abstractmethod
    def __truediv__(self, other: _R) -> _R: ...

    @abstractmethod
    def __floordiv__(self, other: _R) -> _R: ...

@runtime_checkable
class SupportsInPlaceArithmetic(Protocol[_P], metaclass=ABCMeta):
    @abstractmethod
    def __iadd__(self, other: _P) -> _P: ...

    @abstractmethod
    def __isub__(self, other: _P) -> _P: ...

    @abstractmethod
    def __imul__(self, other: _P) -> _P: ...

    @abstractmethod
    def __itruediv__(self, other: _P) -> _P: ...

    @abstractmethod
    def __ifloordiv__(self, other: _P) -> _P: ...

# Pygame
SURFACE = pygame.Surface | str
OPT_SURFACE = Optional[SURFACE]

RECT = pygame.Rect | pygame.FRect

RECT_POS_RENDER = Literal[
    'topleft', 'midtop', 'topright',
    'midleft', 'center', 'midright',
    'bottomleft', 'midbottom', 'bottomright'
]
SPRITE_DIRECTIONAL = Literal[
    'Positional', 'Directional'
]
COLOR = Optional[pygame.Color]
FONT = dict[str, pygame.Surface]

# Engine
EVENT_TYPES = Literal["Regular", "EventSend", "KeyDown", "KeyUp"]
STATE_HANDLE = Dict[str, Callable]
TWEEN_FUNC = Callable[[float], float]
TWEEN_VALUE_TYPES = SupportsReverseArithmetic | SupportsSimpleArithmetic | int | float | SupportsInt | SupportsFloat
TWEEN_PROPS = Dict[str, TWEEN_VALUE_TYPES]

# Imported Engine Files
from ..main.function import Function, SetFunction
FUNCTION = Function | SetFunction | Callable[[], None]
EVENT_HANDLE = Dict[str, Dict[int, List[FUNCTION]]]
CALL_TIMES = Dict[float, FUNCTION]

# Recursion Import Objects
SPRITE = Type['Sprite'] | Type['VectorSprite']
ANIMATION = Type['Animation'] | Type['VectorAnimation']
SPRITABLE = SPRITE | ANIMATION

GROUP = Type['Group'] | Type['GroupSingle']

if TYPE_CHECKING:
    from ..sprite.sprite import Sprite, VectorSprite
    from ..sprite.animation.anim import Animation, VectorAnimation
    from ..sprite.group import Group, GroupSingle

    SPRITE = Sprite | VectorSprite
    ANIMATION = Animation | VectorAnimation
    SPRITABLE = SPRITE | ANIMATION

    GROUP = Group | GroupSingle

COLLIDE_FUNC = Callable[[SPRITABLE, SPRITABLE], Any]
FONT_CHAR_FUNC = Callable[[SPRITABLE], None]

