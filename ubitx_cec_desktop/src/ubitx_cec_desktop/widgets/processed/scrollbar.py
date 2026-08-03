#!/usr/bin/python3
"""
scrollbar

scrollbar

UI source file: scrollbar.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import scrollbarui as baseui


#
# Manual user code
#

class scrollbar(baseui.scrollbarUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = scrollbar(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
