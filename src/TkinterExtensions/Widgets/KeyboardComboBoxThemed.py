# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------


from .BaseWidgets import *
from .Frames import *
from .KeyBoard import *
from .Root import *
from .Themed import *
from .Widgets import *
from .base import *




__all__ = [
        'KeyboardComboBoxThemed', 'TitledKeyboardComboBoxThemed', 'TitledComboBoxThemed', 'FramedKeyboardComboBoxThemed', 'FramedComboBoxThemed'
        ]

class KeyboardComboBoxThemed(ComboBoxThemed, KeyboardMixin):
    def __init__(self, master, *, root: tkRoot, placement: PlacementSet = PlacementSet(Placement.Auto), keysize: int = None, keycolor: str = None,
                 text: str = '', Override_var: tk.StringVar = None, Color: dict = None, **kwargs):
        ComboBoxThemed.__init__(self, master, text=text, Override_var=Override_var, Color=Color, postcommand=self._OnDropDown, **kwargs)
        KeyboardMixin.__init__(self, master, root=root, placement=placement, keysize=keysize, keycolor=keycolor)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

    def _OnDropDown(self): self.destroy_popup()



class TitledComboBoxThemed(Frame):
    def __init__(self, master, *, RowPadding: int = 1, factor: int = 3, comobobox: dict = {}, title: dict = {}, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.Grid_RowConfigure(0, weight=1).Grid_RowConfigure(1, weight=factor).Grid_ColumnConfigure(0, weight=1)

        self.Title = Label(self, **title).Grid(row=0, column=0, padx=RowPadding, pady=RowPadding)
        self.cb = ComboBoxThemed(master=self, **comobobox).Grid(row=1, column=0, padx=RowPadding, pady=RowPadding)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

    @property
    def title(self) -> str: return self.Title.txt
    @title.setter
    def title(self, value: str): self.Title.txt = value

    @property
    def value(self) -> str: return self.cb.txt
    @value.setter
    def value(self, value: str): self.cb.txt = value



class TitledKeyboardComboBoxThemed(Frame):
    def __init__(self, master, *, root: tkRoot, RowPadding: int = 1, factor: int = 3, comobobox: dict = {}, title: dict = {}, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.Grid_RowConfigure(0, weight=1).Grid_RowConfigure(1, weight=factor).Grid_ColumnConfigure(0, weight=1)

        self.Title = Label(self, **title).Grid(row=0, column=0, padx=RowPadding, pady=RowPadding)
        self.cb = KeyboardComboBoxThemed(master=self, root=root, **comobobox).Grid(row=1, column=0, padx=RowPadding, pady=RowPadding)

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

    @property
    def title(self) -> str: return self.Title.txt
    @title.setter
    def title(self, value: str): self.Title.txt = value

    @property
    def value(self) -> str: return self.cb.txt
    @value.setter
    def value(self, value: str): self.cb.txt = value



class FramedComboBoxThemed(LabelFrame):
    def __init__(self, master, *, comobobox: dict = {}, **kwargs):
        LabelFrame.__init__(self, master, **kwargs)

        self.cb = ComboBoxThemed(master=self, **comobobox).PlaceFull()

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

    @property
    def title(self) -> str: return self.txt
    @title.setter
    def title(self, value: str): self.txt = value

    @property
    def value(self) -> str: return self.cb.txt
    @value.setter
    def value(self, value: str): self.cb.txt = value



class FramedKeyboardComboBoxThemed(LabelFrame):
    def __init__(self, master, *, root: tkRoot, comobobox: dict = {}, **kwargs):
        LabelFrame.__init__(self, master, **kwargs)

        self.cb = KeyboardComboBoxThemed(master=self, root=root, **comobobox).PlaceFull()

    def _options(self, cnf, kwargs=None) -> dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

    @property
    def title(self) -> str: return self.txt
    @title.setter
    def title(self, value: str): self.txt = value

    @property
    def value(self) -> str: return self.cb.txt
    @value.setter
    def value(self, value: str): self.cb.txt = value


