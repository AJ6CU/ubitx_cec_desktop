#!/usr/bin/python3
"""
sCTkProgressBar.

derived from progressBar

UI source file: sCTkProgressBar.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import os
import sCTkProgressBarui as baseui


#
# Manual user code
#

class sCTkProgressBar(baseui.sCTkProgressBarUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

    def bind(self, sequence=None, command=None, add=None):
        if "PYGUBU_DESIGNER_RUNNING" in os.environ:
            # Avoid error, do nothing.
            pass
        else:
            # Send request to parent class
            return super().bind(sequence, command, add)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkProgressBar(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
