# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

from enum import Enum
from typing import Union

from .BaseApp import BaseApp
from ..Widgets.BaseWidgets import *
from ..Widgets.base import *




__all__ = ['Frame', 'LabelFrame']

class Frame(tk.Frame, BaseTkinterWidget):
    def __init__(self, master, app: BaseApp = None, **kwargs):
        tk.Frame.__init__(self, master=master, **kwargs)
        self.app = app

    def __name__(self, InstanceID: Union[str, int, Enum]):
        if isinstance(InstanceID, Enum): InstanceID = InstanceID.value

        return f'{self.__class__.__name__}_{InstanceID}'.lower()

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)


class LabelFrame(tk.LabelFrame, BaseTextTkinterWidget):
    """Construct a labelframe _widget with the master MASTER.

    STANDARD OPTIONS

        borderwidth, cursor, font, foreground,
        highlightbackground, highlightcolor,
        highlightthickness, padx, pady, relief,
        takefocus, text

    WIDGET-SPECIFIC OPTIONS

        background, class, colormap, container,
        height, labelanchor, labelwidget,
        visual, width
    """
    def __init__(self, master, app: BaseApp = None, text: str = '', **kwargs):
        tk.LabelFrame.__init__(self, master=master, text=text, **kwargs)
        BaseTextTkinterWidget.__init__(self, text=text, configure=False)
        self.app = app

    @property
    def txt(self) -> str: return self._txt.get()
    @txt.setter
    def txt(self, value: str):
        self._txt.set(value)
        self.configure(text=value)


    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)
