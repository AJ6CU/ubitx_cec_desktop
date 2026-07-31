#!/usr/bin/python3
"""
canvas

canvas

UI source file: tabview.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import tabviewui as baseui


#
# Manual user code
#

class tabview(baseui.tabviewUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = tabview(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
