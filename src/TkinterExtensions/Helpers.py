# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------
import itertools
import os
import sys
import threading
from typing import Union

from PIL import Image




__all__ = [
        'ResizePhoto', 'CalculateWrapLength', 'RoundFloat', 'AutoCounter', 'AutoStartThread', 'lazy_property', 'sizeof', 'IsImage',
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


class AutoStartThread(threading.Thread):
    def __init__(self, Target: callable, *args, Name: str = None, AutoStart: bool = True, Daemon: bool = True, **kwargs):
        assert (callable(Target))
        if Name == '' or Name is None: Name = Target.__name__
        threading.Thread.__init__(self, name=Name, target=Target, args=args, kwargs=kwargs, daemon=Daemon)
        if AutoStart: self.start()


class lazy_property(object):
    """A @property that is only evaluated once."""
    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self._func = func

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        value = self._func(obj)
        setattr(obj, self._func.__name__, value)
        return value


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
