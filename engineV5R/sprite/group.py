from pygame.sprite import Group as G, GroupSingle as GS, Sprite as S


class Group(G):
    def __init__(self, *sprites: S):
        super().__init__(*sprites)

class GroupSingle(GS):
    def __init__(self, sprite: S):
        super().__init__(sprite)

