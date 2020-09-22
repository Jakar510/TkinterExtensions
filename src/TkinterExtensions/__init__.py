# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
import base64
import io
import os
import pprint
import tkinter as tk
from abc import ABC
from enum import IntEnum
from tkinter import Event as tkEvent, ttk
from typing import Dict, Union
from urllib.request import urlopen

from PIL import Image, ImageTk

from .Enumerations import *




__all__ = [
        'TkinterEntry', 'TkinterLabel', 'TkinterButton', 'TkinterListbox', 'TkinterEvent', 'tkEvent', 'KeyBindings', 'TkinterTreeView', 'TkinterTreeViewHolder', 'TkinterCheckBox',
        'TkinterFrame', 'TkinterLabelFrame', 'TkinterComboBox', 'tk', 'ttk', 'ButtonGrid', 'ResizePhoto', 'CalculateWrapLength', 'RoundFloat',

        'ActiveStyle', 'AnchorAndSticky', 'Fill', 'Side', 'Relief', 'Orient', 'Wrap', 'BorderMode', 'Tags', 'States', 'MenuItemTypes', 'SelectionMode', 'CanvasStyles', 'ViewArguments'
        ]



def RoundFloat(Float: float, Precision: int) -> str:
    """ Rounds the Float to the given Precision and returns It as string. """
    return f"{Float:.{Precision}f}"
def ResizePhoto(image: Image.Image, *, MaxWidth: int, MaxHeight: int) -> Image:
    scalingFactor = min((MaxWidth / image.width, MaxHeight / image.height))
    newSize = (int(scalingFactor * image.width), int(scalingFactor * image.height))
    return image.resize(newSize)
def CalculateWrapLength(screenWidth: int, *args: Union[int, float]) -> int:
    """
        Example: WrapLength = self._screenWidth * relWidgetWidth * offset

    :param screenWidth: base screen width
    :param args: a list of float or integers to be cumulatively multiplied together.
    :return:
    """
    for arg in args:
        assert (isinstance(arg, (int, float)))
        screenWidth *= arg
    return int(screenWidth)




class KeyBindings(object):
    Return = 'Return'
    Delete = 'Delete'
    BackSpace = 'BackSpace'
    Minus = 'minus'
    KP_Enter = 'KP_Enter'
    Enter = 'Enter'

    Tab = 'Tab'
    ShiftTab = 'ShiftTab'
    ShiftTabEvent = '<Shift-KeyPress-Tab>'

    bindKey = '<Key>'
    bindButton = "<Button>"
    ListboxSelect = "<<ListboxSelect>>"
    ComboboxSelected = "<<ComboboxSelected>>"
    TreeViewSelect = "<<TreeviewSelect>>"

    bindF4 = '<F4>'
    F4 = 'F4'

    bindF5 = '<F5>'
    F5 = 'F5'

    bindF8 = '<F8>'
    F8 = 'F8'

    F12 = 'F12'
    bindF12 = '<F12>'

    bindF11 = '<F11>'
    F11 = 'F11'

    @staticmethod
    def isEnter(keysym: str) -> bool:
        return keysym == KeyBindings.Enter or keysym == KeyBindings.KP_Enter or keysym == KeyBindings.Return



