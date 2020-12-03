# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

from .BaseWidgets import *
from .Frames import *
from .KeyBoard import *
from .Root import *
from .Widgets import *
from .base import *




__all__ = [
        'TitledEntry', 'TitledKeyboardEntry', 'FramedKeyboardEntry', 'FramedEntry', 'KeyboardEntry'
        ]

class KeyboardEntry(Entry, KeyboardMixin):
    def __init__(self, master, *, root: tkRoot, placement: PlacementSet = PlacementSet(Placement.Auto), keysize: int = None, keycolor: str = None,
                 insertbackground: str = 'red', insertborderwidth: int = 3, insertofftime: int = 1, insertontime: int = 1, insertwidth: int = 3,
                 text: str = '', Override_var: tk.StringVar = None, Color: dict = None, **kwargs):
        Entry.__init__(self, master, text=text, Override_var=Override_var, Color=Color,
                       insertbackground=insertbackground, insertborderwidth=insertborderwidth, insertofftime=insertofftime, insertontime=insertontime, insertwidth=insertwidth,
                       **kwargs)
        KeyboardMixin.__init__(self, master, root=root, placement=placement, keysize=keysize, keycolor=keycolor)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))



class TitledEntry(Frame):
    def __init__(self, master, *, RowPadding: int = 1, factor: int = 3, entry: dict = {}, title: dict = {}, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.Grid_RowConfigure(0, weight=1).Grid_RowConfigure(1, weight=factor).Grid_ColumnConfigure(0, weight=1)

        self.Title = Label(self, **title).Grid(row=0, column=0, padx=RowPadding, pady=RowPadding)
        self.Entry = Entry(master=self, **entry).Grid(row=1, column=0, padx=RowPadding, pady=RowPadding)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

    @property
    def title(self) -> str: return self.Title.txt
    @title.setter
    def title(self, value: str): self.Title.txt = value

    @property
    def value(self) -> str: return self.Entry.txt
    @value.setter
    def value(self, value: str): self.Entry.txt = value



class TitledKeyboardEntry(Frame):
    def __init__(self, master, *, root: tkRoot, entry: dict = {}, title: dict = {}, RowPadding: int = 1, factor: int = 3, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.Grid_RowConfigure(0, weight=1).Grid_RowConfigure(1, weight=factor).Grid_ColumnConfigure(0, weight=1)

        self.Title = Label(self, **title).Grid(row=0, column=0, padx=RowPadding, pady=RowPadding)
        self.Entry = KeyboardEntry(master=self, root=root, **entry).Grid(row=1, column=0, padx=RowPadding, pady=RowPadding)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

    @property
    def title(self) -> str: return self.Title.txt
    @title.setter
    def title(self, value: str): self.Title.txt = value

    @property
    def value(self) -> str: return self.Entry.txt
    @value.setter
    def value(self, value: str): self.Entry.txt = value



class FramedKeyboardEntry(LabelFrame):
    def __init__(self, master, *, root: tkRoot, entry: dict = {}, **kwargs):
        LabelFrame.__init__(self, master, **kwargs)

        self.Entry = KeyboardEntry(master=self, root=root, **entry).PlaceFull()

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

    @property
    def title(self) -> str: return self.txt
    @title.setter
    def title(self, value: str): self.txt = value

    @property
    def value(self) -> str: return self.Entry.txt
    @value.setter
    def value(self, value: str): self.Entry.txt = value


class FramedEntry(LabelFrame):
    def __init__(self, master, *, entry: dict = {}, **kwargs):
        LabelFrame.__init__(self, master, **kwargs)

        self.Entry = Entry(master=self, **entry).PlaceFull()

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

    @property
    def title(self) -> str: return self.txt
    @title.setter
    def title(self, value: str): self.txt = value

    @property
    def value(self) -> str: return self.Entry.txt
    @value.setter
    def value(self, value: str): self.Entry.txt = value
