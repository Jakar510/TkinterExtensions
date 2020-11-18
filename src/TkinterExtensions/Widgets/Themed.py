# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------
from enum import Enum
from typing import Dict, List, Tuple, Union

from PythonDebugTools import PRINT

from .BaseWidgets import *
from ..Events import Bindings, TkinterEvent
from ..Misc.Enumerations import *
from ..Widgets.Frames import *
from ..Widgets.base import *




__all__ = [
        'TreeViewThemed', 'TreeViewHolderThemed', 'ComboBoxThemed', 'ButtonThemed', 'EntryThemed', 'LabelThemed', 'NotebookThemed',
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
--ThemedTreeView
"""

class ComboBoxThemed(ttk.Combobox, BaseTextTkinterWidget, CommandMixin):
    """Construct a Ttk Combobox _widget with the master master.

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
    def __init__(self, master, text: str = '', Override_var: tk.StringVar = None, Color: dict = None, **kwargs):
        ttk.Combobox.__init__(self, master=master, **kwargs)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, text=text, Color=Color)

    @property
    def value(self) -> bool: return self._txt.get()
    @value.setter
    def value(self, v: str): self._txt.set(v)

    def _setCommand(self):
        self.bind(Bindings.ComboboxSelected.value, self._cmd)
        return self

    def SetValues(self, values: list or tuple):
        self.configure(values=values)

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)



class ScrollbarThemed(ttk.Scrollbar, BaseTkinterWidget):
    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)


class DelimiterError(Exception): pass
class TreeViewThemed(ttk.Treeview, BaseTkinterWidget, CommandMixin):
    last_focus: int or str
    focus_tags: List[str] = []
    def __init__(self, master: tk.Frame, Color: dict = None, **kwargs):
        ttk.Treeview.__init__(self, master=master, **kwargs)
        BaseTkinterWidget.__init__(self, Color)

    def _setCommand(self):
        self.bind(Bindings.TreeViewSelect.value, self._cmd)
        return self

    def SetTags(self, tags: dict):
        if tags:
            for tag, kwargs in tags.items():
                self.tag_configure(tag, **kwargs)
    def Clear(self): self.delete(*self.get_children())
    def SetItems(self, items: list or tuple or dict, *, clear: bool = True):
        assert (isinstance(items, (list, tuple, dict)))
        if clear: self.Clear()
        self._json_tree(tree=self, parent='', d=items)
    def _json_tree(self, tree: ttk.Treeview, parent: str,
                   d: Union[List, Tuple, Dict[str, Union[List, Tuple, Dict[str, Union[List, Tuple, Dict[str, Union[List, Tuple, Dict, str]], str]], str]]]):
        GroupName = ''
        if isinstance(d, dict):
            for key, value in d.items():
                try:
                    uid, GroupName = key.split('=')
                except (AttributeError, ValueError):
                    uid = key
                if isinstance(value, dict):
                    tree.insert(parent, tk.END, uid, text=key)
                    self._json_tree(tree, uid, value)

                elif isinstance(value, (list, tuple)):
                    tree.insert(parent, tk.END, uid, text=GroupName)
                    result = { }
                    for x in value:
                        if isinstance(x, str): k, v = x.split('=')
                        else:
                            k = x.ID  # Key Property
                            v = x.Name  # Value Property

                        result[k] = v

                    self._json_tree(tree, uid, result)

                else:
                    if value is None: value = 'None'
                    tree.insert(parent, tk.END, uid, text=value)  # text=key, value=value)
        elif isinstance(d, (list, tuple)):
            for item in d:
                if isinstance(item, str):
                    try:
                        GroupName, children = item.split(':')
                    except (AttributeError, ValueError) as e:
                        raise DelimiterError('GroupName must be delimited by a :') from e

                    tree.insert(parent, tk.END, GroupName, text=GroupName)
                    result = { }
                    try:
                        for x in children.split(','):
                            try:
                                k, v = x.split('=')
                                result[k] = v
                            except (AttributeError, ValueError) as e:
                                raise DelimiterError('Key Value Pair must be delimited by a =') from e
                    except (AttributeError, ValueError) as e:
                        raise DelimiterError('Key Value Pairs must be delimited by a ,') from e

                    self._json_tree(tree, GroupName, result)

                else: self._json_tree(tree, parent, item)





    def OnSelectRow(self, event: tkEvent):
        if not isinstance(event, TkinterEvent): event = TkinterEvent(event)

        _iid = self.identify_row(event.y)

        if _iid != self.last_focus:
            if self.last_focus:
                self.item(self.last_focus, tags=[])
            self.item(_iid, tags=self.focus_tags)
            self.last_focus = _iid
            print(event, _iid)

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)


