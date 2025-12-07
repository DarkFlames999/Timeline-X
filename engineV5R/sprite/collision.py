from .. import types
from typing import Type
import pygame

__all__ = [
    'collideRect',
    'collideMask',
    'collideSprite',
    'collideGroup',
]

def collideRect(spr1: Type['types.SPRITABLE'], spr2: Type['types.SPRITABLE']) -> bool:
    return spr1.rect.colliderect(spr2.rect)

def collideMask(spr1: Type['types.SPRITABLE'], spr2: Type['types.SPRITABLE']) -> tuple[int, int]:
    return spr1.mask.colliderect(spr2.mask, pygame.Vector2(spr2.rect.topleft) - pygame.Vector2(spr1.rect.topleft))

def collideSprite(spr: Type['types.SPRITABLE'], group: Type['types.GROUP'], collide: Type['types.COLLIDE_FUNC']) -> list['types.SPRITABLE']:
    arr = []
    for sprite in group:
        if not collide(spr, sprite): continue
        arr.append(sprite)
    return arr

def collideGroup(groupA: 'types.GROUP', groupB: 'types.GROUP', collide: 'types.COLLIDEFUNC') -> dict['types.SPRITELIKE', list['types.SPRITELIKE']]:
    """
    Returns a 2D Array:
    data[0] = Array of Sprites colliding with GroupA
    data[1] = Array of Sprites colliding with GroupB
    """
    data = {}
    for spriteA in groupA:
        data[spriteA] = collideSprite(spriteA, groupB, collide)

    return data