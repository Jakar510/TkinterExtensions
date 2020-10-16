# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------
from enum import Enum

from ..Widgets.Style import *
from ..Widgets.base import *




__all__ = ['Root', 'TopLevel']

# noinspection PyUnresolvedReferences
class _rootMixin:
    Style: Style
    Screen_Width: int
    Screen_Height: int
    def SetDimmensions(self, Screen_Width: int = None, Screen_Height: int = None, x: int = 0, y: int = 0):
        self.Screen_Width = Screen_Width or int(self.winfo_screenwidth())
        self.Screen_Height = Screen_Height or int(self.winfo_screenheight())
        self.geometry(self.Dimmensions(x, y))
    def Dimmensions(self, x: int = 0, y: int = 0) -> str: return f"{self.Screen_Width}x{self.Screen_Height}+{x}+{y}"

    def HideCursor(self):
        self.config(cursor="none")
        return self

    def SetFullScreen(self, fullscreen: bool = False, ):
        self.attributes('-fullscreen', fullscreen)
        return self
    def SetTitle(self, title: str):
        self.title(title)
        return self
    def SetResizable(self, resizable: bool):
        self.resizable(width=resizable, height=resizable)
        return self

    def Bind(self, sequence: str or Enum = None, func: callable = None, add: bool = None):
        if isinstance(sequence, Enum): sequence = sequence.value
        return self.bind(sequence, func, add)

    @property
    def width(self) -> int: return self.winfo_width()
    @property
    def height(self) -> int: return self.winfo_height()
# noinspection DuplicatedCode
class Root(tk.Tk, _rootMixin):
    def __init__(self, Screen_Width: int = None, Screen_Height: int = None, x: int = 0, y: int = 0, fullscreen: bool = None, **kwargs):
        super().__init__(**kwargs)
        self.SetDimmensions(Screen_Width, Screen_Height, x, y)
        if fullscreen is not None: self.SetFullScreen(fullscreen)

        self.Style = Style(master=self)

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)


# noinspection DuplicatedCode
class TopLevel(tk.Toplevel, _rootMixin):
    def __init__(self, master: Root, Screen_Width: int = None, Screen_Height: int = None, x: int = 0, y: int = 0, fullscreen: bool = None, **kwargs):
        assert (isinstance(master, Root))
        super().__init__(master=master, **kwargs)
        self.SetDimmensions(Screen_Width, Screen_Height, x, y)
        if fullscreen is not None: self.SetFullScreen(fullscreen)

        self.Style = master.Style

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)
