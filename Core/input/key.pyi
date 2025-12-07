from dataclasses import dataclass

@dataclass
class Key:
    """
    KeyData For Key Presses
    """

    Pressed: bool = False
    Held: bool = False
    Released: bool = False

    HoldTime: float = 0
    LastHoldTime: float = 0

    TotalPressCount: int = 0
    SinceLastPress: float = 0
    SinceReleased: float = 0

    def update(self, dt: float):
        """
        Updates the Key State
        """
        ...

