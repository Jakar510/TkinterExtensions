# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

import base64
from abc import ABC
from typing import Dict, List, Union

from PIL import Image, ImageTk

from .Frames import *
from .Widgets import *
from .base import *




__all__ = [
        'AnimatedGIF', 'ButtonGrid'
        ]

class ButtonGrid(TkinterFrame, ABC):
    __buttons: Dict[int, Button] = { }
    def __init__(self, *, master: TkinterFrame, rows: int = None, cols: int = None, NumberOfButtons: int = None, **kwargs):
        """
            :param kwargs: Button kwargs
        """
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
            self.__buttons[i] = Button(self, Text=self.ButtonTitles[i], **kwargs)
            self.__buttons[i].grid(row=r, column=c)
            self.__buttons[i].SetCommand(self.ButtonCommands[i])
            c += 1

    def HideAll(self):
        for w in self.__buttons.values(): w.hide()
    def ShowAll(self):
        for w in self.__buttons.values(): w.show()

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

    @property
    def ButtonTitles(self) -> dict: raise NotImplementedError()
    @property
    def ButtonCommands(self) -> dict: raise NotImplementedError()


class AnimatedGIF(Label, object):
    """
    Creates an Animated loading screen with a GIF whose animation is started by AnimatedGIF.Pack/Place/Grid/show and stopped by AnimatedGIF.hide.

    Based off of:
        AnimatedGIF - a class to show an animated gif without blocking the tkinter mainloop()
        Copyright (c) 2016 Ole Jakob Skjelten <olesk@pvv.org>
        Released under the terms of the MIT license (https://opensource.org/licenses/MIT) as described in LICENSE.md
        https://github.com/olesk75/AnimatedGIF/blob/master/AnimatedGif.py
    """
    _callback_id = None
    _is_running: bool = False
    _forever: bool = False

    _loc: int = 0
    _frames: List[ImageTk.PhotoImage] = []
    def __init__(self, master: tk.Widget, *, root: Union[tk.Tk, tk.Toplevel] = None, path: str, forever=True, defaultDelay: int = 100):
        super().__init__(master)
        self._master = master
        self._forever = forever
        self.Root = root

        with Image.open(path) as img:
            assert (isinstance(img, Image.Image))

            try: self._delay = img.info['duration']
            except (AttributeError, KeyError): self._delay = defaultDelay

            i = 0
            while True:
                try:
                    photoframe = ImageTk.PhotoImage(image=img.copy().convert(mode='RGBA'), master=self.Root or self)
                    self._frames.append(photoframe)

                    i += 1
                    img.seek(i)
                except EOFError: break

        self._setFrame()
    def start_animation(self, frame=None):
        if self._is_running: return

        if frame is not None:
            self._loc = 0
            self.configure(image=self._frames[frame])

        self._master.after(self._delay, self._animate_GIF)
        self._is_running = True
    def stop_animation(self):
        if not self._is_running: return

        if self._callback_id is not None:
            self.after_cancel(self._callback_id)
            self._callback_id = None

        self._is_running = False
    def _setFrame(self): self.configure(image=self._frames[self._loc])
    def _animate_GIF(self):
        self._loc += 1
        self._setFrame()

        if self._loc == self._last_index:
            if self._forever:
                self._loc = 0
                self._callback_id = self._master.after(self._delay, self._animate_GIF)
            else:
                self._callback_id = None
                self._is_running = False
        else:
            self._callback_id = self._master.after(self._delay, self._animate_GIF)

    @property
    def _last_index(self) -> int: return len(self._frames) - 1



    def Pack(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super().Pack(**kwargs)
    def Grid(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super().Grid(**kwargs)
    def Place(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super().Place(**kwargs)

    def show(self, start_animation=True):
        if start_animation: self.start_animation()
        super().show()
    def hide(self):
        self.stop_animation()
        super().hide()

    @classmethod
    def FromBase64Data(cls, master, *, root: Union[tk.Tk, tk.Toplevel] = None, data: Union[str, bytes], path: str, forever=True, defaultDelay: int = 100):
        with open(path, 'wb') as fp:
            fp.write(base64.urlsafe_b64decode(data))

        return cls(master, root=root, path=path, forever=forever, defaultDelay=defaultDelay)
