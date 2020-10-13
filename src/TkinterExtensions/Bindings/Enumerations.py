# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

from enum import Enum

from .Raw import *




__all__ = [
        'Bindings'
        # 'Special', 'Mouse', 'UpperCase', 'LowerCase', 'FunctionKeys', 'Custom', 'Core', 'ComboBox', 'ThemedTreeView', 'ListBox', 'Numbers', 'Foucs',
        ]

class Bindings(object):

    class Special(Enum):
        Activate = Activate
        Configure = Configure
        Deactivate = Deactivate
        Destroy = Destroy
        Expose = Expose
        Map = Map
        Motion = Motion
        MouseWheel = MouseWheel
        Unmap = Unmap
        Visibility = Visibility

    class Mouse(Enum):
        B1_Motion = B1_Motion
        B2_Motion = B2_Motion
        Button = Button
        Button1 = Button1
        Button2 = Button2
        Button3 = Button3
        ButtonRelease = ButtonRelease
        ButtonRelease1 = ButtonRelease1
        ButtonRelease2 = ButtonRelease2
        ButtonRelease3 = ButtonRelease3
        Double_Button = Double_Button
        Double_Button2 = Double_Button2
        Double_Button3 = Double_Button3

    # noinspection DuplicatedCode
    class UpperCase(Enum):
        A = A
        B = B
        C = C
        D = D
        E = E
        F = F
        G = G
        H = H
        I = I
        J = J
        K = K
        L = L
        M = M
        N = N
        O = O
        P = P
        Q = Q
        R = R
        S = S
        T = T
        U = U
        V = V
        W = W
        X = X
        Y = Y
        Z = Z

    # noinspection DuplicatedCode
    class LowerCase(Enum):
        a = a
        b = b
        c = c
        d = d
        e = e
        f = f
        g = g
        h = h
        i = i
        j = j
        k = k
        l = l
        m = m
        n = n
        o = o
        p = p
        q = q
        r = r
        s = s
        t = t
        u = u
        v = v
        w = w
        x = x
        y = y
        z = z

    class Custom(Enum):
        ShiftTab = ShiftTab
        ShiftTabEvent = ShiftTabEvent

    class FunctionKeys(Enum):
        F1 = F1
        F2 = F2
        F3 = F3
        F4 = F4
        F5 = F5
        F6 = F6
        F7 = F7
        F8 = F8
        F9 = F9
        F10 = F10
        F11 = F11
        F12 = F12

    class Foucs(Enum):
        Next = Next
        Prior = Prior
        Enter_Boundary = Enter_Boundary
        Leave_Boundary = Leave_Boundary
        FocusIn = FocusIn
        FocusOut = FocusOut

    class Core(Enum):
        Alt_L = Alt_L
        BackSpace = BackSpace
        Cancel = Cancel
        Caps_Lock = Caps_Lock
        Control_L = Control_L
        Delete = Delete
        Down = Down
        End = End
        Enter = Enter
        Escape = Escape
        Home = Home
        Insert = Insert
        KP_Add = KP_Add
        KP_Enter = KP_Enter
        KP_Subtract = KP_Subtract
        Key = Key
        Left = Left
        Minus = Minus
        Num_Lock = Num_Lock
        Pause = Pause
        Plus = Plus
        Print = Print
        Return = Return
        Right = Right
        Scroll_Lock = Scroll_Lock
        Shift = Shift
        Shift_Down = Shift_Down
        Shift_L = Shift_L
        Shift_Left = Shift_Left
        Shift_Right = Shift_Right
        Shift_Up = Shift_Up
        Tab = Tab
        Up = Up

    class ListBox(Enum):
        ListboxSelect = ListboxSelect

    class ComboBox(Enum):
        ComboboxSelected = ComboboxSelected

    class Numbers(Enum):
        zero = zero
        one = one
        two = two
        three = three
        four = four
        five = five
        six = six
        seven = seven
        eight = eight
        nine = nine

    class TreeView(Enum):
        TreeViewSelect = TreeViewSelect

    @staticmethod
    def IsEnter(keysym: str) -> bool: return keysym == Bindings.Core.Enter.value or keysym == Bindings.Core.KP_Enter.value or keysym == Bindings.Core.Return.value
