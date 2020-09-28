# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

from .Widgets import _BaseTkinterWidget_, tk




__all__ = ['Print']

def Print(w: _BaseTkinterWidget_, root: tk.Tk or tk.Toplevel, Message: str = 'BEFORE'):
    from pprint import PrettyPrinter
    pp = PrettyPrinter(indent=4)
    print(f'---------------- {Message} {w.__class__.__name__} ----------------')
    pp.pprint({ 'MODE': w, 'PI': w.pi, 'w.children': w.children, 'root.children': root.children })
