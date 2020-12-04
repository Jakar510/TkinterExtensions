# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

import string
from enum import IntEnum, IntFlag
from typing import *

from .BaseWidgets import *
from .Frames import *
from .Root import *
from .Widgets import *
from .base import *
from ..Events import *
from ..Misc import HID_BUFFER




__all__ = [
        'KeyboardMixin', 'KeyBoardState',
        'PopupKeyboard', 'Placement', 'PlacementSet',
        'value_title_mixin', 'BaseFramed', 'BaseFramedKeyboard', 'BaseTitled', 'BaseTitledKeyboard',
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
    _shift = 'Aa'
    _next = '>>>' or '→'  # &#x2192
    _previous = '<<<' or '←'  # &#x2190
    _enter = '↲'  # &#x21B2
    _backspace = '<-'
    _delete = 'Clr'
    _sign = '±'
    # _close = '[abc]'

    _is_number: bool = False
    _root_frame: Frame
    _Frames: Dict[int, Frame] = { }
    _letters: Dict[int, Dict[int, Button]] = { }
    _numbers: Dict[int, Dict[int, Button]] = { }
    _hid = HID_BUFFER()
    def __init__(self, root: tkRoot, *, attach, x: int, y: int, keysize: int = -1,
                 keycolor: str = 'white', transparency: float = 0.85, takefocus: bool = False, font: str = '-family {Segoe UI Black} -size 13'):
        assert (isinstance(root, tkRoot))
        self.root = root
        tkTopLevel.__init__(self, master=root, fullscreen=False, Screen_Width=root.Screen_Width, Screen_Height=root.Screen_Height, takefocus=takefocus)
        self.overrideredirect(True)
        self.SetTransparency(transparency)

        if not isinstance(attach, KeyboardMixin) and isinstance(attach, BaseTextTkinterWidget): raise TypeError(type(attach), (KeyboardMixin, BaseTextTkinterWidget))
        self.attach = attach

        self._keysize = keysize
        self._keycolor = keycolor

        self._x = x
        self._y = y

        self._root_frame = Frame(self).Grid(row=0, column=0).Grid_ColumnConfigure(0, weight=1).Grid_RowConfigure(0, weight=1)

        Row0: List[str] = [self._backspace] + [str(i) for i in range(10)] + [self._delete]
        Row1: List[str] = ['|', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '/']
        Row2: List[str] = [self._shift, 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ':', '^']
        Row3: List[str] = ['', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?', self._enter]
        Row4: List[str] = ['@', '#', '!', '*', self._space, '-', '_', '+', '=']

        offset = 0
        for r, row in enumerate([Row0, Row1, Row2, Row3, Row4]):
            if r not in self._letters: self._letters[r] = { }
            self._root_frame.Grid_RowConfigure(r, weight=1)
            for c, text in enumerate(row):
                self._root_frame.Grid_ColumnConfigure(c, weight=1)

                if text == '': continue
                w = Button(master=self._root_frame, text=text, bg=self._keycolor, takefocus=takefocus).SetCommand(CurrentValue(self._handle_key_press))

                if self._shift == text: w.Grid(row=r, column=c, rowspan=2)

                elif 'space' in text:
                    w.Grid(row=r, column=c, columnspan=3)
                    offset = 2

                elif self._enter == text: w.Grid(row=r, column=c, rowspan=2)

                else: w.Grid(row=r, column=c + offset)

                self._letters[r][c] = w
        if keysize > 0: self.SetSize(keysize)
        if font: self.SetFont(font)

        self.Bind(Bindings.Key, lambda e: self.attach.destroy_popup())  # destroy _PopupKeyboard on keyboard interrupt


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
            for w in row.values(): w.configure(font=font)

        for row in self._numbers.values():
            for w in row.values(): w.configure(font=font)

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
                    return middle()

                if x_plus_frame_width > root_width:
                    return middle()

                if x_plus_frame_width < root_width and x_minus_frame_width > root_x:
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




    def SwitchCase(self):
        for row in self._letters.values():
            for w in row.values():
                if w.txt not in string.ascii_letters: continue
                if w.txt in string.ascii_uppercase:
                    w.txt = w.txt.lower()
                else:
                    w.txt = w.txt.upper()

        return self._resize()

    def _handle_key_press(self, value: str):
        if value == self._shift: self.SwitchCase()

        elif value == self._space: self._append_space(self.attach)

        elif value == self._enter: self._handle_enter()

        elif value == self._backspace: self._handle_backspace()

        elif value == self._delete:
            self._hid.Value = self.attach.txt = ''

        elif self._handle_navigation(value): pass

        else:
            self._hid += value
            self.attach.txt = self._hid.Value
    def _append_space(self, w):
        if isinstance(w, BaseTextTkinterWidget):
            self._hid.Value = w.txt
            self._hid += ' '
            w.txt = self._hid.Value
    def _handle_backspace(self):
        print('_handle_backspace_', self.attach)
        if isinstance(self.attach, Entry):
            index = self.attach.index(tk.INSERT)
            del self._hid[index]
            self.attach.txt = self._hid.Value

        else:
            self._hid.Value = self.attach.txt
            self._hid.Backspace()
            self.attach.txt = self._hid.Value

    def _handle_navigation(self, value: str) -> bool:
        if value == self._next or value == self._previous:
            if isinstance(self.attach, Entry):
                index = self.attach.index(tk.INSERT)
                if value == self._next:
                    self.attach.icursor(index + 1)
                    return True

                elif value == self._previous:
                    self.attach.icursor(index - 1)
                    return True

                else:
                    self.attach.insert(index, value)
                    return True

            elif isinstance(self.attach, BaseTextTkinterWidget):
                return self._navagate(value)

        return False
    def _navagate(self, value: str) -> bool:
        if value == self._next:
            self.attach.tk_focusNext().focus_set()
            return self._handle_enter()

        elif value == self._previous:
            self.attach.tk_focusPrev().focus_set()
            return self._handle_enter()
    def _handle_enter(self) -> True:
        if isinstance(self.attach, KeyboardMixin):
            self.attach.destroy_popup()
            return True

        raise AttributeError('self.attach.destroy_popup() not found')

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
    kb: Union[PopupKeyboard, None] = None
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
        if self.state == KeyBoardState.Virtual:
            if event.type == EventType.FocusOut:
                self.state = KeyBoardState.Typing
                # self.destroy_popup()

            elif event.type == EventType.KeyPress:
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
            if event.type == EventType.FocusOut:
                self.state = KeyBoardState.Idle

    def _call_popup(self):
        try:
            self.destroy_popup()
        except AttributeError: pass

        self.kb = PopupKeyboard(self.root, attach=self, x=self.x, y=self.y, keycolor=self.keycolor, keysize=self.keysize)

    def destroy_popup(self):
        if self.kb:
            self.kb.destroy()
            self.kb = None


    @staticmethod
    def test_entry_placements(root: tkRoot) -> LabelFrame:
        from .KeyboardEntry import TitledKeyboardEntry  # circular import
        frame = LabelFrame(root, background='light blue', text='ENTRY')

        TitledKeyboardEntry(frame, root=root, title=dict(text='Center Below'), value=dict(keysize=7, placement=PlacementSet(Placement.Center, Placement.Bottom))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Left Below'), value=dict(keysize=6, placement=PlacementSet(Placement.Left, Placement.Bottom))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Right Below'), value=dict(keysize=5, placement=PlacementSet(Placement.Right, Placement.Bottom))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Auto Below'), value=dict(keysize=4, placement=PlacementSet(Placement.Auto, Placement.Bottom))).Pack()

        TitledKeyboardEntry(frame, root=root, title=dict(text='FULL Auto'), value=dict()).Pack()

        TitledKeyboardEntry(frame, root=root, title=dict(text='Center Above'), value=dict(placement=PlacementSet(Placement.Center, Placement.Top))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Left Above'), value=dict(placement=PlacementSet(Placement.Left, Placement.Top))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Right Above'), value=dict(placement=PlacementSet(Placement.Right, Placement.Top))).Pack()
        TitledKeyboardEntry(frame, root=root, title=dict(text='Auto Above'), value=dict(placement=PlacementSet(Placement.Auto, Placement.Top))).Pack()
        return frame
    @staticmethod
    def test_comobobox_placements(root: tkRoot) -> LabelFrame:
        from .KeyboardComboBoxThemed import TitledKeyboardComboBoxThemed  # circular import
        frame = LabelFrame(root, background='light blue', text='COMBO_BOX')

        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Center Below'), value=dict(keysize=7, placement=PlacementSet(Placement.Center, Placement.Bottom))).Pack()
        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Left Below'), value=dict(keysize=6, placement=PlacementSet(Placement.Left, Placement.Bottom))).Pack()
        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Right Below'), value=dict(keysize=5, placement=PlacementSet(Placement.Right, Placement.Bottom))).Pack()
        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Auto Below'), value=dict(keysize=4, placement=PlacementSet(Placement.Auto, Placement.Bottom))).Pack()

        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='FULL Auto'), value=dict()).Pack()

        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Center Above'), value=dict(placement=PlacementSet(Placement.Center, Placement.Top))).Pack()
        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Left Above'), value=dict(placement=PlacementSet(Placement.Left, Placement.Top))).Pack()
        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Right Above'), value=dict(placement=PlacementSet(Placement.Right, Placement.Top))).Pack()
        TitledKeyboardComboBoxThemed(frame, root=root, title=dict(text='Auto Above'), value=dict(placement=PlacementSet(Placement.Auto, Placement.Top))).Pack()
        return frame
    @staticmethod
    def test():
        root = tkRoot(Screen_Width=800, Screen_Height=480, x=200, y=200)
        KeyboardMixin.test_entry_placements(root).Grid(0, 0)
        KeyboardMixin.test_comobobox_placements(root).Grid(0, 1)
        root.mainloop()





