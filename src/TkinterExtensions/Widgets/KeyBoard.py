# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

import string
from enum import IntEnum, IntFlag
from typing import Dict, List, Union

from .BaseWidgets import *
from .Frames import *
from .Root import *
from .Widgets import *
from .base import *
from ..Events import *




__all__ = [
        'KeyboardMixin', 'KeyBoardState',
        'PopupKeyboard', 'Placement', 'PlacementSet',
        ]




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



class PopupKeyboard(tkTopLevel):
    """
    A Toplevel instance that displays a keyboard that is attached to another widget.
    Only the Entry widget has a subclass in this version.
    https://www.alt-codes.net/arrow_alt_codes.php
    """
    # _number = '[1,2,3]'
    _space = '[ space ]'
    _shift = 'shift'
    _next = '>>>' or '→'  # &#x2192
    _previous = '<<<' or '←'  # &#x2190
    _enter = '↲'  # &#x21B2
    _backspace = '<-'
    _delete = '->'
    _sign = '±'
    # _close = '[abc]'

    _is_number: bool = False

    _Frames: Dict[int, Frame] = { }
    _letters: Dict[int, Dict[int, Button]] = { }
    _numbers: Dict[int, Dict[int, Button]] = { }

    def __init__(self, root: tkRoot, *, attach, x: int, y: int,
                 keycolor: str = 'white', keysize: int = -1, font: str = '-family {Segoe UI Black} -size 12 -underline 0 -overstrike 0', takefocus: bool = False):
        # PRINT('__PopupKeyboard__', root=root, entry=attach, x=x, y=y, keysize=keysize, keycolor=keycolor, takefocus=takefocus)
        assert (isinstance(root, tkRoot))
        self.root = root
        super().__init__(master=root, fullscreen=False, Screen_Width=root.Screen_Width, Screen_Height=root.Screen_Height, takefocus=takefocus)
        self.overrideredirect(True)
        self.SetTransparency(0.85)

        if not isinstance(attach, KeyboardMixin) and isinstance(attach, BaseTextTkinterWidget): raise TypeError(type(attach), (KeyboardMixin, BaseTextTkinterWidget))
        self.attach: KeyboardMixin = attach

        self._keysize = keysize
        self._keycolor = keycolor

        self._x = x
        self._y = y

        self._init_keys()
        if keysize > 0: self.SetSize(keysize)
        if font: self.SetFont(font)

        self.Bind(Bindings.Key, lambda e: self.attach.destroy_popup())  # destroy _PopupKeyboard on keyboard interrupt

    def _init_keys(self):
        self._root_frame = Frame(self).Grid(row=0, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)
        self._create_letters()
        # self._create_numbers()

    # def _create_numbers(self):
    #     self._numbers_frame = Frame(self._root_frame).Grid(row=0, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)
    #
    #     Row1: List[str] = [self._backspace, self._close]
    #     Row2: List[str] = ['7', '8', '9', self._sign]
    #     Row3: List[str] = ['4', '5', '6']
    #     Row4: List[str] = ['1', '2', '3', self._enter]
    #     Row5: List[str] = ['0', '.']
    #
    #     offset = 0
    #     for r, row in enumerate([Row1, Row2, Row3, Row4, Row5]):
    #         if r not in self._numbers: self._numbers[r] = { }
    #         self._numbers_frame.Grid_RowConfigure(r, weight=1)
    #         for c, text in enumerate(row):
    #             self._numbers_frame.Grid_ColumnConfigure(c, weight=1)
    #             self._numbers[r][c] = w = Button(master=self._numbers_frame, text=text, bg=self._keycolor).SetCommand(self._attach_key_press, z=text)
    #
    #             if self._sign == text:
    #                 w.Grid(row=r, column=c, rowspan=2)
    #             elif self._enter == text:
    #                 w.Grid(row=r, column=c, rowspan=2)
    #             elif self._backspace == text:
    #                 w.Grid(row=r, column=c, columnspan=2)
    #             elif self._close == text:
    #                 w.Grid(row=r, column=c + 1, columnspan=2)
    #             elif '0' == text:
    #                 w.Grid(row=r, column=c, columnspan=2)
    #                 offset = 1
    #             else:
    #                 w.Grid(row=r, column=c + offset)
    #
    #     self._numbers_frame.hide()
    def _create_letters(self):
        self._letters_frame = Frame(self._root_frame).Grid(row=0, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)

        Row0: List[str] = [self._previous] + [str(i) for i in range(10)] + [self._next]
        Row1: List[str] = [self._backspace, 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '/']
        Row2: List[str] = ['|', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':', ';']
        Row3: List[str] = [self._shift, 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?', self._enter]  # self._number
        Row4: List[str] = ['@', '#', '%', '*', self._space, '+', '-', '_', '=']

        offset = 0
        for r, row in enumerate([Row0, Row1, Row2, Row3, Row4]):
            if r not in self._letters: self._letters[r] = { }
            self._root_frame.Grid_RowConfigure(r, weight=1)
            for c, text in enumerate(row):
                self._root_frame.Grid_ColumnConfigure(c, weight=1)
                self._letters[r][c] = w = Button(master=self._letters_frame, text=text, bg=self._keycolor).SetCommand(self._attach_key_press, z=text)

                if 'space' in text:
                    w.Grid(row=r, column=c, columnspan=3)
                    offset = 2
                elif self._enter == text:
                    w.Grid(row=r, column=c, rowspan=2)
                # elif self._backspace == text:
                #     w.Grid(row=r, column=c, columnspan=2)
                else: w.Grid(row=r, column=c + offset)



    def SetSize(self, size: int):
        self._keysize = size

        for row in self._letters.values():
            for w in row.values():
                w.configure(width=size)

        for row in self._numbers.values():
            for w in row.values():
                w.configure(width=size)
        return self._resize()

    def SetFont(self, font: str):
        for row in self._letters.values():
            for w in row.values():
                w.configure(font=font)

        for row in self._numbers.values():
            for w in row.values():
                w.configure(font=font)
        return self._resize()

    def _resize(self):
        # resize to fit keys
        self.update_idletasks()
        self.update()

        self._SetDimmensions(frame_width=self._root_frame.width, frame_height=self._root_frame.height, entry_width=self.attach.width, entry_height=self.attach.height)

        # PRINT('__resize__', size=self._keysize, width=self.width, root_width=self.root.width, _break=self.root.width >= self.width)
        return self
    def _SetDimmensions(self, frame_width: int, frame_height: int, entry_width: int, entry_height: int):
        y = self._get_y(y=self._y, frame_height=frame_height, entry_height=entry_height, placement=self.attach.placement)
        x = self._get_x(x=self._x, frame_width=frame_width, entry_width=entry_width, placement=self.attach.placement)
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
            pass
            # PRINT('__get_x__',
            #       x=x,
            #       root_width=root_width,
            #       root_x=root_x,
            #       middle=middle(),
            #       right=right(),
            #       left=left(),
            #       center=center(),
            #       x_plus_frame_width=x_plus_frame_width,
            #       x_minus_frame_width=x_minus_frame_width,
            #       frame_width=frame_width,
            #       entry_width=entry_width,
            #       placement=placement)

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
            pass
            # PRINT('__get_y__',
            #       y=y,
            #       root_height=root_height,
            #       root_y=root_y,
            #       above=above(),
            #       below=below(),
            #       frame_height=frame_height,
            #       entry_height=entry_height,
            #       placement=placement)

        raise ValueError(f'self.entry.position is unknown. {placement}')




    # def _switchModes(self):
    #     if self._is_number:
    #         self._numbers_frame.hide()
    #         self._letters_frame.show()
    #         self._is_number = False
    #     else:
    #         self._numbers_frame.show()
    #         self._letters_frame.hide()
    #         self._is_number = True
    #
    #     return self._resize()
    def SwitchCase(self):
        for row in self._letters.values():
            for w in row.values():
                if w.txt not in string.ascii_letters: continue
                if w.txt in string.ascii_uppercase:
                    w.txt = w.txt.lower()
                else:
                    w.txt = w.txt.upper()

        return self._resize()

    def _attach_key_press(self, value: str):
        if isinstance(self.attach, Entry):
            index = self.attach.index(tk.INSERT)
            if value == self._next:
                self.attach.icursor(index + 1)

            elif value == self._previous:
                self.attach.icursor(index - 1)

            elif value == self._space: self.attach.insert(index, ' ')

            elif value == self._shift: self.SwitchCase()

            elif value == self._enter:
                if isinstance(self.attach, KeyboardMixin):
                    self.attach.destroy_popup()
                else:
                    raise AttributeError('self.attach.destroy_popup() not found')

            else: self.attach.insert(index, value)

        else:
            if value == self._next:
                self.attach.tk_focusNext().focus_set()
                self.attach.destroy_popup()

            elif value == self._previous:
                self.attach.tk_focusPrev().focus_set()
                self.attach.destroy_popup()

            elif value == self._space: self.attach.Append(' ')

            elif value == self._shift: self.SwitchCase()

            elif value == self._enter: self.attach.destroy_popup()

            else: self.attach.Append(value)



class KeyboardMixin:
    """
    Popup Keyboard is a module to be used with Python's Tkinter library
    It subclasses the Entry widget as KeyboardEntry to make a pop-up keyboard appear when the widget gains focus.
    Still early in development.


    An extension/subclass of the Tkinter Entry widget, capable
    of accepting all existing args, plus a _keysize and _keycolor option.
    Will pop up an instance of _PopupKeyboard when focus moves into
    the widget

    Usage:
    KeyboardEntry(master, keysize=6, keycolor='white').pack()

    Example Class:

        class KeyboardEntry(Entry, KeyboardMixin):
            def __init__(self, master, *,
                         root: tkRoot,
                         placement: PlacementSet = PlacementSet(Placement.Auto),
                         keysize: int = None,
                         keycolor: str = None,
                         insertbackground: str = 'red',
                         insertborderwidth: int = 3,
                         insertofftime: int = 1,
                         insertontime: int = 1,
                         insertwidth: int = 3,
                         text: str = '',
                         Override_var: tk.StringVar = None,
                         Color: dict = None, **kwargs):
                Entry.__init__(self, master,
                               text=text,
                               Override_var=Override_var,
                               Color=Color,
                               insertbackground=insertbackground,
                               insertborderwidth=insertborderwidth,
                               insertofftime=insertofftime,
                               insertontime=insertontime,
                               insertwidth=insertwidth,
                               **kwargs)
                KeyboardMixin.__init__(self,
                                       master,
                                       root=root,
                                       placement=placement,
                                       keysize=keysize,
                                       keycolor=keycolor)

    """
    kb: Union[PopupKeyboard, None]
    Bind: callable
    tk_focusNext: callable
    tk_focusPrev: callable
    Append: callable
    insert: callable

    width: int
    height: int
    x: int
    y: int
    def __init__(self, master, *, root: tkRoot, placement: PlacementSet = PlacementSet(Placement.Auto), keysize: int = None, keycolor: str = None):
        if not isinstance(self, BaseTextTkinterWidget) and isinstance(self, KeyboardMixin):
            raise TypeError(f'{self.__class__.__name__} must be used on a sub-class of {BaseTextTkinterWidget}')

        self.master = master

        assert (isinstance(root, tkRoot))
        self.root = root

        self.placement = placement

        self.keysize = keysize or -1
        self.keycolor = keycolor

        self.state: KeyBoardState = KeyBoardState.Idle

        self.Bind(Bindings.FocusIn, self._check_state)
        self.Bind(Bindings.FocusOut, self._check_state)
        self.Bind(Bindings.Key, self._check_state)
        self.Bind(Bindings.ButtonPress, self._check_state)


    def _check_state(self, e: tkEvent): return self._handle_event_(TkinterEvent(e))
    def _handle_event_(self, event: TkinterEvent):
        print(event)
        if self.state == KeyBoardState.Virtual:
            if event == EventType.FocusOut:
                self.destroy_popup()
                self.state = KeyBoardState.Typing

            elif event == EventType.KeyPress:
                self.destroy_popup()
                self.state = KeyBoardState.Typing
                self.Append(event.char)

            elif event.type == EventType.ButtonPress:
                self._call_popup()
                self.state = KeyBoardState.Virtual

        elif self.state == KeyBoardState.Idle:
            if event.type == EventType.FocusIn:
                self._call_popup()
                self.state = KeyBoardState.Virtual

        elif self.state == KeyBoardState.Typing:
            if event == EventType.FocusOut:
                self.state = KeyBoardState.Idle

    def _call_popup(self):
        try:
            self.destroy_popup()
        except AttributeError: pass

        self.kb = PopupKeyboard(self.root, attach=self, x=self.x, y=self.y, keycolor=self.keycolor, keysize=self.keysize)

    def destroy_popup(self):
        self.kb.destroy()
        self.kb = None
        # self.state = KeyBoardState.Idle


    @staticmethod
    def test_entry_placements(root: tkRoot) -> LabelFrame:
        from .KeyboardEntry import TitledKeyboardEntry # circular import
        frame = LabelFrame(root, background='light blue', text='ENTRY')

        TitledKeyboardEntry(frame, root=root, title=dict(text='Center Below'), entry=dict(keysize=7, placement=PlacementSet(Placement.Center, Placement.Bottom))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Left Below'), entry=dict(keysize=6, placement=PlacementSet(Placement.Left, Placement.Bottom))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Right Below'), entry=dict(keysize=5, placement=PlacementSet(Placement.Right, Placement.Bottom))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Auto Below'), entry=dict(keysize=4, placement=PlacementSet(Placement.Auto, Placement.Bottom))).Pack()

        TitledKeyboardEntry(frame, root=root, title=dict(text='FULL Auto'), entry=dict()).Pack()

        TitledKeyboardEntry(frame, root=root, title=dict(text='Center Above'), entry=dict(placement=PlacementSet(Placement.Center, Placement.Top))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Left Above'), entry=dict(placement=PlacementSet(Placement.Left, Placement.Top))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Right Above'), entry=dict(placement=PlacementSet(Placement.Right, Placement.Top))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Auto Above'), entry=dict(placement=PlacementSet(Placement.Auto, Placement.Top))).Pack()
        return frame
    @staticmethod
    def test_comobobox_placements(root: tkRoot) -> LabelFrame:
        from .KeyboardComboBoxThemed import TitledKeyboardComboBoxThemed # circular import
        frame = LabelFrame(root, background='light blue', text='COMBO_BOX')

        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Center Below'), comobobox=dict(keysize=7, placement=PlacementSet(Placement.Center, Placement.Bottom))).Pack()
        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Left Below'), comobobox=dict(keysize=6, placement=PlacementSet(Placement.Left, Placement.Bottom))).Pack()
        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Right Below'), comobobox=dict(keysize=5, placement=PlacementSet(Placement.Right, Placement.Bottom))).Pack()
        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Auto Below'), comobobox=dict(keysize=4, placement=PlacementSet(Placement.Auto, Placement.Bottom))).Pack()

        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='FULL Auto'), comobobox=dict()).Pack()

        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Center Above'), comobobox=dict(placement=PlacementSet(Placement.Center, Placement.Top))).Pack()
        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Left Above'), comobobox=dict(placement=PlacementSet(Placement.Left, Placement.Top))).Pack()
        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Right Above'), comobobox=dict(placement=PlacementSet(Placement.Right, Placement.Top))).Pack()
        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Auto Above'), comobobox=dict(placement=PlacementSet(Placement.Auto, Placement.Top))).Pack()
        return frame
    @staticmethod
    def test():
        root = tkRoot(Screen_Width=800, Screen_Height=480, x=200, y=200)
        KeyboardMixin.test_entry_placements(root).Grid(0, 0)
        KeyboardMixin.test_comobobox_placements(root).Grid(0, 1)
        root.mainloop()
