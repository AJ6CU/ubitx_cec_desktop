#!/usr/bin/python3
"""
sCTkDialog

a special widget deciated to making popup dialogs consistent

UI source file: dialogBase.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import dialogBaseui as baseui


#
# Manual user code
#

class dialogBase(baseui.dialogBaseUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.pack(expand=True, fill="both")


if __name__ == "__main__":
    root = tk.Tk()
    widget = dialogBase(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