class value_title_mixin:
    Title: Label
    Entry: BaseTextTkinterWidget

    @property
    def title(self) -> str: return self.Title.txt
    @title.setter
    def title(self, value: str): self.Title.txt = value

    @property
    def value(self) -> str: return self.Entry.txt
    @value.setter
    def value(self, value: str): self.Entry.txt = value

    @staticmethod
    def AssertKeyBoardType(cls):
        if not (issubclass(cls, BaseTextTkinterWidget) and issubclass(cls, KeyboardMixin)): raise TypeError(type(cls), (BaseTextTkinterWidget, KeyboardMixin))

    @staticmethod
    def AssertType(cls):
        if not (issubclass(cls, BaseTextTkinterWidget)): raise TypeError(type(cls), (BaseTextTkinterWidget,))



class BaseTitled(Frame, value_title_mixin):
    """
        When subclassed, pairs the class type with the title label, wrapped in a grid.

        Example:
            class TitledEntry(BaseTitled):
                def __init__(self, master, *, RowPadding: int = 1, factor: int = 3, value: Dict = { }, title: Dict = { }, cls: Type[Entry] = Entry, **kwargs):
                    assert (issubclass(cls, Entry))
                    BaseTitled.__init__(self, master, cls=cls, value=value, RowPadding=RowPadding, title=title, factor=factor, **kwargs)

    """
    def __init__(self, master, *, cls, RowPadding: int, factor: int, value: Dict, title: Dict, **kwargs):
        value_title_mixin.AssertType(cls)
        Frame.__init__(self, master, **kwargs)
        self.Grid_RowConfigure(0, weight=1).Grid_RowConfigure(1, weight=factor).Grid_ColumnConfigure(0, weight=1)

        self.Title = Label(self, **title).Grid(row=0, column=0, padx=RowPadding, pady=RowPadding)
        # noinspection PyArgumentList
        self.Entry = cls(self, **value).Grid(row=1, column=0, padx=RowPadding, pady=RowPadding)
