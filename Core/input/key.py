from dataclasses import dataclass

@dataclass
class Key:
    Pressed = False
    Held = False
    Released = False

    HoldTime = 0
    LastHoldTime = 0

    TotalPressCount = 0
    SinceLastPress = 0
    SinceReleased = 0

    def update(self, dt):
        self.SinceLastPress += dt
        self.SinceReleased += dt

        if self.Pressed:
            self.TotalPressCount += 1
            self.SinceLastPress = 0
            self.SinceReleased = 0

        if self.Held:
            self.HoldTime += dt
            self.SinceReleased = 0

        if self.Released:
            self.LastHoldTime = self.HoldTime
            self.HoldTime = 0