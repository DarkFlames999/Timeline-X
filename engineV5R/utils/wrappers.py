from typing import Callable
import pygame

__all__ = [
    "propConvertTo",
    'onChanged'
]


def getVarValue(self, var: str) -> str:
    newGet = var
    if newGet.startswith('__'):
        if hasattr(self, f'_{self.__class__.__name__}{var}'):
            newGet = f'_{self.__class__.__name__}{var}'
            return newGet
        for base in self.__class__.__bases__:
            if hasattr(self, f'_{base.__name__}{var}'):
                newGet = f'_{base.__name__}{var}'
                return newGet
    return newGet


def propConvertTo(__type: Callable):
    def decorator(func):
        def wrapper(self, value):
            return func(self, __type(value))
        return wrapper
    return decorator

def onChanged(var):
    def decorator(func):
        def wrapper(self, value):
            nVar = getVarValue(self, var)
            val = getattr(self, nVar)
            if val == value: return
            return func(self, value)
        return wrapper
    return decorator
