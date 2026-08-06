#!/usr/bin/python3
"""
newdeleteme

newdeleteme

UI source file: newdeleteme.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import newdeletemeui as baseui
import customtkinter as ctk


#
# Manual user code
#

class newdeleteme(baseui.newdeletemeUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = ctk.CTk()
    widget = newdeleteme(root)
    root.mainloop()
