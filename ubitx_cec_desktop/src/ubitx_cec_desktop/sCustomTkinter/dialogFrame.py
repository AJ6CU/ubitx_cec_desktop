#!/usr/bin/python3
"""
dialogCommand

test

UI source file: dialogCommand.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import dialogFrameui as baseui


#
# Manual user code
#

class dialogFrame(baseui.dialogFrameUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.pack(expand=True, fill="both")


if __name__ == "__main__":
    root = tk.Tk()
    widget = dialogFrame(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
