# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------


import base64
import io
import os
from enum import Enum
from typing import Union
from urllib.request import urlopen

from PIL import Image, ImageTk

from ..Misc.Enumerations import *
from ..Misc.Helpers import *
from ..Widgets.base import *




__all__ = ['BaseTkinterWidget', 'BaseTextTkinterWidget', 'Image', 'ImageTk',
           'CurrentValue', 'CallWrapper', 'CurrentValue', 'CommandMixin', 'ImageMixin']

class BaseTkinterWidget(tk.Widget):
    _state_: ViewState = ViewState.Hidden
    _pi: dict = { }
    _manager_: Layout = None
    _wrap: int = None

    @property
    def pi(self) -> dict: return self._pi.copy()

    @property
    def IsVisible(self) -> bool: return self._state_ != ViewState.Hidden

    @property
    def State(self) -> ViewState: return self._state_

    @property
    def width(self) -> int: return self.winfo_width()
    @property
    def height(self) -> int: return self.winfo_height()

    # noinspection PyUnresolvedReferences
    def show(self, **kwargs) -> bool:
        """
        Shows the current widget or _root_frame, based on the current geometry manager.
        Can be overridden to add additional functionality if needed.
        """
        if self._manager_ is None: return False

        state = kwargs.get('state', None) or kwargs.get('State', ViewState.Normal)
        assert (isinstance(state, ViewState))

        if self._manager_ == Layout.pack:
            self.pack(self._pi)
            return self._show(state)

        elif self._manager_ == Layout.grid:
            self.grid(self._pi)
            return self._show(state)

        elif self._manager_ == Layout.place:
            self.place(self._pi)
            return self._show(state)

        return False
    def _show(self, state: ViewState) -> bool:
        assert (isinstance(state, ViewState))
        self._SetState(state)
        return True

    # noinspection PyUnresolvedReferences
    def hide(self) -> bool:
        """
        Hides the current widget or _root_frame, based on the current geometry manager.
        Can be overridden to add additional functionality if needed.
        """
        if self._manager_ is None: return False
        if self._manager_ == Layout.pack:
            self.pack_forget()
            return self._hide()

        elif self._manager_ == Layout.grid:
            self.grid_forget()
            return self._hide()

        elif self._manager_ == Layout.place:
            self.place_forget()
            return self._hide()

        return False
    def _hide(self) -> bool:
        self._SetState(state=ViewState.Hidden)
        return True


    def Bind(self, sequence: str or Enum = None, func: callable = None, add: bool = None):
        if isinstance(sequence, Enum): sequence = sequence.value
        return self.bind(sequence, func, add)


    def Pack(self, cnf: dict = { }, **kwargs):
        self.pack(cnf, **kwargs)
        self._pi = self.pack_info()
        self._manager_ = Layout.pack
        return self
    def PackOptions(self, *, side: str or Side, fill: str or Fill, expand: bool, anchor: str or AnchorAndSticky = AnchorAndSticky.All, padx: int = 0, pady: int = 0, **kwargs):
        """Pack a widget in the master widget. Use as options:
        after=widget - pack it after you have packed widget
        anchor=NSEW (or subset) - position widget according to
                                  given direction
        before=widget - pack it before you will pack widget
        expand=bool - expand widget if master size grows
        fill=NONE or X or Y or BOTH - fill widget if widget grows
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in _x direction
        ipady=amount - add internal padding in _y direction
        padx=amount - add padding in _x direction
        pady=amount - add padding in _y direction
        side=TOP or BOTTOM or LEFT or RIGHT -  where to add this widget.
        """
        if 'after' in kwargs: assert (isinstance(kwargs['after'], tk.Widget))
        if 'before' in kwargs: assert (isinstance(kwargs['before'], tk.Widget))

        return self.Pack(side=side, anchor=anchor, expand=expand, fill=fill, padx=padx, pady=pady, **kwargs)
    def PackFull(self):
        """ Default placement in _root_frame occupying the full screen and/or space available in master. """
        return self.Pack(expand=True, fill=Fill.both, side=Side.top)


    def Place(self, cnf={ }, **kwargs):
        """Place a widget in the master widget. Use as options:
        in=master - master relative to which the widget is placed
        in_=master - see 'in' option description
        _x=amount - locate anchor of this widget at position _x of master
        _y=amount - locate anchor of this widget at position _y of master
        relx=amount - locate anchor of this widget between 0.0 and 1.0
                      relative to width of master (1.0 is right edge)
        rely=amount - locate anchor of this widget between 0.0 and 1.0
                      relative to height of master (1.0 is bottom edge)
        anchor=NSEW (or subset) - position anchor according to given direction
        width=amount - width of this widget in pixel
        height=amount - height of this widget in pixel
        relwidth=amount - width of this widget between 0.0 and 1.0
                          relative to width of master (1.0 is the same width
                          as the master)
        relheight=amount - height of this widget between 0.0 and 1.0
                           relative to height of master (1.0 is the same
                           height as the master)
        bordermode="inside" or "outside" - whether to take border width of
                                           master widget into account
        """
        self.place(cnf, **kwargs)
        self._pi = self.place_info()
        self._manager_ = Layout.place
        return self
    def PlaceAbsolute(self, x: float, y: float, width: float, height: float):
        return self.Place(x=x, y=y, width=width, height=height)
    def PlaceRelative(self, relx: float, rely: float, relwidth: float, relheight: float):
        return self.Place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    def PlaceFull(self):
        """ Default placement in _root_frame occupying the full screen and/or space available in master. """
        return self.PlaceRelative(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)


    def Grid(self, row: int, column: int, sticky: str or AnchorAndSticky = tk.NSEW, rowspan: int = 1, columnspan: int = 1, padx: int = 0, pady: int = 0, **kwargs):
        """Position a widget in the master widget in a grid. Use as options:
        column=number - use cell identified with given column (starting with 0)
        columnspan=number - this widget will span several columns
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in _x direction
        ipady=amount - add internal padding in _y direction
        padx=amount - add padding in _x direction
        pady=amount - add padding in _y direction
        row=number - use cell identified with given row (starting with 0)
        rowspan=number - this widget will span several rows
        sticky=NSEW - if cell is larger on which sides will this
                      widget stick to the cell boundary
        """
        self.grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=pady, **kwargs)
        self._pi = self.grid_info()
        self._manager_ = Layout.grid
        return self
    # noinspection PyMethodOverriding
    def Grid_Anchor(self, anchor: str or AnchorAndSticky):
        """The anchor value controls how to place the grid within the
        master when no row/column has any weight.

        The default anchor is nw."""
        self.grid_anchor(anchor=anchor)
        return self
    def Grid_RowConfigure(self, index: int, weight: int, **kwargs):
        """Configure row INDEX of a grid.

        Valid resources are minsize (minimum size of the row),
        weight (how much does additional space propagate to this row)
        and pad (how much space to let additionally)."""
        self.grid_rowconfigure(index, weight=weight, **kwargs)
        return self
    def Grid_ColumnConfigure(self, index: int, weight: int, **kwargs):
        """Configure column INDEX of a grid.

        Valid resources are minsize (minimum size of the column),
        weight (how much does additional space propagate to this column)
        and pad (how much space to let additionally)."""
        self.grid_columnconfigure(index, weight=weight, **kwargs)
        return self


    def SetActive(self, takeFocus: bool = True):
        """ Set the widget to Active Status """
        if takeFocus: self.focus_set()
        return self._SetState(state=ViewState.Active)

    def Disable(self):
        """ Disable the widget """
        return self._SetState(state=ViewState.Disabled)
    def Enable(self, state: ViewState = ViewState.Normal):
        """ Enable the widget, and optinally change its state from normal. """
        return self._SetState(state=state)

    def _SetState(self, state: ViewState):
        assert (isinstance(state, ViewState))
        try: self.configure(state=state.value)
        except tk.TclError: pass

        self._state_ = state
        return self
