from ..main.engine import Base
from ..utils.util import warn
from .. import types
from pytweening import linear


__all__ = [
    'Tween'
]


class _BaseObject:
    def __init__(self):
        self.Value = 0


class Tween(Base):
    def __init__(self, func: types.TWEEN_FUNC = linear, time: float = 1, obj: object = _BaseObject(), properties: types.TWEEN_PROPS=None, onComplete: types.FUNCTION = lambda: None, callOnTimes: dict[float, types.FUNCTION] = {}):
        super().__init__()
        if properties is None:
            properties = {"Value": 1}

        self.TweenFunc: types.TWEEN_FUNC = func
        self.Time: float = time
        self.Obj: object = obj
        self.Properties: types.TWEEN_PROPS = properties
        self.OnComplete: types.FUNCTION = onComplete
        self.CallOnTimes: dict[float, types.FUNCTION] = callOnTimes

        self.CurTime: float = 0

        self.Started: bool = False
        self.Paused: bool = False
        self.Completed: bool = False

    def start(self):
        self.Started = True
        self.Paused = False
        self.Completed = False

        self.CurTime = 0
        if self in self.Engine.TweenHandler:
            self.Engine.TweenHandler.remove(self)
        self.Engine.TweenHandler.append(self)

    def stop(self):
        self.Started = False
        self.Paused = False
        self.Completed = True

        if self in self.Engine.TweenHandler:
            self.Engine.TweenHandler.remove(self)

        self.OnComplete()

    def pause(self):
        self.Paused = True

    def resume(self):
        self.Paused = False

    @property
    def TimeProgress(self) -> float:
        return self.CurTime / self.Time

    @property
    def TweenProgress(self) -> float:
        return self.TweenFunc(self.CurTime / self.Time)

    def Value(self, attr: str = 'Value') -> types.SupportsSimpleArithmetic:
        value = getattr(self.Obj, attr)
        if not isinstance(value, types.SupportsSimpleArithmetic):
            warn("Attribute doesn't support __add__, __sub__, __mul__, __truediv__ and __floordiv__")
        return value


