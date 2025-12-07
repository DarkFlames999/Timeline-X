import pygame


class Vector2(pygame.Vector2):
    @classmethod
    def zero(cls):
        """Same as Vector2()"""
        return Vector2(0,0)

    @classmethod
    def one(cls):
        """Same as Vector2(1, 1)"""
        return Vector2(1,1)

    @classmethod
    def x0(cls, value: float):
        """Vector2 but x is 0"""
        return Vector2(0, value)

    @classmethod
    def x1(cls, value: float):
        """Vector2 but x is 1"""
        return Vector2(1, value)

    @classmethod
    def y0(cls, value: float):
        """Vector2 but y is 0"""
        return Vector2(value, 0)

    @classmethod
    def y1(cls, value: float):
        """Vector2 but y is 1"""
        return Vector2(value, 1)

pygame.math.Vector2 = Vector2
pygame.Vector2 = Vector2