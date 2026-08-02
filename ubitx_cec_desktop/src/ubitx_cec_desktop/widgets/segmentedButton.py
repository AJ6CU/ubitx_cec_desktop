#!/usr/bin/python3
"""
segmentedButton

segmentedButton

UI source file: segmentedButton.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import segmentedButtonui as baseui
import os


#
# Manual user code
#

class segmentedButton(baseui.segmentedButtonUI):
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
    widget = segmentedButton(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