class TkinterEvent(tkEvent):
    __slots__ = ['serial', 'num', 'height', 'keycode', 'state', 'time', 'width', 'x', 'y', 'char', 'keysym', 'keysym_num', 'type', 'widget', 'x_root', 'y_root', 'delta']
    def __init__(self, *args, source: tkEvent = None, **kwargs):
        super().__init__(*args, **kwargs)
        if source is not None:
            self.__dict__ = source.__dict__
            for name, value in source.__dict__.items():
                setattr(self, name, value)

    def __str__(self) -> str: return self.ToString()
    def __repr__(self) -> str: return self.ToString()

    def ToString(self) -> str: return f'<{self.__class__.__name__} Object. SavedFileSettings: \n{pprint.pformat(self.ToDict(), indent=4)} >'
    def ToDict(self) -> dict:
        """
            {
                'num': self.num,
                'height': self.height,
                'width': self.width,
                'widget': self.widget,
                'keysym': self.keysym,
                'keycode': self.keycode,
                'keysym_num': self.keysym_num,
                'state': self.state,
                'time': self.time,
                'x': self.x,
                'y': self.y,
                'char': self.char,
                'type': self.type,
                'x_root': self.x_root,
                'y_root': self.y_root,
                'delta': self.delta,
            }
        :return:
        """
        return self.__dict__
    # def ToDict(self) -> dict: return {
    #             'num': self.num,
    #             'height': self.height,
    #             'width': self.width,
    #             'widget': self.widget,
    #             'keysym': self.keysym,
    #             'keycode': self.keycode,
    #             'keysym_num': self.keysym_num,
    #             'state': self.state,
    #             'time': self.time,
    #             'x': self.x,
    #             'y': self.y,
    #             'char': self.char,
    #             'type': self.type,
    #             'x_root': self.x_root,
    #             'y_root': self.y_root,
    #             'delta': self.delta,
    #             }


class Layout(IntEnum):
    place = 1
    grid = 2
    pack = 3
# noinspection PyUnresolvedReferences
class _LayoutManagerMixin:
    _pi: dict = { }
    _manager_: Layout = None
    def show(self, *args, **kwargs) -> bool:
        """         Shows the current widget or frame. Can be overridden to add additional functionality if need.        """
        if self._manager_ is None: return False
        if self._manager_ == Layout.pack:
            self.pack(self._pi)
            return True
        elif self._manager_ == Layout.grid:
            self.grid(self._pi)
            return True
        elif self._manager_ == Layout.place:
            self.place(self._pi)
            return True

        return False
    def hide(self, *args, **kwargs) -> bool:
        """         Hides the current widget or frame. Can be overridden to add additional functionality if need.        """
        if self._manager_ is None: return False
        if self._manager_ == Layout.pack:
            self.pack_forget()
            return True
        elif self._manager_ == Layout.grid:
            self.grid_forget()
            return True
        elif self._manager_ == Layout.place:
            self.place_forget()
            return True

        return False

    def pack(self, *args, **kwargs):
        super(_LayoutManagerMixin, self).pack(*args, **kwargs)
        self._pi = self.pack_info()
        self._manager_ = Layout.pack
        return self

    def place(self, *args, **kwargs):
        super(_LayoutManagerMixin, self).place(*args, **kwargs)
        self._pi = self.place_info()
        self._manager_ = Layout.place
        return self

    def grid(self, *args, sticky: str or AnchorAndSticky = tk.NSEW, rowspan: int = 1, columnspan: int = 1, **kwargs):
        if isinstance(sticky, AnchorAndSticky): sticky = sticky.value
        super(_LayoutManagerMixin, self).grid(*args, sticky=sticky, rowspan=rowspan, columnspan=columnspan, **kwargs)
        self._pi = self.grid_info()
        self._manager_ = Layout.grid
        return self
    def grid_anchor(self, anchor: str or AnchorAndSticky):
        if isinstance(anchor, AnchorAndSticky): anchor = anchor.value
        super(_LayoutManagerMixin, self).grid_anchor(anchor)
        return self
    def grid_rowconfigure(self, index: int, weight: int = 1, **kwargs):
        super(_LayoutManagerMixin, self).grid_rowconfigure(index, weight=weight, **kwargs)
        return self
    def grid_columnconfigure(self, index: int, weight: int = 1, **kwargs):
        super(_LayoutManagerMixin, self).grid_columnconfigure(index, weight=weight, **kwargs)
        return self
