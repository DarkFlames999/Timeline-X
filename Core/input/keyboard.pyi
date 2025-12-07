from typing import Any
from .key import Key
from .anyallkey import AnyKeys, AllKeys


class Keyboard:
    """
    The Keyboard Input Class
    Use __getitem__ to get a key state
    """

    __StrToInt: dict[str, int]
    __KeyDict: dict[int, Key]

    def __init__(self): ...

    def update(self, dt: float):
        """
        Updates with Delta Time in Seconds
        """
        ...

    def __getInt(self, k: int) -> Key:
        """
        Returns the Key from Int
        """
        ...

    def __getStr(self, k: str) -> Key:
        """
        Returns the Key from Str
        """

    def __getAny(self, k: AnyKeys) -> Key:
        """
        Returns the Key State for all keys, with any of them being used
        """
        ...

    def __getAll(self, k: AllKeys) -> Key:
        """
        Returns the Key State for all keys, with all of them being used
        """
        ...

    def __getListTuple(self, k: list|tuple) -> Key:
        """
        Returns the Key State using __getAny or __getAll depending if k[0] == any | all
        """
        ...

    def __onAny(self):
        """
        Returns the Key state using ALL keys, with any of them being used
        """
        ...

    def __onAll(self):
        """
        Returns the key state using ALL keys, with all of them being used
        """
        ...

    def __getitem__(self, key: int | str | tuple | list | AnyKeys | AllKeys | Any):
        """
        Returns the Key State via:\n
        int, str\n
        tuple[any|all, *keys(int|str)], list[any|all, *keys(int|str)]\n
        AnyKeys(*k: int|str|AnyKeys|AllKeys), AllKeys(*k: int|str|AnyKeys|AllKeys)
        """
        ...
