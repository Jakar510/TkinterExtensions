# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------
import itertools
import os
import sys
import threading
import time
from abc import ABC
from types import FunctionType, MethodType
from typing import Union

from PIL import Image




__all__ = [
        'ResizePhoto', 'CalculateOffset', 'RoundFloat', 'AutoCounter', 'AutoStartThread', 'sizeof', 'IsImage', 'AutoStartTargetedThread', 'Wait', 'IsMethod', 'IsFunction'
        ]

def RoundFloat(Float: float, Precision: int) -> str:
    """ Rounds the Float to the given Precision and returns It as string. """
    return f"{Float:.{Precision}f}"
def ResizePhoto(image: Image.Image, *, WidthMax: int or float, HeightMax: int or float) -> Image:
    scalingFactor = min((WidthMax / image.width, HeightMax / image.height))
    newSize = (int(scalingFactor * image.width), int(scalingFactor * image.height))
    # PRINT('ResizePhoto', dict(newSize=newSize, WidthMax=WidthMax, HeightMax=HeightMax, image=image))
    return image.resize(newSize)
def CalculateOffset(starting: int, *args: Union[int, float]) -> int:
    """
        Example: WrapLength = ScreenWidth * Widget.Parent.relwidth * Widget.relwidth * offset

    :param starting: starting value (such as width or height)
    :param args: a list of float or integers to be cumulatively multiplied together.
    :return:
    """
    for arg in args:
        if not isinstance(arg, (int, float)): arg = float(arg)
        starting *= arg
    return int(starting)



def IsImage(*, directory: str = None, fileName: str = None, path: str = None) -> bool:
    try:
        if directory and fileName: path = os.path.join(directory, fileName)

        assert (os.path.isfile(path))
        with open(path, 'rb') as f:
            with Image.open(f) as img:
                assert (isinstance(img, Image.Image))
                img.verify()
                return True

    except (FileNotFoundError, ValueError, EOFError, Image.UnidentifiedImageError, Image.DecompressionBombError):
        return False


def sizeof(obj):
    size = sys.getsizeof(obj)
    if isinstance(obj, dict): return size + sum(map(sizeof, obj.keys())) + sum(map(sizeof, obj.values()))
    if isinstance(obj, (list, tuple, set, frozenset)): return size + sum(map(sizeof, obj))
    return size


class AutoStartThread(threading.Thread, ABC):
    def __init__(self, *args, Name: str = None, AutoStart: bool = True, Daemon: bool = True, **kwargs):
        if not Name:
            try: Name = self.__class__.__qualname__
            except AttributeError: Name = self.__class__.__name__

        super().__init__(name=Name, args=args, kwargs=kwargs, daemon=Daemon)
        if AutoStart: self.start()
    def run(self): raise NotImplementedError()

class AutoStartTargetedThread(threading.Thread):
    def __init__(self, target: callable, *args, Name: str = None, AutoStart: bool = True, Daemon: bool = True, **kwargs):
        assert (callable(target))
        if not Name:
            try: Name = target.__qualname__
            except AttributeError: Name = target.__name__

        super().__init__(name=Name, target=target, args=args, kwargs=kwargs, daemon=Daemon)
        if AutoStart: self.start()



class AutoCounter(object):
    _counter: itertools.count
    _next: callable
    def __init__(self, *, start: int = 0, step: int = 1):
        self._value = start
        self.reset(start=start, step=step)
    def __call__(self, *args, **kwargs) -> int:
        self._value = self._next()
        return self._value
    def reset(self, *, start: int = 0, step: int = 1):
        self._counter = itertools.count(start=start, step=step)
        self._next = self._counter.__next__

    @property
    def value(self) -> int: return self._value

def Wait(delay: Union[int, float]): time.sleep(delay)



def IsMethod(o) -> bool:
    """
        Checks if passed object is a method

        https://stackoverflow.com/questions/37455426/advantages-of-using-methodtype-in-python
    :param o: object being checked
    :type o: any
    :return: weather it is a method
    :rtype: bool
    """
    return isinstance(o, MethodType)
def IsFunction(o) -> bool:
    """
        Checks if passed object is a function

        https://stackoverflow.com/questions/37455426/advantages-of-using-methodtype-in-python
    :param o: object being checked
    :type o: any
    :return: weather it is a method
    :rtype: bool
    """
    return isinstance(o, FunctionType)
