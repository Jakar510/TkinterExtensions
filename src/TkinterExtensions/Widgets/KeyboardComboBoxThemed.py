# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

from typing import *

from .BaseWidgets import *
from .KeyBoard import *
from .Root import *
from .Themed import *
from .base import *
from ..Events import *




__all__ = [
        'KeyboardComboBoxThemed', 'TitledKeyboardComboBoxThemed', 'TitledComboBoxThemed', 'FramedKeyboardComboBoxThemed', 'FramedComboBoxThemed'
        ]

class KeyboardComboBoxThemed(ComboBoxThemed, KeyboardMixin):
    def __init__(self, master, *, root: tkRoot, placement: PlacementSet = PlacementSet(Placement.Auto), keysize: int = None, keycolor: str = None,
                 text: str = '', Override_var: tk.StringVar = None, Color: Dict = None, **kwargs):
        ComboBoxThemed.__init__(self, master, text=text, Override_var=Override_var, Color=Color, postcommand=self._OnDropDown, **kwargs)
        KeyboardMixin.__init__(self, master, root=root, placement=placement, keysize=keysize, keycolor=keycolor)
        self.Bind(Bindings.ComboboxSelected, self._OnSelect)

    def _options(self, cnf, kwargs=None) -> Dict: return super()._options(cnf, BaseTkinterWidget.convert_kwargs(kwargs))

    def _OnDropDown(self):
        """ By default, destroys the popup when the dropdown list is expanded. Override to add functionality """
        self.destroy_popup()

    # noinspection PyUnusedLocal
    def _OnSelect(self, event: tkEvent = None):
        """ By default, destroys the popup when a item is selected. Override to add functionality """
        self.destroy_popup()





class TitledComboBoxThemed(BaseTitled):
    def __init__(self, master, *, RowPadding: int = 1, factor: int = 3, value: Dict = { }, title: Dict = { }, cls: Type[ComboBoxThemed] = ComboBoxThemed, **kwargs):
        assert (issubclass(cls, ComboBoxThemed))
        BaseTitled.__init__(self, master, cls=cls, value=value, RowPadding=RowPadding, title=title, factor=factor, **kwargs)





class TitledKeyboardComboBoxThemed(BaseTitledKeyboard):
    def __init__(self, master, *, root: tkRoot, RowPadding: int = 1, factor: int = 3, value: Dict = { }, title: Dict = { },
                 cls: Type[KeyboardComboBoxThemed] = KeyboardComboBoxThemed, **kwargs):
        assert (issubclass(cls, KeyboardComboBoxThemed))
        BaseTitledKeyboard.__init__(self, master, cls=cls, root=root, value=value, RowPadding=RowPadding, title=title, factor=factor, **kwargs)





class FramedComboBoxThemed(BaseFramed):
    def __init__(self, master, *, value: Dict = { }, cls: Type[ComboBoxThemed] = ComboBoxThemed, **kwargs):
        assert (issubclass(cls, ComboBoxThemed))
        BaseFramed.__init__(self, master, cls=cls, value=value, **kwargs)





class FramedKeyboardComboBoxThemed(BaseFramedKeyboard):
    def __init__(self, master, *, root: tkRoot, value: Dict = { }, cls: Type[KeyboardComboBoxThemed] = KeyboardComboBoxThemed, **kwargs):
        assert (issubclass(cls, KeyboardComboBoxThemed))
        BaseFramedKeyboard.__init__(self, master, cls=cls, root=root, value=value, **kwargs)
