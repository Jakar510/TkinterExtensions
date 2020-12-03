# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------

from enum import Enum
from typing import Union

from ..Widgets.BaseWidgets import *
from ..Widgets.base import *




__all__ = [
        'Frame', 'LabelFrame',
        'FrameThemed', 'LabelFrameThemed',
        'FrameTypes',
        ]

class BaseFrameMixin:
    InstanceID: Union[str, int, Enum] = None

    def SetID(self, InstanceID: Union[str, int, Enum]):
        self.InstanceID = InstanceID
        return self

    @property
    def __name__(self):
        try: base = super().__name__()
        except AttributeError: base = self.__class__.__name__

        if self.InstanceID:
            if isinstance(self.InstanceID, Enum): InstanceID = self.InstanceID.value
            else: InstanceID = self.InstanceID

            return f'{base}_{InstanceID}'.lower()

        return base


# noinspection DuplicatedCode
class Frame(OptionsMixin, tk.Frame, BaseTkinterWidget, BaseFrameMixin):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master=master, **kwargs)





class LabelFrame(OptionsMixin, tk.LabelFrame, BaseTextTkinterWidget, BaseFrameMixin):
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
    def __init__(self, master, text: str = '', **kwargs):
        tk.LabelFrame.__init__(self, master=master, text=text, **kwargs)
        BaseTextTkinterWidget.__init__(self, text=text, configure=False)

    @property
    def txt(self) -> str: return self._txt.get()
    @txt.setter
    def txt(self, value: str):
        self._txt.set(value)
        self.configure(text=value)






# noinspection DuplicatedCode
class FrameThemed(OptionsMixin, ttk.Frame, BaseTkinterWidget, BaseFrameMixin):
    def __init__(self, master, **kwargs):
        ttk.Frame.__init__(self, master=master, **kwargs)





class LabelFrameThemed(OptionsMixin, ttk.LabelFrame, BaseTextTkinterWidget, BaseFrameMixin):
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
    def __init__(self, master, text: str = '', **kwargs):
        ttk.LabelFrame.__init__(self, master=master, text=text, **kwargs)
        BaseTextTkinterWidget.__init__(self, text=text, configure=False)

    @property
    def txt(self) -> str: return self._txt.get()
    @txt.setter
    def txt(self, value: str):
        self._txt.set(value)
        self.configure(text=value)





FrameTypes = Union[Frame, LabelFrame, FrameThemed, LabelFrameThemed]
