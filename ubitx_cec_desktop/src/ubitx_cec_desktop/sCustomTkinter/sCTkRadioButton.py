#!/usr/bin/python3
"""
sCTkRadioButton

derived from radioButton

UI source file: sCTkRadioButton.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkRadioButtonui as baseui


#
# Manual user code
#

class sCTkRadioButton(baseui.sCTkRadioButtonUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkRadioButton(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