class TreeViewHolderThemed(Frame):
    """Construct a Ttk Treeview with master scale.

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
    Also creates ttk.scrollbar and the _root_frame that conatins
    both ThemedTreeView and ScrollBar objects
    """
    TreeView: TreeViewThemed
    vsb: ScrollbarThemed
    def __init__(self, master, backgroundColor: str, **kwargs):
        Frame.__init__(self, master=master, bg=backgroundColor, **kwargs)

        self.TreeView = TreeViewThemed(master=self, **kwargs)
        self.TreeView.pack(side='left', fill=tk.BOTH, expand=1)

        self.vsb = ScrollbarThemed(master=self, orient="vertical", command=self).Pack(side='right', fill=Fill.y)
        self.TreeView.configure(yscrollcommand=self.vsb.set)

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)



# noinspection DuplicatedCode
class ButtonThemed(ttk.Button, BaseTextTkinterWidget, ImageMixin, CommandMixin):
    """Construct a button _widget with the master MASTER.

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
    def __init__(self, master, text: str = '', Override_var: tk.StringVar = None, Color: dict = None, Command: callable = None, **kwargs):
        ttk.Button.__init__(self, master=master, **kwargs)
        cmd = kwargs.pop('command', None)
        if cmd: self.SetCommand(cmd)

        if Command: self.SetCommand(Command)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, text=text, Color=Color)

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)



# noinspection DuplicatedCode
class LabelThemed(ttk.Label, BaseTextTkinterWidget, ImageMixin):
    __doc__ = """Construct a label _widget with the master MASTER.

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
    def __init__(self, master, text: str = '', Override_var: tk.StringVar = None, Color: dict = None, **kwargs):
        ttk.Label.__init__(self, master=master, **kwargs)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, text=text, Color=Color)

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)



# noinspection DuplicatedCode
class EntryThemed(ttk.Entry, BaseTextTkinterWidget, CommandMixin):
    __doc__ = """Construct an entry _widget with the master MASTER.

    Valid resource names: background, bd, bg, borderwidth, cursor,
    exportselection, fg, font, foreground, highlightbackground,
    highlightcolor, highlightthickness, insertbackground,
    insertborderwidth, insertofftime, insertontime, insertwidth,
    invalidcommand, invcmd, justify, relief, selectbackground,
    selectborderwidth, selectforeground, show, state, takefocus,
    textvariable, validate, validatecommand, vcmd, width,
    xscrollcommand.
    """
    def __init__(self, master, text: str = '', Override_var: tk.StringVar = None, Color: dict = None, **kwargs):
        ttk.Entry.__init__(self, master=master, **kwargs)
        BaseTextTkinterWidget.__init__(self, Override_var=Override_var, text=text, Color=Color)


    def Clear(self): self.delete(0, Tags.End.value)

    def _setCommand(self):
        self.bind(Bindings.ButtonPress.value, self._cmd)
        return self

    @property
    def txt(self) -> str: return self.get()
    @txt.setter
    def txt(self, value: str):
        self.Clear()
        self.insert(Tags.End.value, value)

    def Append(self, value: str):
        self.insert(Tags.End.value, value)

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)



