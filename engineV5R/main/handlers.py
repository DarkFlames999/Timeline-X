from ..utils.util import existThenCall
from ..timer import Timer
from ..tween import Tween
from .. import types
from .engine import Base
from typing import Callable, Any
from pygame.math import clamp

__all__ = [
    'TimerHandler',
    'SequenceHandler',
    'TweenHandler'
]

class TimerHandler(Base, list[Timer]):
    def __init__(self):
        super(Base, self).__init__()
        self.CallInstances: dict[Timer, list[Callable]] = {}

    def __call__(self):
        for timer in self[:]:
            if timer.Paused or timer.Completed or timer.Stopped: self.remove(timer); continue
            self.CallInstances[timer] = self.CallInstances.get(timer, [])  # If Not Existing, then Default is new List

            if timer.Delayed:
                for time, func in timer.CallOnTimes.items():
                    if func in self.CallInstances[timer]: continue
                    if timer.CurTimer >= time:
                        func()
                        self.CallInstances[timer].append(func)


            if timer.CurTimer >= timer.Interval if timer.Delayed else timer.Delay:
                timer.CurTimer = 0
                if not timer.Delayed:
                    timer.Delayed = True
                    continue
                timer.CurRepeat -= 1
                if timer.CurRepeat <= 0:
                    self.remove(timer)
                    timer.Stopped = True
                    timer.Complete = True
                    existThenCall(timer.OnComplete)

            timer.CurTimer += self.Engine.SDeltaTime

    def remove(self, timer: Timer):
        try:
            del self.CallInstances[timer]
        except:
            pass
        super().remove(timer)


class SequenceHandler(Base, list[Timer]):
    def __init__(self):
        super(Base, self).__init__()
        self.CallInstances: list[Callable] = []

    @property
    def ActiveTimer(self):
        try:
            return self[0]
        except IndexError:
            return None

    def __call__(self):
        if not self.ActiveTimer: return
        timer: Timer = self.ActiveTimer
        if timer.Delayed:
            for time, func in timer.CallOnTimes.items():
                if func in self.CallInstances: continue
                if timer.CurTimer >= time:
                    func()
                    self.CallInstances.append(func)

        if timer.CurTimer >= timer.Interval if timer.Delayed else timer.Delay:
            timer.CurTimer = 0
            if not timer.Delayed:
                timer.Delayed = True
                return
            timer.CurRepeat -= 1
            if timer.CurRepeat <= 0:
                self.pop(0)
                self.CallInstances.clear()
                timer.Stopped = True
                timer.Complete = True
                existThenCall(timer.OnComplete)

        timer.CurTimer += self.Engine.SDeltaTime


class TweenHandler(Base, list[Tween]):
    def __init__(self):
        super(Base, self).__init__()
        self.OriginInstances: dict[Tween, dict[str, Any]] = {}
        self.CallInstances: dict[Tween, list[Callable]] = {}

    def setOriginProperty(self, tween: Tween, propertyName: str, propertyValue: types.SupportsReverseArithmetic) -> None:
        self.OriginInstances[tween][propertyName] = propertyValue

    def getOriginProperty(self, tween: Tween, propertyName: str) -> types.SupportsReverseArithmetic| None:
        return self.OriginInstances[tween].get(propertyName, None)

    def __call__(self):
        for tween in self:
            if tween.Completed: self.remove(tween); continue
            self.OriginInstances[tween] = self.OriginInstances.get(tween, {})
            self.CallInstances[tween] = self.CallInstances.get(tween, [])  # If Instance doesn't exist, create one

            for time, func in tween.CallOnTimes.items():
                if func in self.CallInstances[tween]: continue
                if tween.CurTime >= time:
                    func()
                    self.CallInstances[tween].append(func)

            if tween.CurTime >= tween.Time:
                self.remove(tween)
                del self.OriginInstances[tween]
                del self.CallInstances[tween]


            for pName, pValue in tween.Properties.items():
                if self.getOriginProperty(tween, pName) is None:
                    self.setOriginProperty(tween, pName, getattr(tween.Obj, pName))

                originValue: types.TWEEN_VALUE_TYPES = self.getOriginProperty(tween, pName)
                expectedValue: types.TWEEN_VALUE_TYPES = pValue
                difference: types.TWEEN_VALUE_TYPES = expectedValue - originValue

                final: types.TWEEN_VALUE_TYPES = originValue + (tween.TweenProgress * difference)

                setattr(tween.Obj, pName, final)

            tween.CurTime = clamp(tween.CurTime + self.Engine.SDeltaTime, 0, tween.Time)

