from .. import types
from ..utils.util import warn
from typing import Callable

__all__ = [
    'States'
]

class States(types.STATE_HANDLE):
    def __init__(self) -> None:
        super().__init__(
            Main = lambda: None
        )

        self.Current: str = "Main"

    def __call__(self):
        self.get(self.Current, lambda: None)()

    @property
    def MainState(self) -> Callable:
        return self["Main"]

    @MainState.setter
    def MainState(self, value: Callable) -> None:
        if value is None:
            self["Main"] = None
            warn("None value given: Replaced with an empty callable function")
            return
        self["Main"] = value

    @property
    def CurState(self) -> Callable:
        return self.get(self.Current, lambda: None)

    @CurState.setter
    def CurState(self, value: Callable) -> None:
        if value is None:
            self[self.Current] = lambda: None
            warn("None value given: Replaced with an empty callable function")
            return
        self[self.Current] = value


