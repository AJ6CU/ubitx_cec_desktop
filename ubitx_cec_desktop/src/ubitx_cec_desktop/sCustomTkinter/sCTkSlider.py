#!/usr/bin/python3
"""
sCTkSlider

derived from slider

UI source file: sCTkSlider.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkSliderui as baseui


#
# Manual user code
#

class sCTkSlider(baseui.sCTkSliderUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkSlider(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
