from ..main.engine import Base
from .. import types
from typing import Callable

class Timer(Base):
    def __init__(self, delay: float = 0, interval: float = 1, repeat: int = 1, onComplete: Callable = lambda: None, callOnTimes: types.CALL_TIMES = {}) -> None:
        self.Delay: float = delay
        self.Interval: float = interval
        self.OnComplete: Callable = onComplete
        self.CallOnTimes: types.CALL_TIMES = callOnTimes
        self.Repeat: int = repeat

        self.Playing: bool = False
        self.Paused: bool = False
        self.Completed: bool = False
        self.Delayed: bool = False

        self.CurRepeat: int = repeat
        self.CurTimer: float = 0
        super().__init__()

    def start(self) -> None:
        self.Playing = True
        self.Paused = False
        self.Completed = False
        self.Delayed = False

        self.CurTimer = 0
        self.CurRepeat = self.Repeat

        if self in self.Engine.TimerHandler:
            self.Engine.TimerHandler.remove(self)
        self.Engine.TimerHandler.append(self)

    def stop(self) -> None:
        self.Playing = False
        self.Paused = False
        self.Completed = True

        if self in self.Engine.TimerHandler:
            self.Engine.TimerHandler.remove(self)

        self.OnComplete()

    def pause(self) -> None:
        self.Paused = True

    def resume(self) -> None:
        self.Paused = False
