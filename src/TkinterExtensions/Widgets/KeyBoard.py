# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

'''Popup Keyboard is a module to be used with Python's Tkinter library
It subclasses the Entry widget as KeyboardEntry to make a pop-up
keyboard appear when the widget gains focus. Still early in development.
'''
from enum import IntEnum
from typing import Dict, List

from .Frames import *
from .Root import *
from .Widgets import *
from .base import *




class _PopupKeyboard(tkTopLevel):
    '''A Toplevel instance that displays a keyboard that is attached to
    another widget. Only the Entry widget has a subclass in this version.
    '''
    def __init__(self, master: tkRoot, attach: Entry, x: int, y: int, keycolor: str, keysize: int =5, takefocus: bool = False):
        super().__init__(master=master, takefocus=takefocus)

        self.overrideredirect(True)
        self.attributes('-alpha', 0.85)

        self.master = master
        self.attach = attach
        self._keysize = keysize
        self._keycolor = keycolor
        self._x = x
        self._y = y

        self._Frames: Dict[int, Frame] = {}
        self._buttons: Dict[int, Dict[int, Dict[int, Button]]] = { }

        self._init_keys()

        self.bind('<Key>', lambda e: self.destroy()) # destroy _PopupKeyboard on keyboard interrupt

        # resize to fit keys
        self.update_idletasks()
        self.update()
        newGeometry = f'{self._root_frame.width}_x{self._root_frame.height}+{self._x}+{self._y}'
        self.geometry(newGeometry)

    def _init_keys(self):
        self._root_frame = Frame(self).Grid(row=0, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)
        self._Frames[0] = Frame(self._root_frame).Grid(row=1, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)
        self._Frames[1] = Frame(self._root_frame).Grid(row=2, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)
        self._Frames[2] = Frame(self._root_frame).Grid(row=3, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)
        self._Frames[3] = Frame(self._root_frame).Grid(row=4, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)

        Row1: List[str] = ['q', 'w', 'e', 'r', 't', '_y', 'u', 'i', 'o', 'p', '/']
        Row2: List[str] = ['<<<', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ',', '>>>']
        Row3: List[str] = ['shift', 'z', '_x', 'c', 'v', 'b', 'n', 'm', '.', '?', '[1,2,3]']
        Row4: List[str] = ['@', '#', '%', '*', '[ space ]', '+', '-', '=']
        Rows: List[List[str]] = [Row1, Row2, Row3, Row4]

        for r, row in enumerate(Rows):
            if r not in self._buttons: self._buttons[r] = {}
            self._root_frame.Grid_RowConfigure(r, weight=1)
            for c, text in enumerate(row):
                if c not in self._buttons[r]: self._buttons[r][c] = {}
                self._root_frame.Grid_ColumnConfigure(c, weight=1)
                size = self._keysize * 3 if 'space' in text else self._keysize

                self._buttons[r][c] = Button(master=self._Frames[r], width=size, text=text, bg=self._keycolor).Grid(row=r, column=c).SetCommand(self._attach_key_press, z=text)


    def _attach_key_press(self, k: str):
        if k == '>>>':
            self.attach.tk_focusNext().focus_set()
            self.destroy()
        elif k == '<<<':
            self.attach.tk_focusPrev().focus_set()
            self.destroy()
        elif k == '[1,2,3]':
            pass
        elif k == '[ space ]':
            self.attach.Append(' ')
        else:
            self.attach.Append(k)


'''
TO-DO: Implement Number Pad
class _PopupNumpad(Toplevel):
    def __init__(self, _x, _y, _keycolor='gray', _keysize=5):
        Toplevel.__init__(self, takefocus=0)

        self.overrideredirect(True)
        self.attributes('-alpha',0.85)

        self.numframe = Frame(self)
        self.numframe.grid(row=1, column=1)

        self.__init_nums()

        self.update_idletasks()
        self.geometry('{}_x{}+{}+{}'.format(self.winfo_width(),
                                           self.winfo_height(),
                                           self._x,self._y))

    def __init_nums(self):
        i=0
        for num in ['7','4','1','8','5','2','9','6','3']:
            print num
            Button(self.numframe,
                   text=num,
                   width=int(self._keysize/2),
                   bg=self._keycolor,
                   command=lambda num=num: self.__attach_key_press(num)).grid(row=i%3, column=i/3)
            i+=1
'''

class KeyBoardState(IntEnum):
    Idle = 0
    Virtual = 1
    KeyPress = 2
    Typing = 3

class KeyboardEntry(Frame):
    """An extension/subclass of the Tkinter Entry widget, capable
    of accepting all existing args, plus a _keysize and _keycolor option.
    Will pop up an instance of _PopupKeyboard when focus moves into
    the widget

    Usage:
    KeyboardEntry(master, _keysize=6, _keycolor='white').pack()
    """
    def __init__(self, master, keysize=5, keycolor='gray', *args, **kwargs):
        super().__init__(master=master)
        self.master = master

        self.entry = Entry(self, *args, **kwargs)
        self.entry.PackFull()

        self.keysize = keysize
        self.keycolor = keycolor

        self.state: KeyBoardState = KeyBoardState.Idle

        self.entry.bind('<FocusIn>', lambda e: self._check_state('focusin'))
        self.entry.bind('<FocusOut>', lambda e: self._check_state('focusout'))
        self.entry.bind('<Key>', lambda e: self._check_state('keypress'))

    def _check_state(self, event):
        """finite state machine"""
        if self.state == KeyBoardState.Idle:
            if event == 'focusin':
                self._call_popup()
                self.state = 'virtualkeyboard'
        elif self.state == KeyBoardState.Virtual:
            if event == 'focusin':
                self._destroy_popup()
                self.state = KeyBoardState.Typing
            elif event == 'keypress':
                self._destroy_popup()
                self.state = KeyBoardState.Typing
        elif self.state == 'typing':
            if event == 'focusout':
                self.state = KeyBoardState.Idle

    def _call_popup(self):
        self.kb = _PopupKeyboard(attach=self.entry,
                                 master=self.master,
                                 x=self.entry.winfo_rootx(),
                                 y=self.entry.winfo_rooty() + self.entry.winfo_reqheight(),
                                 keysize=self.keysize,
                                 keycolor=self.keycolor)

    def _destroy_popup(self): self.kb.destroy()

def test():
    root = tkRoot(Screen_Width=800, Screen_Height=480, x=100, y=100)
    KeyboardEntry(root, keysize=6, keycolor='white').Pack()
    KeyboardEntry(root).Pack()
    root.mainloop()
