#!/usr/bin/python3
"""
checkBox

derived from CTkCheckBox

UI source file: checkBox.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import checkBoxui as baseui


#
# Manual user code
#

class checkBox(baseui.checkBoxUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = checkBox(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
