from Game_Engine.game_tree import BaseManager
import pygame

class EventHandler(BaseManager, dict):
    def __init__(self):
        dict.__init__(self,
            {
                "Regular": {},
                "KeyDown": {},
                "KeyUp": {},
            }
        )

        BaseManager.__init__(self, "Event Manager", "EMG")

        self.addEvent("Regular", pygame.QUIT, quit)

    def addEvent(self, eventType, event, function):
        self.get(eventType, {})[event] = function

    def removeEvent(self, eventType, event):
        self.get(eventType, {})[event] = None

    def call(self, eventType, event):
        self.get(eventType, {})[event]()

    def exists(self, eventType, event):
        return self.get(eventType, {}).get(event, False)

    def handle(self):
        for event in pygame.event.get():
            if self.exists("Regular", event.type):
                self.call("Regular", event.type)
            if event.type == pygame.KEYDOWN:
                if self.exists("KeyDown", event.key):
                    self.call("KeyDown", event.key)
            elif event.type == pygame.KEYUP:
                if self.exists("KeyUp", event.key):
                    self.call("KeyUp", event.key)
