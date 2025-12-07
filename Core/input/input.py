from Game_Engine.game_tree import BaseManager
from .keyboard import Keyboard
from .mouse import Mouse

class InputManager(BaseManager):
    def __init__(self):
        self.Keyboard = Keyboard()
        self.Mouse = Mouse()
        super().__init__("Input Manager", "INP_MG")

    @property
    def LMB(self):
        return self.Mouse.LMB

    @property
    def RMB(self):
        return self.Mouse.RMB

    @property
    def MMB(self):
        return self.Mouse.MMB

    @property
    def MousePos(self):
        return self.Mouse.Pos

    @MousePos.setter
    def MousePos(self, value):
        self.Mouse.Pos = value

    @property
    def DesktopPos(self):
        return self.Mouse.DesktopPos

    @property
    def MouseDelta(self):
        return self.Mouse.Delta

    def __getitem__(self, item):
        match item:
            case 'LMB':
                return self.LMB
            case 'RMB':
                return self.RMB
            case 'MMB':
                return self.MMB
            case 'SideB1':
                return self.Mouse.SideB1
            case 'SideB2':
                return self.Mouse.SideB2
            case _:
                return self.Keyboard[item]

    def update(self, dt):
        self.Keyboard.update(dt)
        self.Mouse.update(dt)