class BaseTextTkinterWidget(BaseTkinterWidget):
    _txt: tk.StringVar
    # noinspection PyMissingConstructor
    def __init__(self, *, Override_var: tk.StringVar or None, Text: str, configure: bool = True):
        if Override_var is not None:
            self._txt = Override_var
        else:
            self._txt = tk.StringVar(master=self, value=Text)
        if configure: self.configure(textvariable=self._txt)

    @property
    def txt(self) -> str: return self._txt.get()
    @txt.setter
    def txt(self, value: str): self._txt.set(value)

    @property
    def wrap(self) -> int: return self._wrap
    @wrap.setter
    def wrap(self, value: int):
        assert (isinstance(value, int))
        self._wrap = value
        self.configure(wraplength=self._wrap)



class CallWrapper(object):
    """Internal class. Stores function to call when some user
    defined Tcl function is called e.g. after an event occurred."""

    _func: callable
    _widget: Union[BaseTextTkinterWidget, BaseTkinterWidget] = None
    def __init__(self, func: callable, widget: BaseTkinterWidget = None):
        """Store FUNC, SUBST and WIDGET as members."""
        self._func: callable = func
        self._widget = widget

    def __call__(self, *args, **kwargs):
        """Apply first function SUBST to arguments, than FUNC."""
        try:
            return self._func(*args, **kwargs)
        except SystemExit: raise
        except Exception:
            if hasattr(self._widget, '_report_exception'):
                # noinspection PyProtectedMember
                self._widget._report_exception()
            else: raise

    def __repr__(self) -> str: return f'{super().__repr__().replace(">", "")} [ {dict(func=self._func, widget=self._widget)} ]>'
    def __str__(self) -> str: return repr(self)

    def SetWidget(self, w: BaseTkinterWidget):
        """ Internal Method """
        assert (isinstance(w, BaseTkinterWidget))
        self._widget = w
        return self

    @classmethod
    def Create(cls, func: callable, z: int or str = None, widget: BaseTkinterWidget = None, **kwargs):
        if kwargs and func:
            return cls(lambda x=kwargs: func(**x), widget=widget)
        elif z is not None and func:
            return cls(lambda x=z: func(x), widget=widget)
        elif func:
            return cls(func, widget=widget)

        return None
