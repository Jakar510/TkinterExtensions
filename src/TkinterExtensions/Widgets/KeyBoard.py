# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------
import string
from enum import IntEnum, IntFlag
from itertools import combinations
from tkinter import EventType
from typing import Dict, List

from PythonDebugTools import *

from .Frames import *
from .Root import *
from .Widgets import *
from ..Events import *
from ..Misc import Wait




__all__ = [
        'KeyboardEntry', 'KeyBoardState',
        'PopupKeyboard', 'Placement',
        ]

"""
Popup Keyboard is a module to be used with Python's Tkinter library
It subclasses the Entry widget as KeyboardEntry to make a pop-up keyboard appear when the widget gains focus. 
Still early in development.
"""



class KeyBoardState(IntEnum):
    Idle = 0
    Virtual = 1
    KeyPress = 2
    Typing = 3

class Placement(IntFlag):
    Auto = 0x100000

    Top = 0x010000
    Bottom = 0x001000

    Left = 0x000001
    Right = 0x000010
    Center = 0x000100

class PlacementSet(object):
    """ https://blog.magnussen.casa/post/using-enum-as-bitmasks-in-python/ """
    def __init__(self, *flags: Placement):
        self._state = Placement(0)  # Initiate no permissions
        for _flag in flags: self._state |= _flag

    def __contains__(self, o: Placement) -> bool: return (self._state & o) == o

    def __repr__(self): return repr(self._state)

PRINT('__Placement__', list(combinations(Placement, r=2)))



