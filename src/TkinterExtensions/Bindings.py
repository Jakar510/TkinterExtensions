# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

__all__ = ['KeyBindings']

class KeyBindings(object):
    Return = 'Return'
    Delete = 'Delete'
    BackSpace = 'BackSpace'
    Minus = 'minus'
    KP_Enter = 'KP_Enter'
    Enter = 'Enter'

    Tab = 'Tab'
    ShiftTab = 'ShiftTab'
    ShiftTabEvent = '<Shift-KeyPress-Tab>'

    bindKey = '<Key>'
    bindButton = "<Button>"
    ListboxSelect = "<<ListboxSelect>>"
    ComboboxSelected = "<<ComboboxSelected>>"
    TreeViewSelect = "<<TreeviewSelect>>"

    bindF4 = '<F4>'
    F4 = 'F4'

    bindF5 = '<F5>'
    F5 = 'F5'

    bindF8 = '<F8>'
    F8 = 'F8'

    F12 = 'F12'
    bindF12 = '<F12>'

    bindF11 = '<F11>'
    F11 = 'F11'

    @staticmethod
    def isEnter(keysym: str) -> bool:
        return keysym == KeyBindings.Enter or keysym == KeyBindings.KP_Enter or keysym == KeyBindings.Return
