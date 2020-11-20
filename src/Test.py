
# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------
from TkinterExtensions.examples import *


def test():
    import tkinter as tk
    from tkinter import ttk
    from random import choice




    colors = ["red", "green", "black", "blue", "white", "yellow", "orange", "pink", "grey", "purple", "brown"]
    def recolor():
        for child in tree.get_children():
            picked = choice(colors)
            tree.item(child, tags=(picked,), values=(picked,))
        for color in colors:
            tree.tag_configure(color, background=color)
        tree.tag_configure("red", background="red")


    root = tk.Tk()

    tree = ttk.Treeview(root)

    tree["columns"] = ("one", "two", "three")
    tree.column("#0", width=60, minwidth=30, stretch=tk.NO)
    tree.column("one", width=120, minwidth=30, stretch=tk.NO)

    tree.heading("#0", text="0", anchor=tk.W)
    tree.heading("one", text="1", anchor=tk.W)

    for i in range(10):
        tree.insert("", i, text="Elem" + str(i), values=("none"))

    tree.pack(side=tk.TOP, fill=tk.X)

    b = tk.Button(root, text="Change", command=recolor)
    b.pack()

    root.mainloop()

if __name__ == '__main__':
    Root().Run()
    test()
