# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------


import time




__all__ = ['HID_BUFFER', 'TimeKeeperMixin']

class TimeKeeperMixin(object):
    _LastTime = time.time()
    def UpdateTime(self): self._LastTime = time.time()

    @property
    def ElapsedTime(self) -> float: return abs(self.CurrentTime - self._LastTime)

    @property
    def CurrentTime(self) -> float: return time.time()



class HID_BUFFER(TimeKeeperMixin):
    _text = ''
    def Clear(self, s: str = '') -> str:
        if not isinstance(s, str): s = str(s)
        self._text = s
        self.UpdateTime()
        return self._text
    def Add(self, s: str):
        if not isinstance(s, str): s = str(s)
        self._text += s
        self.UpdateTime()
        return self
    def Sub(self, s: str):
        if not isinstance(s, str): s = str(s)
        self._text -= s
        self.UpdateTime()
        return self
    def Backspace(self):
        self._text = self._text[:-1]
        self.UpdateTime()
        return self
    def Backspace_Number(self):
        self.UpdateTime()
        self._text = self._text[:-1]
        if len(self._text) == 0: return self
        if self._text[-1] == '.' or self._text[-1] == ',':
            self._text = self._text[:-2]

        return self


    @property
    def Value(self) -> str: return self._text
    @Value.setter
    def Value(self, v: int or float or str): self._text = str(v)



    def TryReturnAsNumber(self) -> float or str or None:
        """
            tries to convert to number, if fails returns None.
        :return: float or int or None
        """
        try:
            return self.ReturnAsNumber()
        except (ValueError, RuntimeError):
            return None
    def ReturnAsNumber(self) -> float or str:
        """
            Throws RuntimeError if text is empty.
        :return: float
        """
        self.UpdateTime()
        if self._text == '': return ''
        return float(self._text)
    def MultiplyByFactor(self, factor: int or float = -1) -> float or str:
        """
            Throws RuntimeError if text is empty.
        :return: float times a factor (default of -1).
        """
        return self.ReturnAsNumber() * factor

    def format(self, *args, **kwargs) -> str: return self._text.format(*args, **kwargs)
    def __format__(self, format_spec) -> str: return self._text.__format__(format_spec)
    def __contains__(self, item: str) -> bool: return item in self._text
    def __repr__(self) -> str: return f'<{self.__class__.__name__} Object: "{self._text}">'
    def __str__(self) -> str: return self._text


    def __iadd__(self, char: str): return self.Add(char)
    def __add__(self, char: str): return self.Add(char)

    def __isub__(self, char: str): return self.Sub(char)
    def __sub__(self, char: str): return self.Sub(char)

    def __len__(self) -> int: return len(self._text)
