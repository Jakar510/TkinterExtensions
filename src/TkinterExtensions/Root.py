# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

from .Sytle import *
from .base import *




__all__ = ['TkinterRoot', 'TkinterTopLevel']

# noinspection DuplicatedCode
class TkinterRoot(tk.Tk):
    Style: TkinterStyle
    Screen_Width: int
    Screen_Height: int
    def __init__(self, Screen_Width: int = None, Screen_Height: int = None, x: int = 0, y: int = 0, fullscreen: bool = None, **kwargs):
        super().__init__(**kwargs)
        self.SetDimmensions(Screen_Width, Screen_Height, x, y)
        if fullscreen is not None: self.SetFullScreen(fullscreen)

        self.Style = TkinterStyle(master=self)

    def SetDimmensions(self, Screen_Width: int = None, Screen_Height: int = None, x: int = 0, y: int = 0):
        self.Screen_Width = Screen_Width or int(self.winfo_screenwidth())
        self.Screen_Height = Screen_Height or int(self.winfo_screenheight())
        self.geometry(self.Dimmensions(x, y))
    def Dimmensions(self, x: int = 0, y: int = 0) -> str: return f"{self.Screen_Width}x{self.Screen_Height}+{x}+{y}"

    def HideCursor(self): self.config(cursor="none")

    def SetFullScreen(self, fullscreen: bool = False, ): self.attributes('-fullscreen', fullscreen)
    def SetTitle(self, title: str): self.title(title)
    def SetResizable(self, resizable: bool): self.resizable(width=resizable, height=resizable)



# noinspection DuplicatedCode
class TkinterTopLevel(tk.Toplevel):
    Style: TkinterStyle
    Screen_Width: int
    Screen_Height: int
    def __init__(self, Screen_Width: int = None, Screen_Height: int = None, x: int = 0, y: int = 0, fullscreen: bool = None, **kwargs):
        super().__init__(**kwargs)
        self.SetDimmensions(Screen_Width, Screen_Height, x, y)
        if fullscreen is not None: self.SetFullScreen(fullscreen)

        self.Style = TkinterStyle(master=self)

    def SetDimmensions(self, Screen_Width: int = None, Screen_Height: int = None, x: int = 0, y: int = 0):
        self.Screen_Width = Screen_Width or int(self.winfo_screenwidth())
        self.Screen_Height = Screen_Height or int(self.winfo_screenheight())
        self.geometry(self.Dimmensions(x, y))
    def Dimmensions(self, x: int = 0, y: int = 0) -> str: return f"{self.Screen_Width}x{self.Screen_Height}+{x}+{y}"

    def HideCursor(self): self.config(cursor="none")

    def SetFullScreen(self, fullscreen: bool = False, ): self.attributes('-fullscreen', fullscreen)
    def SetTitle(self, title: str): self.title(title)
    def SetResizable(self, resizable: bool): self.resizable(width=resizable, height=resizable)