class NotebookThemed(BaseTextTkinterWidget, ttk.Notebook):
    def __init__(self, master, Color: dict = None, **kwargs):
        ttk.Notebook.__init__(self, master=master, **kwargs)
        BaseTkinterWidget.__init__(self, Color=Color)

    def _options(self, cnf, kwargs=None) -> dict:
        kw = { }
        if isinstance(kwargs, dict):
            for k, v in kwargs.items():
                if isinstance(v, Enum): v = v.value
                kw[k] = v

        return super()._options(cnf, kw)

    def Add(self, w: BaseTkinterWidget, add: dict = dict(padding=2), *, title: str, **kwargs) -> int:
        """Adds a new tab to the notebook.

        If window is currently managed by the notebook but hidden, it is restored to its previous position."""
        index = self.add(w, **add)
        self.tab(index, text=title, **kwargs)
        return index
    def add(self, child: BaseTkinterWidget, **kw) -> int:
        """Adds a new tab to the notebook.

        If window is currently managed by the notebook but hidden, it is restored to its previous position.

        Returns the index of the child. """
        ttk.Notebook.add(self, child, **kw)
        return self.index_of(child)

    def hide_tab(self, tab_id: Union[int, str]):
        """Hides the tab specified by tab_id.

        The tab will not be displayed, but the associated window remains managed by the notebook and its configuration remembered.
        Hidden tabs may be restored with the add command."""
        return ttk.Notebook.hide(self, tab_id)
    def forget(self, tab_id: Union[int, str]):
        """Removes the tab specified by tab_id, unmaps and unmanages the associated window."""
        return ttk.Notebook.forget(self, tab_id)
    def identify(self, x: int, y: int) -> Union[int, str]:
        """Returns the name of the tab element at position x, y, or the empty string if none."""
        return ttk.Notebook.identify(self, x, y)

    def index_of(self, widget: Union[BaseTkinterWidget, str]) -> int:
        if not isinstance(widget, str): _w = str(widget)
        else: _w = widget

        for i, w in enumerate(self.tabs()):
            if w == _w: return i

        raise ValueError(f'widget {widget} is not found in the tabs.')
    def index(self, tab_id: Union[int, str]):
        """Returns the numeric index of the tab specified by tab_id, or the total number of tabs if tab_id is the string "end"."""
        return ttk.Notebook.index(self, tab_id)

    def insert(self, pos: int, child: BaseTkinterWidget, **kw):
        """Inserts a pane at the specified position.

        pos is either the string end, an integer index, or the name of a managed child.
        If child is already managed by the notebook, moves it to the specified position."""
        return ttk.Notebook.insert(self, pos, child, **kw)

    def select(self, tab_id: Union[int, str] = None) -> Union[int, str]:
        """Selects the specified tab.

        The associated child window will be displayed, and the previously-selected window (if different) is unmapped.
        If tab_id is omitted, returns the widget name of the currently selected pane."""
        return ttk.Notebook.select(self, tab_id)

    def tab(self, tab_id: Union[int, str], option: str = None, **kw) -> Union[dict, Union[int, str]]:
        """Query or modify the options of the specific tab_id.

        If kw is not given, returns a dict of the tab option values.

        If option is specified, returns the value of that option.

        Otherwise, sets the options to the corresponding values."""
        return ttk.Notebook.tab(self, tab_id, option, **kw)
    def tabs(self) -> List[BaseTkinterWidget]:
        """Returns a list of windows managed by the notebook."""
        return ttk.Notebook.tabs(self)

    def enable_traversal(self):
        """Enable keyboard traversal for a toplevel window containing this notebook.

        This will extend the bindings for the toplevel window containing this notebook as follows:

            Control-Tab: selects the tab following the currently selected one

            Shift-Control-Tab: selects the tab preceding the currently selected one

            Alt-K: where K is the mnemonic (underlined) character of any tab, will select that tab.


        Multiple notebooks in a single toplevel may be enabled for traversal, including nested notebooks.
        However, notebook traversal only works properly if all panes are direct children of the notebook.


        The only, and good, difference I see is about mnemonics, which works after calling this method.
        Control-Tab and Shift-Control-Tab always works (here at least).
        """
        return ttk.Notebook.enable_traversal(self)


    @property
    def ActiveTab(self) -> Union[int, str]: return self.select()
    @ActiveTab.setter
    def ActiveTab(self, tab_id: Union[int, str]): self.select(tab_id)


    @property
    def txt(self) -> str: return self.tab(self.ActiveTab, option='text')
    @txt.setter
    def txt(self, value: str): self.tab(self.ActiveTab, text=value)


    @property
    def wrap(self) -> int: return self.tab(self.ActiveTab, option='wraplength')
    @wrap.setter
    def wrap(self, value: int):
        assert (isinstance(value, int))
        self.tab(self.ActiveTab, wraplength=self._wrap)
