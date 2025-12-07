from Game_Engine.game_tree import subscribe
from pygame import sprite


@subscribe("CMG")
class Entity(sprite.Sprite):
    CMG = None

    def __init__(self, image = None):
        super().__init__()

        if image:
            self.image = image
            self.rect = self.image.get_rect()

    def update(self):
        ...