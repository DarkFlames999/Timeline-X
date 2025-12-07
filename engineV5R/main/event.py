from .. import types
from ..utils.util import valueInLiteral, existThenCall
from .function import SetFunction
import pygame


__all__ = [
    'EventHandler'
]


class EventHandler(types.EVENT_HANDLE):
    def __init__(self) -> None:
        def windowClose(event: pygame.Event):
            from .window import Window

            w: Window = Window.getInstances()[event.window.id-1]  # Main ID is at 1 so subtract 1
            existThenCall(w.onClose)

        super().__init__(
            Regular = {},
            EventSend = {
                pygame.WINDOWCLOSE: [windowClose]
            },
            KeyDown = {},
            KeyUp = {}
        )

        self.EventExclusions: list[int] = [
            pygame.WINDOWSIZECHANGED
        ]

    def addEvent(self, to: types.EVENT_TYPES, event_id: int, func: SetFunction) -> None:
        if to not in valueInLiteral(to, types.EVENT_TYPES):
            raise ValueError(to, 'is not a valid event type')
        self[to][event_id] = self[to].get(event_id, [])  # Either the ID type exists or returns an empty list
        self[to][event_id].append(func)

    def __callID(self, type: types.EVENT_TYPES, event: pygame.event.Event, *, send: bool = False, key: bool = False) -> None:

        for func in self[type].get(event.key if key else event.type, []):
            func(event) if send else func()

    def __call__(self) -> None:
        for event in pygame.event.get(exclude=self.EventExclusions):
            self.__callID("Regular", event)
            self.__callID("EventSend", event, send=True)

            if event.type == pygame.KEYDOWN:
                self.__callID("KeyDown", event, key=True)
            elif event.type == pygame.KEYUP:
                self.__callID("KeyUp", event, key=True)