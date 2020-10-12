# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------
from .Enumerations import *
from .Bindings import KeyBindings
from .Frames import *
from .base import *
from .BaseWidgets import *




__all__ = [
        'TkinterTreeView', 'TkinterTreeViewHolder', 'TkinterComboBox', 'ThemedTkinterButton', 'ThemedTkinterEntry', 'ThemedTkinterLabel',
        ]

"""
Button
CheckButton
--ComoboBox
Entry
Frame
LabelFrame
Label
Notebook
PanedWidnow
ProgressBar
RadioButton
Scale
Separator
SizeGrip
--TreeView
"""

class TkinterComboBox(ttk.Combobox, BaseTextTkinterWidget, CommandMixin):
    """Construct a Ttk Combobox _widget with the parent master.

    STANDARD OPTIONS

        class, cursor, style, takefocus

    WIDGET-SPECIFIC OPTIONS

        exportselection
        postcommand

        textvariable

        values

        justify
        state
        height
        width
    """
    def __init__(self, master, Text: str = '', Override_var: tk.StringVar = None, **kwargs):
        ttk.Combobox.__init__(self, master=master, **kwargs)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, Text=Text)

    @property
    def value(self) -> bool: return self._txt.get()
    @value.setter
    def value(self, v: str): self._txt.set(v)

    def _setCommand(self):
        self.bind(KeyBindings.ComboboxSelected, self._cmd)
        return self

    def SetValues(self, values: list or tuple):
        self.configure(values=values)


class TkinterTreeView(ttk.Treeview, BaseTkinterWidget, CommandMixin):
    def __init__(self, master: tk.Frame, Color: dict = None, **kwargs):
        ttk.Treeview.__init__(self, master=master, **kwargs)
        if Color:
            self.configure(activebackground=Color['ABG'])
            self.configure(activeforeground=Color['AFG'])
            self.configure(background=Color['BG'])
            self.configure(disabledforeground=Color['DFG'])
            self.configure(foreground=Color['FG'])
            self.configure(highlightbackground=Color['HBG'])
            self.configure(highlightcolor=Color['HFG'])

    def _setCommand(self):
        self.bind(KeyBindings.TreeViewSelect, self._cmd)
        return self

    def SetTags(self, tags: dict):
        if tags:
            for tag, kwargs in tags.items():
                self.tag_configure(tag, **kwargs)
    def Clear(self): self.delete(*self.get_children())
    def SetItems(self, items: list or tuple or dict, *, clear: bool = True):
        assert (isinstance(items, (list, tuple, dict)))
        if clear: self.Clear()
        self._json_tree(tree=self, parent='', dictionary=items)
    def _json_tree(self, tree: ttk.Treeview, parent: str, dictionary: list or tuple or dict):
        GroupName = ''
        for key in dictionary:
            try:
                uid, GroupName = key.split('=')
            except (AttributeError, ValueError):
                uid = key
            if isinstance(dictionary[key], dict):
                tree.insert(parent, 'end', uid, text=key)
                self._json_tree(tree, uid, dictionary[key])

            elif isinstance(dictionary[key], (list, tuple)):
                tree.insert(parent, 'end', uid, text=GroupName)
                result = { }
                for x in dictionary[key]:
                    k, v = x.split('=')
                    result[k] = v
                self._json_tree(tree, uid, result)

            else:
                value = dictionary[key]
                if value is None:
                    value = 'None'
                tree.insert(parent, 'end', uid, text=value)  # text=key, value=value)
class TkinterTreeViewHolder(TkinterFrame):
    """Construct a Ttk Treeview with parent scale.

    STANDARD OPTIONS
        class, cursor, style, takefocus, xscrollcommand,
        yscrollcommand

    WIDGET-SPECIFIC OPTIONS
        columns, displaycolumns, height, padding, selectmode, show

    ITEM OPTIONS
        text, image, values, open, tags

    TAG OPTIONS
        foreground, background, font, image

    --------------------------------------------------------------
    Also creates ttk.scrollbar and the frame that conatins
    both TreeView and ScrollBar objects
    """
    TreeView: TkinterTreeView
    vsb: ttk.Scrollbar
    def __init__(self, master, backgroundColor: str, **kwargs):
        TkinterFrame.__init__(self, master=master, bg=backgroundColor, **kwargs)

        self.TreeView = TkinterTreeView(master=self, **kwargs)
        self.TreeView.pack(side='left', fill=tk.BOTH, expand=1)

        self.vsb = ttk.Scrollbar(master=self, orient="vertical", command=self)
        self.vsb.pack(side='right', fill='y')
        self.vsb.pi = self.vsb.place_info()
        self.TreeView.configure(yscrollcommand=self.vsb.set)


