partialKey = int | str
fullKey = partialKey | tuple | list

def partialParse(kType: AnyKeys | AllKeys, *keys: fullKey) -> AnyKeys | AllKeys: ...
def parseKeys(*keys: fullKey): ...


class AnyKeys(list):
    """
    Key Parser\n
    if (any) keys pressed
    """

    def __init__(self, *keys: fullKey): ...

class AllKeys(list):
    """
    Key Parser\n
    if (all) keys pressed
    """

    def __init__(self, *keys: fullKey): ...