class CurrentValue(CallWrapper):
    def __call__(self, *args, **kwargs): return self._func(self._widget.txt, *args, **kwargs)
    def SetWidget(self, w):
        """
            Internal Method

        :param w:
        :type w: BaseTextTkinterWidget, CommandMixin
        :return: CurrentValue
        :rtype: CurrentValue
        """
        assert (isinstance(w, BaseTextTkinterWidget) and isinstance(w, CommandMixin))
        self._widget = w
        return self



class CommandMixin:
    _cmd: CallWrapper
    configure: callable
    def __call__(self, *args, **kwargs):
        """ Execute the Command """
        if callable(self._cmd): self._cmd(*args, **kwargs)
    def SetCommand(self, func: Union[callable, CurrentValue], z: int or str = None, **kwargs):
        try:
            assert (callable(func) or isinstance(func, CurrentValue))
        except AssertionError:
            raise ValueError(f'_func is not callable. got {type(func)}')

        if isinstance(func, CurrentValue): self._cmd = func.SetWidget(self)
        else: self._cmd = CallWrapper.Create(func, z, **kwargs)

        return self._setCommand()
    def _setCommand(self):
        self.configure(command=self._cmd)
        return self
class ImageMixin:
    _pi: dict
    configure: callable
    _IMG: Union[ImageTk.PhotoImage, tk.PhotoImage] = None
    def SetImage(self, path: str = None, data: str = None, url: str = None):
        if url: self.DownloadImage(url)
        elif data and path: raise KeyError('Cannot use both ImageData and ImageName')
        elif data:
            self._IMG = tk.PhotoImage(master=self, data=data)
            self.configure(image=self._IMG)
        elif path:
            self.OpenImage(path)
        return self
    def DownloadImage(self, url: str):
        raw_data = urlopen(url).read()
        with io.BytesIO(raw_data) as buf:
            with Image.open(buf) as img:
                self._IMG = ImageTk.PhotoImage(img, master=self)
                self.configure(image=self._IMG)
    def OpenImage(self, path: str):
        assert (os.path.isfile(path))
        with open(path, 'rb') as f:
            with Image.open(f) as img:
                self._IMG = ImageTk.PhotoImage(img, master=self)
                self.configure(image=self._IMG)
    def SetPhoto(self, *, Base64Data: str = None, rawData: bytes = None, MaxWidth: int, MaxHeight: int):
        if Base64Data:
            assert (isinstance(Base64Data, str))
            rawData = base64.b64decode(Base64Data)

        assert (isinstance(rawData, bytes))
        with io.BytesIO(rawData) as buf:
            with Image.open(buf) as tempImg:
                self._IMG = ImageTk.PhotoImage(master=self, image=ResizePhoto(tempImg, WidthMax=int(MaxWidth), HeightMax=int(MaxHeight)))
                self.configure(image=self._IMG)

    # # noinspection DuplicatedCode
    # def SetDefaultImage(self, ImagePath: str = None, ImageData: str = None, display=True):
    #     if ImageData and ImagePath: raise KeyError('Cannot use both ImageData and ImageName')
    #     elif ImageData:
    #         self._defaultImage = tk.PhotoImage(master=self, data=ImageData)
    #         if display: self.configure(image=self._defaultImage)
    #     elif ImagePath:
    #         self.OpenImage(ImagePath)
    #         if display: self.configure(image=self._defaultImage)
    #     return self
    # # noinspection DuplicatedCode
    # def SetOptionalImage(self, ImagePath: str = None, ImageData: str = None, display=True):
    #     if ImageData and ImagePath: raise KeyError('Cannot use both ImageData and ImageName')
    #     elif ImageData:
    #         self._optionalImage = tk.PhotoImage(master=self, data=ImageData)
    #         if display: self.configure(image=self._optionalImage)
    #     elif ImagePath:
    #         self.OpenImage(ImagePath)
    #         if display: self.configure(image=self._optionalImage)
    #     return self
