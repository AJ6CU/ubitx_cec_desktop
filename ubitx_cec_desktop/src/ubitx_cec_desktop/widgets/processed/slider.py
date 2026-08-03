#!/usr/bin/python3
"""
sliderPrimary

derived from slider

UI source file: slider.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sliderui as baseui


#
# Manual user code
#

class slider(baseui.sliderUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = slider(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