class PopupKeyboard(tkTopLevel):
    """
    A Toplevel instance that displays a keyboard that is attached to another widget.
    Only the Entry widget has a subclass in this version.
    https://www.alt-codes.net/arrow_alt_codes.php
    """
    _number = '[1,2,3]'
    _space = '[ space ]'
    _shift = 'shift'
    _next = '→'  # &#x2192  # '>>>'
    _previous = '←'  # &#x2190  # '<<<'
    _enter = '↲'  # &#x21B2
    _backspace = '<-'

    _is_number: bool = False

    _Frames: Dict[int, Frame] = { }
    _letters: Dict[int, Dict[int, Button]] = { }
    _numbers: Dict[int, Dict[int, Button]] = { }

    def __init__(self, root: tkRoot, *, entry, x: int, y: int, keycolor: str, keysize: int = -1, takefocus: bool = False):
        PRINT('__PopupKeyboard__', root=root, entry=entry, x=x, y=y, keysize=keysize, keycolor=keycolor, takefocus=takefocus)
        assert (isinstance(root, tkRoot))
        self.root = root
        super().__init__(master=root, fullscreen=False, Screen_Width=root.Screen_Width, Screen_Height=root.Screen_Height, takefocus=takefocus)
        self.overrideredirect(True)
        self.SetTransparency(0.85)

        assert (isinstance(entry, KeyboardEntry))
        self.entry: KeyboardEntry = entry

        self._keysize = keysize
        self._keycolor = keycolor

        self._x = x
        self._y = y

        self._init_keys()
        if keysize > 0: self.SetKeySize(keysize)
        else: self.SetKeySize(1)

        self.Bind(Bindings.Key, lambda e: self.destroy())  # destroy _PopupKeyboard on keyboard interrupt


    def AutoSize(self):
        keysize = 1
        while self.root.width >= self.width:
            self.SetKeySize(keysize)
            Wait(0.25)
            keysize += 1
    def SetKeySize(self, size: int):
        self._keysize = size

        for row in self._letters.values():
            for w in row.values():
                if 'space' in w.txt: w.configure(width=size * 3)
                else: w.configure(width=size)

        for row in self._numbers.values():
            for w in row.values():
                w.configure(width=size)
        return self._resize()
    def _resize(self):
        # resize to fit keys
        self.update_idletasks()
        self.update()

        self._SetDimmensions(frame_width=self._root_frame.width, frame_height=self._root_frame.height, entry_width=self.entry.width, entry_height=self.entry.height)

        PRINT('__resize__', size=self._keysize, width=self.width, root_width=self.root.width, _break=self.root.width > self.width)
        return self
    def _SetDimmensions(self, frame_width: int, frame_height: int, entry_width: int, entry_height: int):
        y = self._get_y(y=self._y, frame_height=frame_height, entry_height=entry_height, placement=self.entry.placement)
        x = self._get_x(x=self._x, frame_width=frame_width, entry_width=entry_width, placement=self.entry.placement)
        self.SetDimmensions(frame_width, frame_height, x, y)
    def _get_x(self, *, x: int, frame_width: int, entry_width: int, placement: PlacementSet):
        def left(): return int(x - frame_width + entry_width)
        def right(): return int(x)
        def center(): return int((x + (entry_width / 2)) - (frame_width / 2))
        def middle(): return int((self.root.width - frame_width) / 2 + self.root.x)

        root_width = self.root.width
        root_x = self.root.x
        x_plus_frame_width = x + frame_width
        x_minus_frame_width = x - frame_width

        try:
            if Placement.Auto in placement:
                if x_minus_frame_width < root_x:
                    print('right')
                    return middle()

                if x_plus_frame_width > root_width:
                    print('left')
                    return middle()

                if x_plus_frame_width < root_width and x_minus_frame_width > root_x:
                    print('center')
                    return center()

                return center()

            if Placement.Center in placement: return center()
            if Placement.Left in placement: return left()
            if Placement.Right in placement: return right()
        finally:
            PRINT('__get_x__',
                  x=x,
                  root_width=root_width,
                  root_x=root_x,
                  middle=middle(),
                  right=right(),
                  left=left(),
                  center=center(),
                  x_plus_frame_width=x_plus_frame_width,
                  x_minus_frame_width=x_minus_frame_width,
                  frame_width=frame_width,
                  entry_width=entry_width,
                  placement=placement)

        raise ValueError(f'placement is unknown. {placement}')
    def _get_y(self, *, y: int, frame_height: int, entry_height: int, placement: PlacementSet):
        def above(): return y - frame_height
        def below(): return y + entry_height

        root_height = self.root.height
        root_y = self.root.y
        try:
            if Placement.Top in placement: return above()
            elif Placement.Bottom in placement: return below()
            elif Placement.Auto in placement:
                if above() < root_y: return below()
                if below() > root_height: return above()

                return below()
        finally:
            PRINT('__get_y__',
                  y=y,
                  root_height=root_height,
                  root_y=root_y,
                  above=above(),
                  below=below(),
                  frame_height=frame_height,
                  entry_height=entry_height,
                  placement=placement)

        raise ValueError(f'self.entry.position is unknown. {placement}')



    def _init_keys(self):
        self._root_frame = Frame(self).PlaceFull()
        self._create_letters()
        self._create_numbers()

    def _create_numbers(self):
        self._numbers_frame = Frame(self._root_frame).PlaceFull()  # Grid(row=0, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)

        Row1: List[str] = [self._backspace, '/', '*', '-']
        Row2: List[str] = ['7', '8', '9', '+']
        Row3: List[str] = ['4', '5', '6']
        Row4: List[str] = ['1', '2', '3', self._enter]
        Row5: List[str] = ['0', '.']

        for r, row in enumerate([Row1, Row2, Row3, Row4, Row5]):
            if r not in self._numbers: self._numbers[r] = { }
            self._numbers_frame.Grid_RowConfigure(r, weight=1)
            for c, text in enumerate(row):
                self._numbers_frame.Grid_ColumnConfigure(c, weight=1)
                # size = self._keysize * 3 if 'space' in text else self._keysizev    # width=size,

                self._numbers[r][c] = Button(master=self._numbers_frame, text=text, bg=self._keycolor).Grid(row=r, column=c).SetCommand(self._attach_key_press, z=text)

        self._numbers_frame.hide()
    def _create_letters(self):
        self._letters_frame = Frame(self._root_frame).PlaceFull()  # Grid(row=0, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)
        self._Frames[0] = Frame(self._letters_frame).Grid(row=1, column=0).Grid_RowConfigure(0, weight=1)
        self._Frames[1] = Frame(self._letters_frame).Grid(row=2, column=0).Grid_RowConfigure(0, weight=1)
        self._Frames[2] = Frame(self._letters_frame).Grid(row=3, column=0).Grid_RowConfigure(0, weight=1)
        self._Frames[3] = Frame(self._letters_frame).Grid(row=4, column=0).Grid_RowConfigure(0, weight=1)

        Row1: List[str] = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '/']
        Row2: List[str] = [self._previous, 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ',', self._next]
        Row3: List[str] = [self._shift, 'z', 'x', 'c', 'v', 'b', 'n', 'm', '.', '?', self._number]
        Row4: List[str] = ['@', '#', '%', '*', self._space, '+', '-', '=']

        for r, row in enumerate([Row1, Row2, Row3, Row4]):
            if r not in self._letters: self._letters[r] = { }
            frame = self._Frames[r]
            self._root_frame.Grid_RowConfigure(r, weight=1)
            for c, text in enumerate(row):
                self._root_frame.Grid_ColumnConfigure(c, weight=1)
                # size = self._keysize * 3 if 'space' in text else self._keysizev    # width=size,

                self._letters[r][c] = Button(master=frame, text=text, bg=self._keycolor).Grid(row=r, column=c).SetCommand(self._attach_key_press, z=text)


    def _switchModes(self):
        if self._is_number:
            self._numbers_frame.hide()
            self._letters_frame.show()
            self._is_number = False
        else:
            self._numbers_frame.show()
            self._letters_frame.hide()
            self._is_number = True

        return self._resize()
    def SwitchCase(self):
        for row in self._letters.values():
            for w in row.values():
                if w.txt not in string.ascii_letters: continue
                if w.txt in string.ascii_uppercase:
                    w.txt = w.txt.lower()
                else:
                    w.txt = w.txt.upper()

    def _attach_key_press(self, k: str):
        if k == self._next:
            self.entry.tk_focusNext().focus_set()
            self.destroy()

        elif k == self._previous:
            self.entry.tk_focusPrev().focus_set()
            self.destroy()

        elif k == self._number: self._switchModes()

        elif k == self._space: self.entry.Append(' ')

        elif k == self._shift: self.SwitchCase()

        else: self.entry.Append(k)



