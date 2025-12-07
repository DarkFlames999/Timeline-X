from threading import Lock
from collections import defaultdict
from weakref import WeakSet
from .logger import info, warning

class GameTree(dict):
    def __init__(self):
        import pygame
        info("Game Tree Initialized")
        pygame.init()

        self._Lock = Lock()

        self._Subs = defaultdict(WeakSet)
        super().__init__()

    def subscribe(self, cls, names):
        with self._Lock:
            for name in names:
                info(f"Subscribing {cls.__name__} to [{", ".join(names)}]")
                self._Subs[name].add(cls)

    def addLib(self, name, instance):
        with self._Lock:
            if self.get(name) is not None:
                warning(f"Re-subscribing {name} lib")
            self[name] = instance
            self.propagate()


    def propagate(self):
        for name, classes in self._Subs.items():
            if self.get(name) is None: continue
            for cls in classes:
                if hasattr(cls, name) and getattr(cls, name) is not None:
                    warning(f"Re-Propagating {name} to {cls.__name__} with {self.get(name)}")
                info(f"Propagating {name} to {cls.__name__}")
                setattr(cls, name, self.get(name))


gameTree = GameTree()
def subscribe(*names):
    def subwrap(cls):
        gameTree.subscribe(cls, names)
        return cls
    return subwrap


class BaseManager:
    def __init__(self, mgName, subName):
        info(f"Registering '{mgName}' to Game Tree with '{subName}'")
        gameTree.addLib(subName, self)