class _ImageMixin:
    configure: callable
    _master: any
    _pi: dict
    _optionalImage: ImageTk.PhotoImage
    _defaultImage: ImageTk.PhotoImage
    _IMG: ImageTk.PhotoImage
    def SetDefaultImage(self, ImagePath: str = None, ImageData: str = None, display=True):
        if ImageData and ImagePath: raise KeyError('Cannot use both ImageData and ImageName')
        elif ImageData:
            self._defaultImage = tk.PhotoImage(master=self._master, data=ImageData)
            if display: self.configure(image=self._defaultImage)
        elif ImagePath:
            self.OpenImage(ImagePath)
            if display: self.configure(image=self._defaultImage)
        return self
    def SetOptionalImage(self, ImagePath: str = None, ImageData: str = None, display=True):
        if ImageData and ImagePath: raise KeyError('Cannot use both ImageData and ImageName')
        elif ImageData:
            self._optionalImage = tk.PhotoImage(master=self, data=ImageData)
            if display: self.configure(image=self._optionalImage)
        elif ImagePath:
            self.OpenImage(ImagePath)
            if display: self.configure(image=self._optionalImage)
        return self
    def SetImage(self, ImagePath: str = None, ImageData: str = None, default: bool = False, optional: bool = False, url: str = None):
        if optional:
            self.configure(image=self._optionalImage)
        elif default:
            self.configure(image=self._defaultImage)
        elif url:
            raw_data = urlopen(url).read()
            with io.BytesIO(raw_data) as buf:
                with Image.open(buf) as img:
                    self._IMG = ImageTk.PhotoImage(img, master=self._master)
                    self.configure(image=self._IMG)
        elif ImageData and ImagePath: raise KeyError('Cannot use both ImageData and ImageName')
        elif ImageData:
            self._IMG = tk.PhotoImage(master=self._master, data=ImageData)
            self.configure(image=self._IMG)
        elif ImagePath:
            self.OpenImage(ImagePath)
        return self
    def OpenImage(self, path: str):
        assert (os.path.isfile(path))
        with open(path, 'rb') as f:
            with Image.open(f) as img:
                self._IMG = ImageTk.PhotoImage(img, master=self._master)
                self.configure(image=self._IMG)
    def SetPhoto(self, *, Base64Data: str = None, rawData: bytes = None,
                 parent_pi: dict = None, parentRelX: float = None, parentRelY: float = None,
                 maxWidth: int = None, maxHeight: int = None,
                 offset_factor: float = 0.95, screenWidth: int, screenHeight: int):
        if parent_pi is not None:
            parentRelX = float(parent_pi['relwidth'])
            parentRelY = float(parent_pi['relheight'])

        assert (isinstance(parentRelX, float))
        assert (isinstance(parentRelY, float))

        if maxWidth is None:
            # if hasattr(widget, 'width'): maxHeight = widget.width
            if 'width' in self._pi and self._pi['width'] != '':
                maxWidth = (float(self._pi['width']) / screenWidth) * offset_factor * parentRelX
            else:
                maxWidth = CalculateWrapLength(screenWidth, float(self._pi['relwidth']), offset_factor, parentRelX)
            maxWidth = int(maxWidth)
        if maxHeight is None:
            # if hasattr(widget, 'height'): maxHeight = widget.height
            if 'height' in self._pi and self._pi['height'] != '':
                maxHeight = (float(self._pi['height']) / screenHeight) * offset_factor * parentRelY
            else:
                maxHeight = CalculateWrapLength(screenHeight, float(self._pi['relheight']), offset_factor, parentRelY)
            maxHeight = int(maxHeight)

        if Base64Data:
            assert (Base64Data is not None)
            msg = base64.b64decode(Base64Data)
        else:
            assert (rawData is not None)
            msg = rawData

        with io.BytesIO(msg) as buf:
            with Image.open(buf) as tempImg:
                self._IMG = ImageTk.PhotoImage(master=self, image=ResizePhoto(tempImg, MaxWidth=maxWidth, MaxHeight=maxHeight))
                self.configure(image=self._IMG)
class _CommandMixin:
    _cmd: callable
    configure: callable
    def SetCommand(self, func: callable, z: int or str = None, **kwargs):
        try:
            assert (callable(func))
        except AssertionError:
            raise ValueError(f'func is not callable. got {type(func)}')
        if kwargs and func:
            self._cmd = lambda x=kwargs: func(**x)
            self.configure(command=self._cmd)
        elif z is not None and func:
            self._cmd = lambda x=z: func(x)
            self.configure(command=self._cmd)
        elif func:
            self._cmd = func
            self.configure(command=func)
        return self


    def __call__(self, *args, **kwargs):
        if self._cmd:
            self._cmd(*args, **kwargs)



