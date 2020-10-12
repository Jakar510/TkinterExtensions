# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------


import pprint
from tkinter import Event as tkEvent




__all__ = ['TkinterEvent']

class TkinterEvent(tkEvent):
    __slots__ = ['serial', 'num', 'height', 'keycode', 'state', 'time', 'width', 'x', 'y', 'char', 'keysym', 'keysym_num', 'type', 'widget', 'x_root', 'y_root', 'delta']
    def __init__(self, source: tkEvent = None):
        super().__init__()
        if source is not None:
            assert (isinstance(source, tkEvent))
            for name, value in source.__dict__.items():
                setattr(self, name, value)

    def __str__(self) -> str: return self.ToString()
    def __repr__(self) -> str: return self.ToString()

    def ToString(self) -> str: return f'<{self.__class__.__name__} Object. State: \n{pprint.pformat(self.ToDict(), indent=4)} >'
    def ToDict(self) -> dict:
        """
            {
                'num': self.num,
                'height': self.height,
                'width': self.width,
                '_widget': self._widget,
                'keysym': self.keysym,
                'keycode': self.keycode,
                'keysym_num': self.keysym_num,
                'state': self.state,
                'time': self.time,
                'x': self.x,
                'y': self.y,
                'char': self.char,
                'type': self.type,
                'x_root': self.x_root,
                'y_root': self.y_root,
                'delta': self.delta,
            }
        :return:
        """
        return self.__dict__

    @staticmethod
    def IsValid(o: str):
        if isinstance(o, str): return o != '??'

        raise TypeError(f'expected str, got {type(o)}')
