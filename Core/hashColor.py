import pygame


class HashColor(pygame.Color):
    def __hash__(self):
        return hash((self.r, self.g, self.b, self.a))