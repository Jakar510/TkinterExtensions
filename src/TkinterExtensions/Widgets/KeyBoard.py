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




class _PopupKeyboard(TopLevel):
    '''A Toplevel instance that displays a keyboard that is attached to
    another widget. Only the Entry widget has a subclass in this version.
    '''
    def __init__(self, master, attach, x, y, keycolor, keysize=5, takefocus: bool = False):
        super().__init__(master=master, takefocus=takefocus)

        self.overrideredirect(True)
        self.attributes('-alpha', 0.85)

        self.master = master
        self.attach = attach
        self.keysize = keysize
        self.keycolor = keycolor
        self.x = x
        self.y = y

        self.Frames: Dict[int, Frame] = {}
        self._buttons: Dict[int, Dict[int, Dict[int, Button]]] = { }

        self._init_keys()

        self.bind('<Key>', lambda e: self.destroy()) # destroy _PopupKeyboard on keyboard interrupt

        # resize to fit keys
        self.update_idletasks()
        self.update()
        newGeometry = f'{self.frame.width}x{self.frame.height}+{self.x}+{self.y}'
        self.geometry(newGeometry)

    def _init_keys(self):
        self.frame = Frame(self).Grid(row=0, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)
        self.Frames[0] = Frame(self.frame).Grid(row=1, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)
        self.Frames[1] = Frame(self.frame).Grid(row=2, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)
        self.Frames[2] = Frame(self.frame).Grid(row=3, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)
        self.Frames[3] = Frame(self.frame).Grid(row=4, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)

        Row1: List[str] = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '/']
        Row2: List[str] = ['<<<', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ',', '>>>']
        Row3: List[str] = ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '.', '?', '[1,2,3]']
        Row4: List[str] = ['@', '#', '%', '*', '[ space ]', '+', '-', '=']
        Rows: List[List[str]] = [Row1, Row2, Row3, Row4]

        for r, row in enumerate(Rows):
            if r not in self._buttons: self._buttons[r] = {}
            self.frame.Grid_RowConfigure(r, weight=1)
            for c, text in enumerate(row):
                if c not in self._buttons[r]: self._buttons[r][c] = {}
                self.frame.Grid_ColumnConfigure(c, weight=1)
                # size = self.keysize * 3 if 'space' in text else self.keysize
                self._buttons[r][c] = Button(master=self.Frames[r], Text=text, bg=self.keycolor).Grid(row=r, column=c).SetCommand(self._attach_key_press, z=text)

        # for i, k in enumerate(Row1):
        #     # Button(master=self.Row1, text=k, width=self.keysize, bg=self.keycolor).Grid(row=0, column=i).SetCommand(self._attach_key_press, z=k)
        #     Button(master=self.frame, text=k, width=self.keysize, bg=self.keycolor).Grid(row=0, column=i).SetCommand(self._attach_key_press, z=k)
        #
        # for i, k in enumerate(Row2):
        #     # Button(master=self.Row2, text=k, width=self.keysize, bg=self.keycolor).Grid(row=0, column=i).SetCommand(self._attach_key_press, z=k)
        #     Button(master=self.frame, text=k, width=self.keysize, bg=self.keycolor).Grid(row=1, column=i).SetCommand(self._attach_key_press, z=k)
        #
        # for i, k in enumerate(Row3):
        #     # Button(master=self.Row3, text=k, width=self.keysize, bg=self.keycolor).Grid(row=0, column=i).SetCommand(self._attach_key_press, z=k)
        #     Button(master=self.frame, text=k, width=self.keysize, bg=self.keycolor).Grid(row=2, column=i).SetCommand(self._attach_key_press, z=k)



    def _attach_key_press(self, k):
        if k == '>>>':
            self.attach.tk_focusNext().focus_set()
            self.destroy()
        elif k == '<<<':
            self.attach.tk_focusPrev().focus_set()
            self.destroy()
        elif k == '[1,2,3]':
            pass
        elif k == '[ space ]':
            self.attach.insert(tk.END, ' ')
        else:
            self.attach.insert(tk.END, k)


'''
TO-DO: Implement Number Pad
class _PopupNumpad(Toplevel):
    def __init__(self, x, y, keycolor='gray', keysize=5):
        Toplevel.__init__(self, takefocus=0)

        self.overrideredirect(True)
        self.attributes('-alpha',0.85)

        self.numframe = Frame(self)
        self.numframe.grid(row=1, column=1)

        self.__init_nums()

        self.update_idletasks()
        self.geometry('{}x{}+{}+{}'.format(self.winfo_width(),
                                           self.winfo_height(),
                                           self.x,self.y))

    def __init_nums(self):
        i=0
        for num in ['7','4','1','8','5','2','9','6','3']:
            print num
            Button(self.numframe,
                   text=num,
                   width=int(self.keysize/2),
                   bg=self.keycolor,
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
    of accepting all existing args, plus a keysize and keycolor option.
    Will pop up an instance of _PopupKeyboard when focus moves into
    the widget

    Usage:
    KeyboardEntry(master, keysize=6, keycolor='white').pack()
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
    root = Root(Screen_Width=800, Screen_Height=480)
    KeyboardEntry(root, keysize=6, keycolor='white').Pack()
    KeyboardEntry(root).Pack()
    root.mainloop()
