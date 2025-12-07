from .. import types
from .util import pathExists, xml, json, debug, exists
from .file import File
from multipledispatch import dispatch
from xml.etree.ElementTree import Element
from lxml.etree import _Element
from typing import get_args
import pygame, pygame.freetype

__all__ = [
    "image",
    "animation",
]

# Image Loader
@dispatch(get_args(types.OPT_PATH))
def image(path: types.OPT_PATH) -> pygame.Surface:
    debug("[ IMAGE ] Creating Image From Path:", path)
    if (not pathExists(path)) or path is None:
        raise FileNotFoundError(f"'{path}' does not exist.")
    return pygame.image.load(path).convert_alpha()

@dispatch(str, str)
def image(file: str, folder: str = 'image') -> pygame.Surface:
    debug("[ IMAGE ] Creating Image from File:", file, "; Folder:", folder)
    return pygame.image.load(File.image(file, folder))

@dispatch(pygame.Surface)
def image(surface: pygame.Surface) -> pygame.Surface:
    debug("[ IMAGE ] Creating Image From Surface:", surface)
    return surface.copy().convert_alpha()

@dispatch(float, float, float, float, float)
def image(w: float, h: float, r: float, g: float, b: float) -> pygame.Surface:
    debug(f"[ IMAGE ] Creating Image With Surface Properties:[w={w}; h={h}; r={r}; g={g}; b={b}]")
    s = pygame.Surface((w, h)).convert_alpha()
    s.fill((r, g, b))
    return s

@dispatch(float, float, float, float, float, float)
def image(w: float, h: float, r: float, g: float, b: float, a: float=255) -> pygame.Surface:
    debug(f"[ IMAGE ] Creating Image With Surface Properties:[w={w}; h={h}; r={r}; g={g}; b={b}; a={a}]")
    s = pygame.Surface((w, h)).convert_alpha()
    s.fill((r, g, b, a))
    return s



from ..sprite.animation.base import AnimSelector, FrameGroup, Frame
@dispatch((Element, _Element))
def animation(xmlData: Element | _Element) -> AnimSelector:
    def getAnimName(origName: str) -> str:
        startCount = False
        for i in range(len(origName) - 1, 0, -1):
            if origName[i].isdigit():
                startCount = True
            if origName[i].isalpha() and startCount:
                return origName[:i + 1]
        return origName

    img: pygame.Surface = image(xmlData.attrib['imagePath'], 'animations')

    cur: FrameGroup | None = None
    group: AnimSelector = AnimSelector()
    curName: str = ""

    debug("[ ANIMATION ] Creating Frames")
    for sprite in xmlData:
        nameR = sprite.get('name')
        if not exists(nameR): continue
        name: str = getAnimName(nameR)

        debug("Creating FrameGroup:", name)

        if curName != name:
            if exists(cur):
                group[curName] = cur
            curName = name
            cur = FrameGroup()

        x, y, w, h = map(lambda v: int(sprite.get(v)), ['x', 'y', 'width', 'height'])

        x, y = min(x, img.width), min(y, img.height)
        frame = img.subsurface(x, y, w, h)

        offX, offY = map(lambda v: int(sprite.get(v)), ['frameX', 'frameY'])
        cur.add(Frame(frame, pygame.Vector2(offX, offY)))
    group[curName] = cur

    group.Selected = list(group.keys())[0] if len(group.keys()) > 0 else ""
    group.Index = 0

    return group

@dispatch(dict)  # JSON - ASEPRITE
def animation(jsonData: dict) -> AnimSelector:
    from typing import Generator
    img: pygame.Surface = image(jsonData['meta']['image'], 'animations')
    anim: FrameGroup | None = None
    group: AnimSelector = AnimSelector()
    curName: str = ""

    def yieldJS(obj: list | dict) -> Generator[tuple[str, any], None, None]:
        if isinstance(obj, dict):
            for key, value in obj.items():
                yield key, value
        if isinstance(obj, list):
            for item in obj:
                yield item['filename'], item
        raise NotImplementedError("Only supports LIST and DICT")

    for name, sprite in yieldJS(jsonData['frames']):
        if name != curName:
            if exists(curName):
                group[name] = anim
            anim = FrameGroup()

        x, y, w, h = map(lambda v: int(sprite.get(v)), 'x y w h'.split())
        x, y = min(x, img.width), min(y, img.height)
        frame = img.subsurface(x, y, w, h)

        anim.add(Frame(frame, pygame.Vector2(0, 0)))
    group[curName] = anim
    group.Selected = list(group.keys())[0] if len(group.keys()) > 0 else ""
    group.Index = 0

    return group

@dispatch(str)
def animation(path: str) -> AnimSelector:
    if not pathExists(path):
        raise FileNotFoundError(path)

    if path.endswith('.xml'):
        return animation(xml(path))
    elif path.endswith('.json'):
        return animation(json(path))
    else:
        raise NotImplementedError("Only supports XML and JSON! NOT: '" + path.split('.')[-1] + "'")

@dispatch(str, str)
def animation(file: str, folder: str = 'animation') -> AnimSelector:
    from .file import File
    path = File.animation(file, folder)
    return animation(path)

"""
FONTS
"""
@dispatch(pygame.freetype.Font)
def font(f: pygame.freetype.Font) -> dict[str, pygame.Surface]:
    return font(f.path)

from types import NoneType
@dispatch((str, NoneType))
def font(path: str | None) -> dict[str, pygame.Surface]:
    import string
    data = {}
    if path is None:
        raise FileNotFoundError("Path is required")
    try:
        f = pygame.freetype.Font(path, 256)
    except FileNotFoundError:
        f = pygame.freetype.SysFont('Arial', 256)
    f.antialiased = False

    for char in string.printable:
        data[char] = f.render(char, (255, 255, 255))[0]

    return data

@dispatch(str, str)
def font(file: str, folder: str = 'font') -> dict[str, pygame.Surface]:
    from .file import File
    path = File.font(file, folder)
    return font(path)
