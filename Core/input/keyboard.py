from Core.input.key import Key
from Core.input.anyallkey import AnyKeys, AllKeys, parseKeys
import pygame


class Keyboard:
    def __init__(self):
        self.__StrToInt = {
            pygame.key.name(getattr(pygame.constants, k)): getattr(pygame.constants, k) for k in dir(pygame.constants) if k.startswith('K_')
        }
        self.__KeyDict = {
            k: Key() for k in self.__StrToInt.values()
        }

    def update(self, dt):
        pressed = pygame.key.get_just_pressed()
        held = pygame.key.get_pressed()
        released = pygame.key.get_just_released()

        for kid, key in self.__KeyDict.items():
            key.Pressed = pressed[kid]
            key.Held = held[kid]
            key.Released = released[kid]

            key.update(dt)

    def __getInt(self, k):
        return self.__KeyDict[k]

    def __getStr(self, k):
        return self.__KeyDict[self.__StrToInt[k.lower()]]

    def __getAny(self, k):
        anyKey = Key()
        tKeys = [self[v] for v in k]

        def g(obj):
            return map(lambda x: getattr(x, obj), tKeys)

        anyKey.Pressed = any(g('Pressed'))
        anyKey.Held = any(g('Held'))
        anyKey.Released = any(g('Released'))

        anyKey.HoldTime = max(g('HoldTime'))
        anyKey.LastHoldTime = max(g('LastHoldTime'))

        anyKey.TotalPressCount = max(g('TotalPressCount'))
        anyKey.SinceLastPress = max(g('SinceLastPress'))
        anyKey.SinceReleased = max(g('SinceReleased'))
        return anyKey

    def __getAll(self, k):
        allKey = Key()
        tKeys = [self[v] for v in k]

        def g(obj):
            return map(lambda x: getattr(x, obj), tKeys)

        allKey.Pressed = all(g('Pressed'))
        allKey.Held = all(g('Held'))
        allKey.Released = all(g('Released'))

        allKey.HoldTime = min(g('HoldTime')) if allKey.Held else 0
        allKey.LastHoldTime = min(g('LastHoldTime'))

        allKey.TotalPressCount = min(g('TotalPressCount'))
        allKey.SinceLastPress = min(g('SinceLastPress'))
        allKey.SinceReleased = min(g('SinceReleased'))
        return allKey

    def __getListTuple(self, k):
        return self[parseKeys(*k)]

    def __onAny(self, *k):
        return self.__getAny(AnyKeys(*self.__KeyDict.keys()))

    def __onAll(self, *k):
        return self.__getAll(AllKeys(*self.__KeyDict.keys()))

    def __getitem__(self, key):
        return {
            int: self.__getInt,
            str: self.__getStr,
            list: self.__getListTuple,
            tuple: self.__getListTuple,
            AnyKeys: self.__getAny,
            AllKeys: self.__getAll,
            any: self.__onAny,
            all: self.__onAll
        }.get(type(key), lambda k: Key())(key)
