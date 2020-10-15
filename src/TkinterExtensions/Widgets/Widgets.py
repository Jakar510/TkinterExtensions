# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

import base64
import io
import os
from enum import Enum
from typing import Tuple
from urllib.request import urlopen

from .BaseWidgets import *
from .Frames import Frame
from ..Bindings import Bindings
from ..Bindings.Events import *
from ..Misc.Enumerations import *
from ..Widgets.base import *




__all__ = [
        'Entry', 'Label', 'Button', 'Listbox', 'CheckBox', 'Canvas', 'Text', 'CheckButton', 'ScrolledText', 'Scrollbar',
        ]

"""
--Button
Canvas
CheckButton
--Entry
--Frame
--LabelFrame
--Label
--ListBox
Message
Popupmenu
RadioButton
Scale
Spinbox
Text
"""

# noinspection DuplicatedCode
class Button(tk.Button, BaseTextTkinterWidget, ImageMixin, CommandMixin):
    """Construct a button _widget with the master MASTER.

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
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, Text=Text)

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)


# noinspection DuplicatedCode
class Label(tk.Label, BaseTextTkinterWidget, ImageMixin, CommandMixin):
    __doc__ = """Construct a label _widget with the master MASTER.

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
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, Text=Text)

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

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)

    def _setCommand(self):
        self.bind(Bindings.Button, func=self._cmd)
        return self


# noinspection DuplicatedCode
class Entry(tk.Entry, BaseTextTkinterWidget, CommandMixin):
    __doc__ = """Construct an entry _widget with the master MASTER.

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
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, Text=Text)
        if Color:
            self.configure(background=Color['BG'])
            self.configure(disabledforeground='black')
            self.configure(foreground=Color['FG'])
            self.configure(highlightbackground='light gray')
            self.configure(highlightcolor='black')
            self.configure(highlightbackground=Color['HBG'])
            self.configure(highlightcolor=Color['HFG'])

    def Clear(self):
        self.delete(0, Tags.End.value)

    def _setCommand(self):
        self.bind(Bindings.Button.value, self._cmd)
        return self

    @property
    def txt(self) -> str: return self.get()
    @txt.setter
    def txt(self, value: str):
        self.Clear()
        self.insert(Tags.End.value, value)

    def Append(self, value: str):
        self.insert(Tags.End.value, value)

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)


class CheckBox(tk.Checkbutton, BaseTextTkinterWidget, ImageMixin, CommandMixin):
    """Construct a checkbutton _widget with the master MASTER.

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
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, Text=Text)
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

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)


