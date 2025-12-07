import pygame
from Core.event_handler import EventHandler
from Core.Clock import Clock
from Core.hashColor import HashColor
from Core.input import InputManager

class Game:
    def __init__(self):
        pygame.init()
        self.active = False
        self.event_handler = EventHandler()
        self.clock = Clock()
        self.input = InputManager()

        self.window = pygame.Window()
        self.window.get_surface()

    def update(self):
        self.input.update(self.clock.SDeltaTime)

        if self.input["W"].Pressed:
            print("Pressed")
        if self.input["A", "left"].Pressed:
            print("Left")
        if self.input[all, 'W', 'S'].Held:
            print("Held")

        print(self.input['W'])

    def draw(self): ...

    def gameLoop(self):
        self.clock.tick()
        self.event_handler.handle()

        self.update()

        self.window.get_surface().fill((0, 0, 0))
        self.draw()
        self.window.flip()

    def run(self):
        self.active = True
        while self.active:
            self.gameLoop()