class _BaseTkinterWidget(object):
    configure: callable
    winfo_width: callable
    winfo_height: callable
    _master: any

    _pi: dict
    _wrap: int
    _IMG = None
    _defaultImage = None
    _optionalImage = None

    _txt: tk.StringVar
    img: Image.Image
    imgTk: ImageTk.PhotoImage
    _screenWidth: int
    _screenHeight: int

    @property
    def wrap(self) -> int: return self._wrap
    @wrap.setter
    def wrap(self, value: int):
        self._wrap = value
        self.configure(wraplength=self._wrap)

    @property
    def txt(self) -> str: return self._txt.get()
    @txt.setter
    def txt(self, value: str): self._txt.set(value)

    @property
    def pi(self) -> dict: return self._pi.copy()
    @property
    def width(self) -> int: return self.winfo_width()
    @property
    def height(self) -> int: return self.winfo_height()

    @property
    def __name__(self) -> str: return str(self.__class__.__name__)


class TkinterFrame(_LayoutManagerMixin, tk.Frame, _BaseTkinterWidget):
    def __init__(self, master, **kwargs):
        self._master = master
        tk.Frame.__init__(self, master=self._master, **kwargs)
        self.place_configure()
class TkinterLabelFrame(_LayoutManagerMixin, tk.LabelFrame, _BaseTkinterWidget):
    def __init__(self, master, **kwargs):
        self._master = master
        tk.LabelFrame.__init__(self, master=self._master, **kwargs)

    @property
    def txt(self) -> str: return self._txt.get()
    @txt.setter
    def txt(self, value: str):
        self._txt.set(value)
        self.configure(text=value)


class TkinterEntry(_LayoutManagerMixin, tk.Entry, _BaseTkinterWidget):
    __doc__ = """Construct an entry widget with the parent MASTER.

    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, highlightbackground,
    highlightcolor, highlightthickness, insertbackground,
    insertborderwidth, insertofftime, insertontime, insertwidth,
    invalidcommand, invcmd, justify, relief, selectbackground,
    selectborderwidth, selectforeground, show, state, takefocus,
    textvariable, validate, validatecommand, vcmd, width,
    xscrollcommand.
    """
    def __init__(self, master, Color: dict = None, **kwargs):
        self._master = master
        tk.Entry.__init__(self, master=self._master, **kwargs)
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

    @property
    def txt(self) -> str:
        return self.get()
    @txt.setter
    def txt(self, value: str):
        self.insert(tk.END, value)


class TkinterButton(_LayoutManagerMixin, tk.Button, _BaseTkinterWidget, _ImageMixin, _CommandMixin):
    """Construct a button widget with the parent MASTER.

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
        self._master = master
        tk.Button.__init__(self, master=self._master, **kwargs)
        cmd = kwargs.get('Command', None) or kwargs.get('command', None)
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
        if Override_var is not None:
            self._txt = Override_var
        else:
            self._txt = tk.StringVar(master=self, value=Text)
        self.configure(textvariable=self._txt)


class TkinterCheckBox(_LayoutManagerMixin, tk.Checkbutton, _BaseTkinterWidget, _CommandMixin, _ImageMixin):
    """Construct a checkbutton widget with the parent MASTER.

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
        self._master = master
        tk.Checkbutton.__init__(self, master=self._master, **kwargs)
        self._value = tk.BooleanVar(master=self, value=False)
        self.configure(variable=self._value)

        if Override_var is not None:
            self._txt = Override_var
        else:
            self._txt = tk.StringVar(master=self, value=Text)
        self.configure(textvariable=self._txt)

    @property
    def value(self) -> bool: return self._value.get()
    @value.setter
    def value(self, b: bool):
        self._value.set(b)
        if b:
            self.select()
        else:
            self.deselect()


