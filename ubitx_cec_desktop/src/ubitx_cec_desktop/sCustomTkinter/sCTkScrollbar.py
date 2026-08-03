#!/usr/bin/python3
"""
sCTkScrollbar

scrollbar

UI source file: sCTkScrollbar.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkScrollbarui as baseui


#
# Manual user code
#

class sCTkScrollbar(baseui.sCTkScrollbarUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkScrollbar(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
