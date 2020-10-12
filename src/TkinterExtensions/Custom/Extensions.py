# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------
from abc import ABC
from typing import Dict

from TkinterExtensions.Widgets.Frames import *
from TkinterExtensions.Widgets.Widgets import *




__all__ = [
        'ButtonGrid',
        ]

class ButtonGrid(TkinterFrame, ABC):
    __buttons: Dict[int, Button] = { }
    def __init__(self, *, master: TkinterFrame, rows: int = None, cols: int = None, NumberOfButtons: int = None, **kwargs):
        """
            :param kwargs: Button kwargs
        """
        assert (isinstance(master, TkinterFrame))
        TkinterFrame.__init__(self, master=master)
        self._rows = rows or len(self.ButtonTitles)
        self._cols = cols or 1
        self._NumberOfButtons = NumberOfButtons or self._rows * self._cols

        if len(self.ButtonCommands) != self._NumberOfButtons:
            raise ValueError(f"len(self.ButtonCommands) [ {len(self.ButtonCommands)} ]  does not Match self._NumberOfButtons [ {self._NumberOfButtons} ]")
        if len(self.ButtonTitles) != self._NumberOfButtons:
            raise ValueError(f"len(self.ButtonTitles) [ {len(self.ButtonTitles)} ]  does not Match self._NumberOfButtons [ {self._NumberOfButtons} ]")

        self._MakeGrid(kwargs)
    def _MakeGrid(self, kwargs: dict):
        for r in range(self._rows): self.grid_rowconfigure(r, weight=1)
        for c in range(self._cols): self.grid_columnconfigure(c, weight=1)

        r = 0
        c = 0
        for i in range(self._NumberOfButtons):
            if c >= self._cols:
                r += 1
                c = 0
            self.__buttons[i] = Button(self, Text=self.ButtonTitles[i], **kwargs)
            self.__buttons[i].grid(row=r, column=c)
            self.__buttons[i].SetCommand(self.ButtonCommands[i])
            c += 1

    def HideAll(self):
        for w in self.__buttons.values(): w.hide()
    def ShowAll(self):
        for w in self.__buttons.values(): w.show()

    def UpdateText(self, Titles: dict = None):
        if Titles is None: Titles = self.ButtonTitles
        if len(Titles) != self._NumberOfButtons: raise ValueError("len(Titles) Doesn't Match NumberOfButtons")

        for i in range(self._NumberOfButtons):
            self.__buttons[i].txt = Titles[i]
    def UpdateCommands(self, commands: dict = { }, kwz: dict = { }, z: dict = { }):
        if len(commands) != self._NumberOfButtons: raise ValueError("len(commands) Doesn't Match NumberOfButtons")

        for i, Command in commands.items():
            widget = self.__buttons[i]
            if i in kwz and kwz[i] is not None and Command:
                widget.cmd = lambda x=kwz[i]: Command(**x)
                widget.configure(command=widget.cmd)
            elif i in z and z[i] is not None and Command:
                widget.cmd = lambda x=z[i]: Command(x)
                widget.configure(command=widget.cmd)
            elif Command:
                widget.configure(command=Command)

    @property
    def ButtonTitles(self) -> dict: raise NotImplementedError()
    @property
    def ButtonCommands(self) -> dict: raise NotImplementedError()
