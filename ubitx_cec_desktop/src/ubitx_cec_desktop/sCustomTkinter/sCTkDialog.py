#!/usr/bin/python3
"""
sCTkDialog

a special widget deciated to making popup dialogs consistent

UI source file: sCTkDialog.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkDialogui as baseui


#
# Manual user code
#

class sCTkDialog(baseui.sCTkDialogUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkDialog(root)
    root.mainloop()
