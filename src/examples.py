
# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

from TkinterExtensions import *



class Root(tk.Tk):
    # sets up Tkinter and creates the other windows and places them accordingly.
    def __init__(self):
        super().__init__()
        self.geometry('800x480+100+100')
        self.home = HomeWindow(master=self).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.w1 = Window1(master=self).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.w2 = Window2(master=self).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.w3 = Window3(master=self).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.w4 = LabelWindow(master=self).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

        # DebugWidgetRecursively(self.home, Message='__init__')
        # DebugWidgetRecursively(self.w1, root=self, Message='__init__')
        # DebugWidgetRecursively(self.w2, root=self, Message='__init__')
        # DebugWidgetRecursively(self.w3, root=self, Message='__init__')
        self.w1.hide()
        self.w2.hide()
        self.w3.hide()
        self.w4.hide()



class HomeWindow(TkinterFrame):
    def __init__(self, master: Root):
        self.root = master
        super().__init__(master)
        self.b1 = TkinterButton(master=self, Text="widnow 1").SetCommand(self.win1).Place(relx=0.0, rely=0.0, relheight=0.25, relwidth=0.5)
        self.b2 = TkinterButton(master=self, Text="widnow 2").SetCommand(self.win2).Place(relx=0.0, rely=0.25, relheight=0.25, relwidth=0.5)
        self.b3 = TkinterButton(master=self, Text="widnow 3").SetCommand(self.win3).Place(relx=0.0, rely=0.50, relheight=0.25, relwidth=0.5)
        self.b4 = TkinterButton(master=self, Text="widnow 4").SetCommand(self.win4).Place(relx=0.0, rely=0.75, relheight=0.25, relwidth=0.5)

    def win1(self): self.root.w1.show()
    def win2(self): self.root.w2.show()
    def win3(self): self.root.w3.show()
    def win4(self): self.root.w4.show()



class BaseWindow(TkinterFrame):
    button: TkinterButton
    CreateWidgets: callable
    def __init__(self, master: Root):
        self.master = master
        super().__init__(master)
        self.CreateWidgets()

    def exit(self):
        self.hide()
        self.master.home.show()


class Window1(BaseWindow):
    def CreateWidgets(self):
        self.button = TkinterButton(master=self, Text="button 1").SetCommand(self.exit).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)


class Window2(BaseWindow):
    def CreateWidgets(self):
        self.button = TkinterButton(master=self, Text="button 2").SetCommand(self.exit).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)


class Window3(BaseWindow):
    nested: Window2
    def CreateWidgets(self):
        self.button = TkinterButton(master=self, Text="button 3").SetCommand(self.exit).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=0.5)
        self.nested = LabelWindow(master=self).Place(relx=0.5, rely=0.0, relheight=1.0, relwidth=0.5)


class LabelWindow(TkinterLabelFrame):
    button: TkinterButton
    CreateWidgets: callable
    def __init__(self, master: Root or BaseWindow):
        self.master = master
        super().__init__(master, Text=self.__class__.__name__)
        self.button = TkinterButton(master=self, Text="button 4").SetCommand(self.exit).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=0.5)

    def exit(self):
        self.hide()
        self.master.home.show()



if __name__ == '__main__':
    root = Root()
    root.mainloop()
