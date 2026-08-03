#!/usr/bin/python3
"""
sCTkTabview

Built on top of CTkTabview.

UI source file: sCTkTabview.ui
"""
import os
import tkinter as tk
import tkinter.ttk as ttk
import sCTkTabviewui as baseui


#
# Manual user code
#

class sCTkTabview(baseui.sCTkTabviewUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

    def bind(self, sequence=None, command=None, add=None):
        if "PYGUBU_DESIGNER_RUNNING" in os.environ:
            # Avoid error, do nothing.
            pass
        else:
            # Send reques to parent class
            return super().bind(sequence, command, add)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkTabview(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
