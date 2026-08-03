#!/usr/bin/python3
"""
sCTkCheckBox

derived from CTkCheckBox

UI source file: sCTkCheckBox.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkCheckBoxui as baseui


#
# Manual user code
#

class sCTkCheckBox(baseui.sCTkCheckBoxUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkCheckBox(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
