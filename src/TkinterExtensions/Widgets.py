# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

import base64
import io
import os
import tkinter as tk
from enum import Enum
from tkinter import Event as tkEvent, ttk
from typing import Union
from urllib.request import urlopen

from PIL import Image, ImageTk

from .Bindings import *
from .Enumerations import *
from .Events import *
from .Helpers import *




__all__ = [
        'tk', 'ttk', 'CurrentValue', 'tkEvent',

        'TkinterEntry', 'TkinterLabel', 'TkinterButton', 'TkinterListbox', 'TkinterTreeView', 'TkinterTreeViewHolder',
        'TkinterCheckBox', 'TkinterFrame', 'TkinterLabelFrame', 'TkinterComboBox',
        ]

class _BaseTkinterWidget_(tk.Widget):
    _state_: ViewState = ViewState.Hidden
    _pi: dict = { }
    _manager_: Layout = None
    _wrap: int = None

    @property
    def pi(self) -> dict: return self._pi.copy()

    @property
    def State(self) -> ViewState: return self._state_

    @property
    def width(self) -> int: return self.winfo_width()

    @property
    def height(self) -> int: return self.winfo_height()

    # noinspection PyUnresolvedReferences
    def show(self, **kwargs) -> bool:
        """
        Shows the current widget or frame, based on the current geometry manager.
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
    def _show(self, state: ViewState = ViewState.Normal) -> bool:
        self._SetState(state)
        return True

    # noinspection PyUnresolvedReferences
    def hide(self) -> bool:
        """
        Hides the current widget or frame, based on the current geometry manager.
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


    def Pack(self, cnf={ }, **kwargs):
        """Pack a widget in the parent widget. Use as options:
        after=widget - pack it after you have packed widget
        anchor=NSEW (or subset) - position widget according to
                                  given direction
        before=widget - pack it before you will pack widget
        expand=bool - expand widget if parent size grows
        fill=NONE or X or Y or BOTH - fill widget if widget grows
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        side=TOP or BOTTOM or LEFT or RIGHT -  where to add this widget.
        """
        self.pack(cnf, **kwargs)
        self._pi = self.pack_info()
        self._manager_ = Layout.pack
        return self

    def Place(self, cnf={ }, **kwargs):
        """Place a widget in the parent widget. Use as options:
        in=master - master relative to which the widget is placed
        in_=master - see 'in' option description
        x=amount - locate anchor of this widget at position x of master
        y=amount - locate anchor of this widget at position y of master
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
    def PlaceFull(self):
        """ Default placement in frame occupying the full screen and/or space available in master. """
        return self.Place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

    def Grid(self, cnf={ }, sticky: str or AnchorAndSticky = tk.NSEW, rowspan: int = 1, columnspan: int = 1, **kwargs):
        """Position a widget in the parent widget in a grid. Use as options:
        column=number - use cell identified with given column (starting with 0)
        columnspan=number - this widget will span several columns
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        row=number - use cell identified with given row (starting with 0)
        rowspan=number - this widget will span several rows
        sticky=NSEW - if cell is larger on which sides will this
                      widget stick to the cell boundary
        """
        if isinstance(sticky, AnchorAndSticky): sticky = sticky.value
        self.grid(cnf, sticky=sticky, rowspan=rowspan, columnspan=columnspan, **kwargs)
        self._pi = self.grid_info()
        self._manager_ = Layout.grid
        return self
    # noinspection PyMethodOverriding
    def Grid_Anchor(self, anchor: str or AnchorAndSticky):
        """The anchor value controls how to place the grid within the
        master when no row/column has any weight.

        The default anchor is nw."""
        if isinstance(anchor, AnchorAndSticky): anchor = anchor.value
        self.grid_anchor(anchor)
        return self
    def Grid_RowConfigure(self, index: int, weight: int = 1, **kwargs):
        """Configure row INDEX of a grid.

        Valid resources are minsize (minimum size of the row),
        weight (how much does additional space propagate to this row)
        and pad (how much space to let additionally)."""
        self.grid_rowconfigure(index, weight=weight, **kwargs)
        return self
    def Grid_ColumnConfigure(self, index: int, weight: int = 1, **kwargs):
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
class _BaseTextTkinterWidget_(_BaseTkinterWidget_):
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
        self._wrap = value
        self.configure(wraplength=self._wrap)



class CallWrapper(object):
    """Internal class. Stores function to call when some user
    defined Tcl function is called e.g. after an event occurred."""

    _func: callable
    _widget: Union[_BaseTextTkinterWidget_, _BaseTkinterWidget_] = None
    def __init__(self, func: callable, widget: Union[_BaseTextTkinterWidget_, _BaseTkinterWidget_] = None):
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



    def SetWidget(self, w):
        """ Internal Method """
        assert (isinstance(w, _BaseTkinterWidget_))
        self._widget = w
        return self

    @classmethod
    def Create(cls, func: callable, z: int or str = None, widget: Union[_BaseTextTkinterWidget_, tk.Widget] = None, **kwargs):
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
        """ Internal Method """
        assert (isinstance(w, _BaseTextTkinterWidget_) and isinstance(w, tk.Widget))
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
    def SetImage(self, ImagePath: str = None, ImageData: str = None, url: str = None):
        if url: self.DownloadImage(url)
        elif ImageData and ImagePath: raise KeyError('Cannot use both ImageData and ImageName')
        elif ImageData:
            self._IMG = tk.PhotoImage(master=self, data=ImageData)
            self.configure(image=self._IMG)
        elif ImagePath:
            self.OpenImage(ImagePath)
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
                self._IMG = ImageTk.PhotoImage(master=self, image=ResizePhoto(tempImg, MaxWidth=int(MaxWidth), MaxHeight=int(MaxHeight)))
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





class TkinterFrame(tk.Frame, _BaseTkinterWidget_):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master=master, **kwargs)

    def __name__(self, InstanceID: Union[str, int, Enum]):
        if isinstance(InstanceID, Enum): InstanceID = InstanceID.value

        return f'{self.__class__.__name__}_{InstanceID}'.lower()
class TkinterLabelFrame(tk.LabelFrame, _BaseTextTkinterWidget_):
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
        _BaseTextTkinterWidget_.__init__(self, Override_var=None, Text=Text, configure=False)

    @property
    def txt(self) -> str: return self._txt.get()
    @txt.setter
    def txt(self, value: str):
        self._txt.set(value)
        self.configure(text=value)



class TkinterEntry(tk.Entry, _BaseTextTkinterWidget_, CommandMixin):
    __doc__ = """Construct an entry _widget with the parent MASTER.

    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, highlightbackground,
    highlightcolor, highlightthickness, insertbackground,
    insertborderwidth, insertofftime, insertontime, insertwidth,
    invalidcommand, invcmd, justify, relief, selectbackground,
    selectborderwidth, selectforeground, show, state, takefocus,
    textvariable, validate, validatecommand, vcmd, width,
    xscrollcommand.
    """
    def __init__(self, master, Color: dict = None, Text: str = '', Override_var: tk.StringVar = None, **kwargs):
        tk.Entry.__init__(self, master=master, **kwargs)
        _BaseTextTkinterWidget_.__init__(self, Override_var=Override_var, Text=Text)
        if Color:
            self.configure(background=Color['BG'])
            self.configure(disabledforeground='black')
            self.configure(foreground=Color['FG'])
            self.configure(highlightbackground='light gray')
            self.configure(highlightcolor='black')
            self.configure(highlightbackground=Color['HBG'])
            self.configure(highlightcolor=Color['HFG'])

    def Clear(self):
        self.delete(tk.FIRST, tk.END)

    def _setCommand(self):
        self.bind(KeyBindings.bindButton, self._cmd)
        return self

    @property
    def txt(self) -> str:
        return self.get()
    @txt.setter
    def txt(self, value: str):
        self.insert(tk.END, value)




class TkinterButton(tk.Button, _BaseTextTkinterWidget_, ImageMixin, CommandMixin):
    """Construct a button _widget with the parent MASTER.

        STANDARD OPTIONS

            activebackground, activeforeground, anchor,
            background, bitmap, borderwidth, cursor,
            disabledforeground, font, foreground
            highlightbackground, highlightcolor,
            highlightthickness, image, justify,
            padx, pady, relief, repeatdelay,
            repeatinterval, takefocus, text,
            textvariable, underline, wraplength

        WIDGET-SPECIFIC OPTIONS

        command, compound, default, height,
        overrelief, state, width
    """
    def __init__(self, master, Text: str = '', Override_var: tk.StringVar = None, Color: dict = None, Command: callable = None, **kwargs):
        tk.Button.__init__(self, master=master, **kwargs)
        cmd = kwargs.pop('command', None)
        if cmd: self.SetCommand(cmd)
        if Color:
            self.configure(activebackground=Color['ABG'])
            self.configure(activeforeground=Color['AFG'])
            self.configure(background=Color['BG'])
            self.configure(disabledforeground='black')
            self.configure(foreground=Color['FG'])
            self.configure(highlightbackground='light gray')
            self.configure(highlightcolor='black')
            self.configure(highlightbackground=Color['HBG'])
            self.configure(highlightcolor=Color['HFG'])

        if Command: self.SetCommand(Command)
        _BaseTextTkinterWidget_.__init__(self, Override_var=Override_var, Text=Text)




class TkinterCheckBox(tk.Checkbutton, _BaseTextTkinterWidget_, ImageMixin, CommandMixin):
    """Construct a checkbutton _widget with the parent MASTER.

        Valid resource names:

                width
                height

                fg
                foreground
                bg
                background
                activebackground
                activeforeground
                highlightbackground
                highlightcolor
                highlightthickness
                disabledforeground
                selectcolor

                selectimage
                bitmap
                image

                indicatoron
                justify
                offvalue
                onvalue
                padx
                pady
                relief

                state
                takefocus

                text
                textvariable
                variable
                font

                command

                bd
                anchor
                cursor
                borderwidth
                underline
                wraplength

    """
    _value: tk.BooleanVar
    def __init__(self, master, Text: str = '', Override_var: tk.StringVar = None, **kwargs):
        tk.Checkbutton.__init__(self, master=master, **kwargs)
        _BaseTextTkinterWidget_.__init__(self, Override_var=Override_var, Text=Text)
        self._value = tk.BooleanVar(master=self, value=False)
        self.configure(variable=self._value)


    @property
    def value(self) -> bool: return self._value.get()
    @value.setter
    def value(self, b: bool):
        self._value.set(b)
        if b:
            self.select()
        else:
            self.deselect()




class TkinterComboBox(ttk.Combobox, _BaseTextTkinterWidget_, CommandMixin):
    """Construct a Ttk Combobox _widget with the parent master.

    STANDARD OPTIONS

        class, cursor, style, takefocus

    WIDGET-SPECIFIC OPTIONS

        exportselection
        postcommand

        textvariable

        values

        justify
        state
        height
        width
    """
    def __init__(self, master, Text: str = '', Override_var: tk.StringVar = None, **kwargs):
        ttk.Combobox.__init__(self, master=master, **kwargs)
        _BaseTextTkinterWidget_.__init__(self, Override_var=Override_var, Text=Text)

    @property
    def value(self) -> bool: return self._txt.get()
    @value.setter
    def value(self, v: str): self._txt.set(v)

    def _setCommand(self):
        self.bind(KeyBindings.ComboboxSelected, self._cmd)
        return self

    def SetValues(self, values: list or tuple):
        self.configure(values=values)



class TkinterLabel(tk.Label, _BaseTextTkinterWidget_, ImageMixin):
    __doc__ = """Construct a label _widget with the parent MASTER.

    STANDARD OPTIONS

        activebackground, activeforeground, anchor,
        background, bitmap, borderwidth, cursor,
        disabledforeground, font, foreground,
        highlightbackground, highlightcolor,
        highlightthickness, image, justify,
        padx, pady, relief, takefocus, text,
        textvariable, underline, wraplength

    WIDGET-SPECIFIC OPTIONS

        height, state, width

    """
    def __init__(self, master, Text: str = '', Override_var: tk.StringVar = None, Color: dict = None, **kwargs):
        tk.Label.__init__(self, master=master, **kwargs)
        _BaseTextTkinterWidget_.__init__(self, Override_var=Override_var, Text=Text)

        if Color:
            self.configure(activebackground=Color['ABG'])
            self.configure(activeforeground=Color['AFG'])
            self.configure(background=Color['BG'])
            self.configure(disabledforeground='black')
            self.configure(foreground=Color['FG'])
            self.configure(highlightbackground='light gray')
            self.configure(highlightcolor='black')
            self.configure(highlightbackground=Color['HBG'])
            self.configure(highlightcolor=Color['HFG'])



class TkinterListbox(tk.Listbox, _BaseTextTkinterWidget_, CommandMixin):
    """Construct a listbox _widget with the parent MASTER.

    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, height, highlightbackground,
    highlightcolor, highlightthickness, relief, selectbackground,
    selectborderwidth, selectforeground, selectmode, setgrid, takefocus,
    width, xscrollcommand, yscrollcommand, listvariable.

    Allowed WordWrap modes are ('word', 'none', 'char')
    """
    _Current_ListBox_Index: int = None
    def __init__(self, master, *, Command: callable = None, z=None, Color: dict = None, selectMode: str = tk.SINGLE, **kwargs):
        if 'SelectMode' in kwargs: selectMode = kwargs.pop('SelectMode')
        if 'selectmode' in kwargs: selectMode = kwargs.pop('selectmode')
        assert (selectMode in (tk.SINGLE, tk.MULTIPLE))
        tk.Listbox.__init__(self, master=master, selectmode=selectMode, **kwargs)
        if Command is not None: self.SetCommand(Command, z=z)
        if Color:
            self.configure(background=Color['BG'])
            self.configure(disabledforeground=Color['DFG'])
            self.configure(foreground=Color['FG'])
        # if Color:
        #     self.configure(activebackground=Color['ABG'])
        #     self.configure(activeforeground=Color['AFG'])
        #     self.configure(background=Color['BG'])
        #     self.configure(disabledforeground=Color['DFG'])
        #     self.configure(foreground=Color['FG'])
        #     self.configure(highlightbackground=Color['HBG'])
        #     self.configure(highlightcolor=Color['HFG'])
        #     self.configure(selectbackground=Color["SBG"])
        #     self.configure(selectforeground=Color["SBG"])
        #     self.configure(insertbackground=Color["IBG"])
    def SelectRow(self, index: int = None):
        if index is None: index = self._Current_ListBox_Index
        if index is None: return
        self.activate(index)
        self.selection_clear(0, tk.END)
        self.selection_set(index)
        self.focus_set()
        self._Current_ListBox_Index = index
    def SelectRows(self, *args):
        if args:
            self.selection_clear(0, tk.END)
            self.focus_set()
            for index in args:
                if isinstance(index, int):
                    self.activate(index)
                    self.selection_set(index)
                    self._Current_ListBox_Index = index
    def Current_Index(self, event: TkinterEvent = None) -> int or None:
        """ :return: int or None """
        try:
            selections = self.curselection()
            if selections != ():
                return selections[0]
            elif self._Current_ListBox_Index is not None:
                return self._Current_ListBox_Index
            else:
                return self.nearest(event.y)
        except (IndexError, AttributeError):
            return None

    def Clear(self):
        """ delete all lines from the listbox. """
        self.delete(0, tk.END)
    def DeleteAtIndex(self, index: int = None):
        """        delete a selected line from the listbox.        """
        if index is None: index = self.Current_Index()  # get selected line index
        if index is None: return
        self.delete(index)
    def ReplaceAtIndex(self, index: int, value: int or float or str):
        if value is not None:
            self.DeleteAtIndex(index)
            self.insert(index, value)
    def GetAtIndex(self, index: int) -> str: return self.get(index)

    def SetList(self, temp_list: list or tuple):
        """        clear the listbox and set the new items.        """
        self.Clear()
        for item in temp_list:
            self.insert(tk.END, item)
    def AddList(self, temp_list: list or tuple):
        """        Append items from the list into the listbox.        """
        for item in temp_list:
            self.insert(tk.END, item)
    def SortList(self, key: callable = str.lower):
        """        function to sort listbox items case insensitive by default.        """
        temp_list = self.Items
        temp_list.sort(key=key)
        # delete contents of present listbox
        self.delete(0, tk.END)
        # load listbox with sorted data
        for item in temp_list:
            self.insert(tk.END, item)

    def _setCommand(self):
        self.bind(KeyBindings.ListboxSelect, self._cmd)
        return self
    def ResetColors(self, color: str):
        for i in range(self.size()):
            self.itemconfig(i, background=color)

    @property
    def Items(self) -> list:
        """ returns the current listbox contents """
        return list(self.get(0, tk.END))

    @property
    def Index(self) -> int or None:
        return self._Current_ListBox_Index
    @Index.setter
    def Index(self, value: int or None):
        self._Current_ListBox_Index = value
        if value is not None: self.SelectRow(value)

    @property
    def txt(self) -> str:
        return self.get('1.0', tk.END)
    @txt.setter
    def txt(self, value: str):
        pass




class TkinterTreeView(ttk.Treeview, _BaseTkinterWidget_, CommandMixin):
    def __init__(self, master: tk.Frame, Color: dict = None, **kwargs):
        ttk.Treeview.__init__(self, master=master, **kwargs)
        if Color:
            self.configure(activebackground=Color['ABG'])
            self.configure(activeforeground=Color['AFG'])
            self.configure(background=Color['BG'])
            self.configure(disabledforeground=Color['DFG'])
            self.configure(foreground=Color['FG'])
            self.configure(highlightbackground=Color['HBG'])
            self.configure(highlightcolor=Color['HFG'])

    def _setCommand(self):
        self.bind(KeyBindings.TreeViewSelect, self._cmd)
        return self

    def SetTags(self, tags: dict):
        if tags:
            for tag, kwargs in tags.items():
                self.tag_configure(tag, **kwargs)
    def Clear(self): self.delete(*self.get_children())
    def SetItems(self, items: list or tuple or dict, *, clear: bool = True):
        assert (isinstance(items, (list, tuple, dict)))
        if clear: self.Clear()
        self._json_tree(tree=self, parent='', dictionary=items)
    def _json_tree(self, tree: ttk.Treeview, parent: str, dictionary: list or tuple or dict):
        GroupName = ''
        for key in dictionary:
            try:
                uid, GroupName = key.split('=')
            except (AttributeError, ValueError):
                uid = key
            if isinstance(dictionary[key], dict):
                tree.insert(parent, 'end', uid, text=key)
                self._json_tree(tree, uid, dictionary[key])

            elif isinstance(dictionary[key], (list, tuple)):
                tree.insert(parent, 'end', uid, text=GroupName)
                result = { }
                for x in dictionary[key]:
                    k, v = x.split('=')
                    result[k] = v
                self._json_tree(tree, uid, result)

            else:
                value = dictionary[key]
                if value is None:
                    value = 'None'
                tree.insert(parent, 'end', uid, text=value)  # text=key, value=value)

class TkinterTreeViewHolder(TkinterFrame):
    """Construct a Ttk Treeview with parent scale.

    STANDARD OPTIONS
        class, cursor, style, takefocus, xscrollcommand,
        yscrollcommand

    WIDGET-SPECIFIC OPTIONS
        columns, displaycolumns, height, padding, selectmode, show

    ITEM OPTIONS
        text, image, values, open, tags

    TAG OPTIONS
        foreground, background, font, image

    --------------------------------------------------------------
    Also creates ttk.scrollbar and the frame that conatins
    both TreeView and ScrollBar objects
    """
    TreeView: TkinterTreeView
    vsb: ttk.Scrollbar
    def __init__(self, master, backgroundColor: str, **kwargs):
        TkinterFrame.__init__(self, master=master, bg=backgroundColor, **kwargs)

        self.TreeView = TkinterTreeView(master=self, **kwargs)
        self.TreeView.pack(side='left', fill=tk.BOTH, expand=1)

        self.vsb = ttk.Scrollbar(master=self, orient="vertical", command=self)
        self.vsb.pack(side='right', fill='y')
        self.vsb.pi = self.vsb.place_info()
        self.TreeView.configure(yscrollcommand=self.vsb.set)
