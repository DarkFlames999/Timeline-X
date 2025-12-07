def partialParse(kType, *keys):
    for k in keys[1:]:
        if isinstance(k, list|tuple):
            kType.append(parseKeys(*k))
        else:
            kType.append(k)
    return kType

def parseKeys(*keys):
    kType = AnyKeys()
    keys = list(keys)
    if keys[0] != all and keys[0] != any:
        keys.insert(0, any)
    if keys[0] == all:
        kType = AllKeys()
    return partialParse(kType, *keys)

class AnyKeys(list):
    def __init__(self, *keys):
        super().__init__()
        partialParse(self, any, *keys)


class AllKeys(list):
    def __init__(self, *keys):
        super().__init__()
        partialParse(self, all, *keys)