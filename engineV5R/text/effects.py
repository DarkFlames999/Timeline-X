from __future__ import annotations
from ..types import SPRITABLE, FONT_CHAR_FUNC


def shake(intensityX: float, intensityY: float) -> FONT_CHAR_FUNC:
    def func(spr: SPRITABLE):
        nonlocal intensityX, intensityY
        import random
        spr.Pos.x += random.random() * intensityX
        spr.Pos.y += random.random() * intensityY
    return func


def wave(spaceDifference: float, speed: float, intensity: float) -> FONT_CHAR_FUNC:
    def func(spr: SPRITABLE):
        from ..main.engine import Engine
        nonlocal spaceDifference, speed, intensity
        import math
        e = Engine.getEngine()
        spr.Pos.y += math.sin(math.radians((spr.Pos.x * spaceDifference) + e.MSElapsed) / speed) * intensity
    return func

def shakeWave(shakeX: float, shakeY: float, waveSpace: float, waveSpeed: float, waveIntensity: float) -> FONT_CHAR_FUNC:
    def func(spr: SPRITABLE):
        wave(waveSpace, waveSpeed, waveIntensity)(spr)
        shake(shakeX, shakeY)(spr)
    return func
