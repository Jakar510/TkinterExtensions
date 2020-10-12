# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

from TkinterExtensions.Widgets.Style import *
from TkinterExtensions.Widgets.base import *




__all__ = ['Root', 'TopLevel']

# noinspection PyUnresolvedReferences
class _roorMixin:
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

# noinspection DuplicatedCode
class Root(tk.Tk, _roorMixin):
    def __init__(self, Screen_Width: int = None, Screen_Height: int = None, x: int = 0, y: int = 0, fullscreen: bool = None, **kwargs):
        super().__init__(**kwargs)
        self.SetDimmensions(Screen_Width, Screen_Height, x, y)
        if fullscreen is not None: self.SetFullScreen(fullscreen)

        self.Style = Style(master=self)



# noinspection DuplicatedCode
class TopLevel(tk.Toplevel, _roorMixin):
    def __init__(self, master: Root, Screen_Width: int = None, Screen_Height: int = None, x: int = 0, y: int = 0, fullscreen: bool = None, **kwargs):
        assert (isinstance(master, Root))
        super().__init__(master=master, **kwargs)
        self.SetDimmensions(Screen_Width, Screen_Height, x, y)
        if fullscreen is not None: self.SetFullScreen(fullscreen)

        self.Style = master.Style