class BaseTitledKeyboard(Frame, value_title_mixin):
    """
        When subclassed, pairs the class type with the title label, wrapped in a grid.

        Example:
            class TitledKeyboardEntry(BaseTitledKeyboard):
                def __init__(self, master, *, root: tkRoot, RowPadding: int = 1, factor: int = 3, value: Dict = { }, title: Dict = { }, cls: Type[KeyboardEntry] = KeyboardEntry, **kwargs):
                    assert (issubclass(cls, KeyboardEntry))
                    BaseTitledKeyboard.__init__(self, master, cls=cls, root=root, value=value, RowPadding=RowPadding, title=title, factor=factor, **kwargs)

    """
    def __init__(self, master, *, cls, root: tkRoot, RowPadding: int, factor: int, value: Dict, title: Dict, **kwargs):
        value_title_mixin.AssertKeyBoardType(cls)
        Frame.__init__(self, master, **kwargs)
        self.Grid_RowConfigure(0, weight=1).Grid_RowConfigure(1, weight=factor).Grid_ColumnConfigure(0, weight=1)

        self.Title = Label(self, **title).Grid(row=0, column=0, padx=RowPadding, pady=RowPadding)
        self.Entry = cls(self, root=root, **value).Grid(row=1, column=0, padx=RowPadding, pady=RowPadding)




class BaseFramed(LabelFrame, value_title_mixin):
    """
        When subclassed, pairs the class type with the title label, wrapped in a LabelFrame.

        Example:
            class FramedEntry(BaseFramed):
                def __init__(self, master, *, value: Dict = { }, cls: Type[Entry] = Entry, **kwargs):
                    assert (issubclass(cls, Entry))
                    BaseFramed.__init__(self, master, cls=cls, value=value, **kwargs)

    """
    def __init__(self, master, *, cls, value: Dict, **kwargs):
        value_title_mixin.AssertType(cls)
        LabelFrame.__init__(self, master, **kwargs)

        # noinspection PyArgumentList
        self.Entry = cls(self, **value).PlaceFull()
class BaseFramedKeyboard(LabelFrame, value_title_mixin):
    """
        When subclassed, pairs the class type with the title label, wrapped in a LabelFrame.

        Example:
            class FramedKeyboardEntry(BaseFramedKeyboard):
                def __init__(self, master, *, root: tkRoot, value: Dict = { }, cls: Type[KeyboardEntry] = KeyboardEntry, **kwargs):
                    assert (issubclass(cls, KeyboardEntry))
                    BaseFramedKeyboard.__init__(self, master, cls=cls, root=root, value=value, **kwargs)

    """
    def __init__(self, master, *, cls, root: tkRoot, value: Dict, **kwargs):
        value_title_mixin.AssertKeyBoardType(cls)
        LabelFrame.__init__(self, master, **kwargs)

        self.Entry = cls(self, root=root, **value).PlaceFull()

