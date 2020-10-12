# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

from enum import Enum
from typing import Union

from .base import *
from .BaseWidgets import *




__all__ = ['TkinterFrame', 'TkinterLabelFrame']

class TkinterFrame(tk.Frame, BaseTkinterWidget):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master=master, **kwargs)

    def __name__(self, InstanceID: Union[str, int, Enum]):
        if isinstance(InstanceID, Enum): InstanceID = InstanceID.value

        return f'{self.__class__.__name__}_{InstanceID}'.lower()
class TkinterLabelFrame(tk.LabelFrame, BaseTextTkinterWidget):
    """Construct a labelframe _widget with the parent MASTER.

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
    def __init__(self, master, Text: str = '', **kwargs):
        if 'text' in kwargs: Text = kwargs.pop('text') or Text
        if 'v' in kwargs: Text = kwargs.pop('v') or Text
        tk.LabelFrame.__init__(self, master=master, text=Text, **kwargs)
        BaseTextTkinterWidget.__init__(self, Override_var=None, Text=Text, configure=False)

    @property
    def txt(self) -> str: return self._txt.get()
    @txt.setter
    def txt(self, value: str):
        self._txt.set(value)
        self.configure(text=value)
