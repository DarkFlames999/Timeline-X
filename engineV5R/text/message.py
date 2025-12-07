from __future__ import annotations, division
from ..types import FONT_CHAR_FUNC
import pygame

__all__ = [
    'Message',
    'MessageGroup'
]


class Message(pygame.Color):
    def __init__(self, text: str, color: pygame.typing.ColorLike, charFunc: FONT_CHAR_FUNC = None):
        super().__init__(color)
        self.Text = text
        self.CharFunc: FONT_CHAR_FUNC | None = charFunc


    def __add__(self, other: str | Message) -> Message | MessageGroup:
        if isinstance(other, str):
            return Message(self.Text + other, self)
        elif isinstance(other, Message):
            return MessageGroup(self, other)
        raise TypeError(type(other), 'Not a Valid Type for Message Adding')

    def __radd__(self, other: str | Message) -> Message | MessageGroup:
        if isinstance(other, str):
            return Message(other + self.Text, self)
        elif isinstance(other, Message):
            return MessageGroup(other, self)
        raise TypeError(type(other), 'Not a Valid Type for Message Adding')

    def __iadd__(self, other: str) -> Message:
        if isinstance(other, str):
            self.Text += other
            return self
        raise TypeError(type(other), 'Not a Valid Type for Message InPlaceAdding')

    def __mul__(self, other: int) -> Message:
        if not isinstance(other, int): raise TypeError(type(other), 'Not a Valid Type for Message Multiplication')
        return Message(self.Text * other, self)

    def __rmul__(self, other: int) -> Message:
        if not isinstance(other, int): raise TypeError(type(other), 'Not a Valid Type for Message Multiplication')
        return Message(self.Text * other, self)

    def __imul__(self, other: int) -> Message:
        if isinstance(other, int):
            self.Text *= other
            return self
        raise TypeError(type(other), 'Not a Valid Type for Message InPlaceMultiplication')

    def __str__(self):
        return self.Text

class MessageGroup(list[Message]):
    def __init__(self, *msg: Message):
        super().__init__(msg)

    def __add__(self, other: str | Message | MessageGroup) -> MessageGroup:
        if isinstance(other, str):
            a = MessageGroup(*self)
            a[len(a)-1].Text += other
            return a
        elif isinstance(other, Message):
            return MessageGroup(*self, other)
        elif isinstance(other, MessageGroup):
            return MessageGroup(*self, *other)
        raise TypeError(type(other), 'Not a Valid Type for MessageGroup Adding')

    def __radd__(self, other: str | Message | MessageGroup) -> MessageGroup:
        if isinstance(other, str):
            a = MessageGroup(*self)
            a[len(a)-1].Text = other + a[len(a)-1].Text
            return a
        elif isinstance(other, Message):
            return MessageGroup(other, *self)
        elif isinstance(other, MessageGroup):
            return MessageGroup(*other, *self)
        raise TypeError(type(other), 'Not a Valid Type for MessageGroup Adding')

    def __iadd__(self, other: str | Message | MessageGroup) -> MessageGroup:
        if not isinstance(other, str | Message | MessageGroup): raise TypeError(type(other),
                                                                                'Not a Valid Type for Message Adding')
        if isinstance(other, str):
            self[len(self)-1].Text += other
        elif isinstance(other, Message):
            self.append(other)
        elif isinstance(other, MessageGroup):
            self.extend(other)
        return self

    def __mul__(self, other: int) -> MessageGroup:
        if not isinstance(other, int): raise TypeError(type(other), 'Not a Valid Type for MessageGroup Multiplication')
        a = MessageGroup()
        for m in range(other):
            a.extend(self)
        return a

    def __rmul__(self, other: int) -> MessageGroup:
        if not isinstance(other, int): raise TypeError(type(other), 'Not a Valid Type for MessageGroup Multiplication')
        return self * other

    def __imul__(self, other: int) -> MessageGroup:
        if not isinstance(other, int): raise TypeError(type(other), 'Not a Valid Type for MessageGroup Multiplication')
        cur = MessageGroup(*self)
        for _ in range(other):
            self.extend(cur)
        return self