class ThemedTkinterButton(ttk.Button, BaseTextTkinterWidget, ImageMixin, CommandMixin):
    """Construct a button _widget with the parent MASTER.

        STANDARD OPTIONS

            activebackground, activeforeground, anchor,
            background, bitmap, borderwidth, cursor,
            disabledforeground, font, foreground
            highlightbackground, highlightcolor,
            highlightthickness, image, justify,
            padx, pady, relief, repeatdelay,
            repeatinterval, takefocus, text,
            textvariable, underline, wraplength

        WIDGET-SPECIFIC OPTIONS

        command, compound, default, height,
        overrelief, state, width
    """
    def __init__(self, master, Text: str = '', Override_var: tk.StringVar = None, Color: dict = None, Command: callable = None, **kwargs):
        ttk.Button.__init__(self, master=master, **kwargs)
        cmd = kwargs.pop('command', None)
        if cmd: self.SetCommand(cmd)
        if Color:
            self.configure(activebackground=Color['ABG'])
            self.configure(activeforeground=Color['AFG'])
            self.configure(background=Color['BG'])
            self.configure(disabledforeground='black')
            self.configure(foreground=Color['FG'])
            self.configure(highlightbackground='light gray')
            self.configure(highlightcolor='black')
            self.configure(highlightbackground=Color['HBG'])
            self.configure(highlightcolor=Color['HFG'])

        if Command: self.SetCommand(Command)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, Text=Text)


class ThemedTkinterLabel(ttk.Label, BaseTextTkinterWidget, ImageMixin):
    __doc__ = """Construct a label _widget with the parent MASTER.

    STANDARD OPTIONS

        activebackground, activeforeground, anchor,
        background, bitmap, borderwidth, cursor,
        disabledforeground, font, foreground,
        highlightbackground, highlightcolor,
        highlightthickness, image, justify,
        padx, pady, relief, takefocus, text,
        textvariable, underline, wraplength

    WIDGET-SPECIFIC OPTIONS

        height, state, width

    """
    def __init__(self, master, Text: str = '', Override_var: tk.StringVar = None, Color: dict = None, **kwargs):
        ttk.Label.__init__(self, master=master, **kwargs)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, Text=Text)

        if Color:
            self.configure(activebackground=Color['ABG'])
            self.configure(activeforeground=Color['AFG'])
            self.configure(background=Color['BG'])
            self.configure(disabledforeground='black')
            self.configure(foreground=Color['FG'])
            self.configure(highlightbackground='light gray')
            self.configure(highlightcolor='black')
            self.configure(highlightbackground=Color['HBG'])
            self.configure(highlightcolor=Color['HFG'])


class ThemedTkinterEntry(ttk.Entry, BaseTextTkinterWidget, CommandMixin):
    __doc__ = """Construct an entry _widget with the parent MASTER.

    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, highlightbackground,
    highlightcolor, highlightthickness, insertbackground,
    insertborderwidth, insertofftime, insertontime, insertwidth,
    invalidcommand, invcmd, justify, relief, selectbackground,
    selectborderwidth, selectforeground, show, state, takefocus,
    textvariable, validate, validatecommand, vcmd, width,
    xscrollcommand.
    """
    def __init__(self, master, Color: dict = None, Text: str = '', Override_var: tk.StringVar = None, **kwargs):
        ttk.Entry.__init__(self, master=master, **kwargs)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, Text=Text)
        if Color:
            self.configure(background=Color['BG'])
            self.configure(disabledforeground='black')
            self.configure(foreground=Color['FG'])
            self.configure(highlightbackground='light gray')
            self.configure(highlightcolor='black')
            self.configure(highlightbackground=Color['HBG'])
            self.configure(highlightcolor=Color['HFG'])

    def Clear(self): self.delete(0, Tags.End.value)

    def _setCommand(self):
        self.bind(KeyBindings.bindButton, self._cmd)
        return self

    @property
    def txt(self) -> str: return self.get()
    @txt.setter
    def txt(self, value: str):
        self.Clear()
        self.insert(Tags.End.value, value)

    def Append(self, value: str):
        self.insert(Tags.End.value, value)