class KeyboardEntry(Entry):
    """
    An extension/subclass of the Tkinter Entry widget, capable
    of accepting all existing args, plus a _keysize and _keycolor option.
    Will pop up an instance of _PopupKeyboard when focus moves into
    the widget

    Usage:
    KeyboardEntry(master, keysize=6, keycolor='white').pack()
    """
    def __init__(self, master, *, root: tkRoot, placement: PlacementSet = PlacementSet(Placement.Auto), keysize: int = -1, keycolor: str = 'gray', **kwargs):
        super().__init__(master=master, **kwargs)
        self.master = master

        assert (isinstance(root, tkRoot))
        self.root = root

        self.placement = placement

        self.keysize = keysize
        self.keycolor = keycolor

        self.state: KeyBoardState = KeyBoardState.Idle

        self.Bind(Bindings.FocusIn, self._check_state)
        self.Bind(Bindings.FocusOut, self._check_state)
        self.Bind(Bindings.Key, self._check_state)


    def _check_state(self, e: tkEvent): return self._handle_event_(TkinterEvent(e))
    def _handle_event_(self, event: TkinterEvent):
        PRINT('_check_state', event=event, state=self.state)
        print()
        print(event)
        print()
        print()

        if self.state == KeyBoardState.Virtual:
            if event == EventType.FocusOut:
                self._destroy_popup()
                self.state = KeyBoardState.Typing

            elif event == EventType.KeyPress:
                self._destroy_popup()
                self.state = KeyBoardState.Typing
                self.Append(event.char)

        elif self.state == KeyBoardState.Idle:
            if event.type == EventType.FocusIn:
                self._call_popup()
                self.state = KeyBoardState.Virtual


        elif self.state == KeyBoardState.Typing:
            if event == EventType.FocusOut:
                self.state = KeyBoardState.Idle

    def _call_popup(self):
        self.kb = PopupKeyboard(self.root, entry=self, x=self.winfo_rootx(), y=self.winfo_rooty(), keycolor=self.keycolor, keysize=self.keysize)
        self.kb.AutoSize()

    def _destroy_popup(self):
        self.kb.destroy()
        self.kb = None


    @staticmethod
    def test():
        root = tkRoot(Screen_Width=800, Screen_Height=480, x=200, y=200)
        frame = Frame(root, background='light blue').PlaceRelative(rely=0, relx=0.33, relwidth=0.66, relheight=1)

        TitledKeyboardEntry(frame, root=root, title=dict(text='Center Below'), entry=dict(keysize=6, keycolor='white', placement=PlacementSet(Placement.Center, Placement.Bottom))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Left Below'), entry=dict(keysize=6, keycolor='white', placement=PlacementSet(Placement.Left, Placement.Bottom))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Right Below'), entry=dict(keysize=6, keycolor='white', placement=PlacementSet(Placement.Right, Placement.Bottom))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Auto Below'), entry=dict(keysize=6, keycolor='white', placement=PlacementSet(Placement.Auto, Placement.Bottom))).Pack()

        TitledKeyboardEntry(frame, root=root, title=dict(text='FULL Auto'), entry=dict(keysize=-1, keycolor='white')).Pack()

        TitledKeyboardEntry(frame, root=root, title=dict(text='Center Above'), entry=dict(placement=PlacementSet(Placement.Center, Placement.Top))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Left Above'), entry=dict(placement=PlacementSet(Placement.Left, Placement.Top))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Right Above'), entry=dict(placement=PlacementSet(Placement.Right, Placement.Top))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Auto Above'), entry=dict(placement=PlacementSet(Placement.Auto, Placement.Top))).Pack()
        root.mainloop()



class TitledKeyboardEntry(Frame):
    def __init__(self, master, *, root: tkRoot, RowPadding: int = 1, factor: int = 3, entry: dict, title: dict, **kwargs):
        super().__init__(master, **kwargs)
        self.Grid_RowConfigure(0, weight=1).Grid_RowConfigure(1, weight=factor).Grid_ColumnConfigure(0, weight=1)

        self.Title = Label(self, **title).Grid(row=0, column=0, padx=RowPadding, pady=RowPadding)
        self.Entry = KeyboardEntry(master=self, root=root, **entry).Grid(row=1, column=0, padx=RowPadding, pady=RowPadding)
