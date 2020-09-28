# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

from typing import Union

from PIL import Image




__all__ = [
        'ResizePhoto', 'CalculateWrapLength', 'RoundFloat',
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