class Listbox(tk.Listbox, BaseTextTkinterWidget, CommandMixin):
    """Construct a listbox _widget with the master MASTER.

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
        self.selection_clear(0, Tags.End.value)
        self.selection_set(index)
        self.focus_set()
        self._Current_ListBox_Index = index
    def SelectRows(self, *args):
        if args:
            self.selection_clear(0, Tags.End.value)
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
        self.delete(0, Tags.End.value)
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
    def Advance(self, *, forward: bool = True, amount: int = 1, extend: bool = False):
        """
            Advance the row either up or down.

        :param forward: direction to change: True moves down, False moves up.
        :type forward: bool
        :param amount: offset to change the line focus index
        :type amount: int
        :param extend: if forward is True, and extend is True, append new row on advance
        :type extend: bool
        :return:
        :rtype:
        """
        i = self.Index
        if forward: i += amount
        else: i -= amount

        if i > self.Count:
            if extend:
                for _ in range(amount): self.Append('')
            else: i = self.Count
        elif i < 0: i = 0

        self.Index = i

    def SetList(self, temp_list: list or tuple):
        """        clear the listbox and set the new items.        """
        self.Clear()
        for item in temp_list:
            self.insert(Tags.End.value, item)
    def AddList(self, temp_list: list or tuple):
        """        Append items from the list into the listbox.        """
        for item in temp_list:
            self.Append(item)
    def SortList(self, key: callable = str.lower):
        """        function to sort listbox items case insensitive by default.        """
        temp_list = self.Items
        temp_list.sort(key=key)
        # delete contents of present listbox
        self.delete(0, Tags.End.value)
        # load listbox with sorted data
        for item in temp_list:
            self.insert(Tags.End.value, item)
    def Append(self, value: str): self.insert(Tags.End.value, value)


    def _setCommand(self):
        self.bind(Bindings.ListboxSelect.value, self._cmd)
        return self
    def ResetColors(self, color: str):
        for i in range(self.size()):
            self.itemconfig(i, background=color)

    @property
    def Items(self) -> list:
        """ returns the current listbox contents """
        return list(self.get(0, Tags.End.value))


    def IsAllValidItems(self) -> bool: return all(self.Items)
    def ValidCount(self) -> int:
        count = 0
        for item in self.Items:
            if item: count += 1

        return count

    @property
    def Count(self) -> int: return self.size()

    @property
    def Index(self) -> int or None: return self._Current_ListBox_Index
    @Index.setter
    def Index(self, value: int or None):
        self._Current_ListBox_Index = value
        if value is not None: self.SelectRow(value)

    @property
    def txt(self) -> str: return self.GetAtIndex(self._Current_ListBox_Index)
    @txt.setter
    def txt(self, value: str): self.ReplaceAtIndex(self._Current_ListBox_Index, value)

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)


class Canvas(tk.Canvas, BaseTkinterWidget):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._setupBindings()
    def _setupBindings(self):
        self.bind(Bindings.Button.value, func=self.HandleRelease)
        self.bind(Bindings.ButtonRelease.value, func=self.HandlePress)

        self.bind(Bindings.FocusIn.value, func=self.HandleFocusIn)
        self.bind(Bindings.FocusOut.value, func=self.HandleFocusOut)

    def SetImage(self, x: int, y: int, path: str = None, data: str = None, url: str = None) -> Tuple[ImageTk.PhotoImage, Tuple[int, int], int]:
        if url: return self.DownloadImage(url, x, y)
        elif data and path: raise KeyError('Cannot use both ImageData and ImageName')
        elif data: return self.SetImageFromBytes(base64.b64decode(data), x, y)
        elif path: return self.OpenImage(path, x=x, y=y)
    def DownloadImage(self, url: str, x: int, y: int): return self.SetImageFromBytes(urlopen(url).read(), x, y)
    def OpenImage(self, path: str, x: int, y: int) -> Tuple[ImageTk.PhotoImage, Tuple[int, int], int]:
        assert (os.path.isfile(path))
        with open(path, 'rb') as f:
            with Image.open(f) as img:
                return self.CreateImage(image=img, x=x, y=y)
    def SetImageFromBytes(self, data: bytes, x: int, y: int) -> Tuple[ImageTk.PhotoImage, Tuple[int, int], int]:
        assert (isinstance(data, bytes))
        with io.BytesIO(data) as buf:
            with Image.open(buf) as tempImg:
                return self.CreateImage(image=tempImg, x=x, y=y)
    def CreateImage(self, image: Image.Image, x: int, y: int, anchor: str or AnchorAndSticky = tk.NW) -> Tuple[ImageTk.PhotoImage, Tuple[int, int], int]:
        img_tk = ImageTk.PhotoImage(image)
        return img_tk, image.size, self.create_image(x, y, anchor=anchor, image=img_tk)

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)

    def HandlePress(self, event: tkEvent):
        """
            Must Be overridden to work.

            suggestion:
                def HandlePress(self, event: tkEvent):
                    event = TkinterEvent(event)
                    ...

        :param event:
        :type event: tkEvent
        :return:
        :rtype:
        """
        pass
    def HandleRelease(self, event: tkEvent):
        """
            Must Be overridden to work.

            suggestion:
                def HandleRelease(self, event: tkEvent):
                    event = TkinterEvent(event)
                    ...

        :param event:
        :type event: tkEvent
        :return:
        :rtype:
        """
        pass

    def HandleFocusIn(self, event: tkEvent):
        """
            Must Be overridden to work.

            suggestion:
                def HandleFocusIn(self, event: tkEvent):
                    event = TkinterEvent(event)
                    ...

        :param event:
        :type event: tkEvent
        :return:
        :rtype:
        """
        pass
    def HandleFocusOut(self, event: tkEvent):
        """
            Must Be overridden to work.

            suggestion:
                def HandleFocusOut(self, event: tkEvent):
                    event = TkinterEvent(event)
                    ...

        :param event:
        :type event: tkEvent
        :return:
        :rtype:
        """
        pass


class CheckButton(tk.Checkbutton, BaseTextTkinterWidget, CommandMixin):

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)


class Scrollbar(tk.Scrollbar, BaseTkinterWidget, CommandMixin):

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)


class Text(tk.Text, BaseTextTkinterWidget, CommandMixin):
    def Clear(self): self.delete(self.GetIndex(1, 0), tk.END)

    @staticmethod
    def GetIndex(line: int, char: int): return f'{line}.{char}'

    @property
    def txt(self) -> str: return self.get(self.GetIndex(1, 0), tk.END)
    @txt.setter
    def txt(self, value: str): self.insert(self.GetIndex(1, 0), value)

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)
    def _setCommand(self):
        self.bind(Bindings.Button, func=self._cmd)
        return self


class ScrolledText(Frame, BaseTextTkinterWidget, CommandMixin):
    def __init__(self, master, **kw):
        super().__init__(master=master, **kw)
        self.text = Text(master=self)

        self.vbar = Scrollbar(self)
        self.vbar.Pack(side=tk.RIGHT, fill=Fill.y)
        self.vbar.SetCommand(self.text.yview)
        self.text.configure(yscrollcommand=self.vbar.set)

        self.text.Pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    @property
    def txt(self) -> str: return self.text.txt
    @txt.setter
    def txt(self, value: str): self.text.txt = value

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)

    def _setCommand(self):
        self.text.bind(Bindings.Button, func=self._cmd)
        return self