class TkinterComboBox(_LayoutManagerMixin, ttk.Combobox, _BaseTkinterWidget, _CommandMixin):
    """Construct a Ttk Combobox widget with the parent master.

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
        self._master = master
        ttk.Combobox.__init__(self, master=self._master, **kwargs)

        if Override_var is not None:
            self._txt = Override_var
        else:
            self._txt = tk.StringVar(master=self, value=Text)
        self.configure(textvariable=self._txt)

    @property
    def value(self) -> bool: return self._txt.get()
    @value.setter
    def value(self, v: str): self._txt.set(v)

    def SetCommand(self, func: callable, z: int or str = None, **kwargs):
        assert (callable(func))
        if kwargs and func:
            self._cmd = lambda x=kwargs: func(**x)
            self.bind(KeyBindings.ComboboxSelected, self._cmd)
        elif z is not None and func:
            self._cmd = lambda x=z: func(x)
            self.bind(KeyBindings.ComboboxSelected, self._cmd)
        elif func:
            self._cmd = func
            self.bind(KeyBindings.ComboboxSelected, self._cmd)
        return self

    def SetValues(self, values: list or tuple):
        self.configure(values=values)


class TkinterLabel(_LayoutManagerMixin, tk.Label, _BaseTkinterWidget, _ImageMixin):
    __doc__ = """Construct a label widget with the parent MASTER.

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
        self._master = master
        tk.Label.__init__(self, master=self._master, **kwargs)

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

        if Override_var is not None:
            self._txt = Override_var
        else:
            self._txt = tk.StringVar(master=self, value=Text)
        self.configure(textvariable=self._txt)


class TkinterListbox(_LayoutManagerMixin, tk.Listbox, _BaseTkinterWidget, _CommandMixin):
    """Construct a listbox widget with the parent MASTER.

    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, height, highlightbackground,
    highlightcolor, highlightthickness, relief, selectbackground,
    selectborderwidth, selectforeground, selectmode, setgrid, takefocus,
    width, xscrollcommand, yscrollcommand, listvariable.

    Allowed WordWrap modes are ('word', 'none', 'char')
    """
    _Current_ListBox_Index: int = None
    def __init__(self, master, *, Command: callable = None, z=None, Color: dict = None, selectMode: str = tk.SINGLE, **kwargs):
        self._master = master
        if 'SelectMode' in kwargs:
            selectMode = kwargs.pop('SelectMode')
        assert (selectMode in (tk.SINGLE, tk.MULTIPLE))
        tk.Listbox.__init__(self, master=self._master, selectmode=selectMode, **kwargs)
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

    def SetCommand(self, func: callable, z: int or str = None, **kwargs):
        assert (callable(func))
        if kwargs and func:
            self._cmd = lambda x=kwargs: func(**x)
            self.bind(KeyBindings.ListboxSelect, self._cmd)
        elif z is not None and func:
            self._cmd = lambda x=z: func(x)
            self.bind(KeyBindings.ListboxSelect, self._cmd)
        elif func:
            self._cmd = func
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


class TkinterTreeView(_LayoutManagerMixin, ttk.Treeview, _BaseTkinterWidget, _CommandMixin):
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
    def SetCommand(self, func: callable, z: int or str = None, **kwargs):
        assert (callable(func))
        if kwargs and func:
            self._cmd = lambda x=kwargs: func(**x)
            self.bind(KeyBindings.TreeViewSelect, self._cmd)
        elif z is not None and func:
            self._cmd = lambda x=z: func(x)
            self.bind(KeyBindings.TreeViewSelect, self._cmd)
        elif func:
            self._cmd = func
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



class ButtonGrid(TkinterFrame, ABC):
    __buttons: Dict[int, TkinterButton] = { }
    def __init__(self, *, master: TkinterFrame, rows: int = None, cols: int = None, NumberOfButtons: int = None, **kwargs):
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
            self.__buttons[i] = TkinterButton(self, Text=self.ButtonTitles[i], **kwargs)
            self.__buttons[i].grid(row=r, column=c)
            self.__buttons[i].SetCommand(self.ButtonCommands[i])
            c += 1

    def HideAll(self):
        for w in self.__buttons.values():
            w.hide()
    def ShowAll(self):
        for w in self.__buttons.values():
            w.show()

    @property
    def ButtonTitles(self) -> dict: raise NotImplementedError()
    @property
    def ButtonCommands(self) -> dict: raise NotImplementedError()


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
