
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
        self.home = HomeWindow(root=self).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.w1 = Window1(root=self).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.w2 = Window2(root=self).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.w3 = Window3(root=self).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

        self.w1.hide()
        self.w2.hide()
        self.w3.hide()
        print('Root.children', self.children)

class HomeWindow(TkinterFrame):
    def __init__(self, root):
        self.root = root
        super().__init__(root)
        self.button = TkinterButton(master=self, Text="widnow 1").SetCommand(self.win1).Place(relx=0.0, rely=0.0, relheight=0.33, relwidth=0.5)
        self.button = TkinterButton(master=self, Text="widnow 2").SetCommand(self.win2).Place(relx=0.0, rely=0.33, relheight=0.33, relwidth=0.5)
        self.button = TkinterButton(master=self, Text="widnow 3").SetCommand(self.win3).Place(relx=0.0, rely=0.66, relheight=0.33, relwidth=0.5)

    def win1(self):
        self.hide()
        self.root.w1.show()
    def win2(self):
        self.hide()
        self.root.w2.show()
    def win3(self):
        self.hide()
        self.root.w3.show()

class BaseWindow(TkinterFrame):
    button: TkinterButton
    CreateWidgets: callable
    def __init__(self, root):
        self.root = root
        super().__init__(root)
        self.CreateWidgets()

    def exit(self):
        self.hide()
        self.root.home.show()
class Window1(BaseWindow):
    def CreateWidgets(self):
        self.button = TkinterButton(master=self, Text="button").SetCommand(self.exit).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

class Window2(BaseWindow):
    def CreateWidgets(self):
        self.button = TkinterButton(master=self, Text="button").SetCommand(self.exit).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

class Window3(BaseWindow):
    def CreateWidgets(self):
        self.button = TkinterButton(master=self, Text="button").SetCommand(self.exit).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)


if __name__ == '__main__':
    root = Root()
    root.mainloop()
