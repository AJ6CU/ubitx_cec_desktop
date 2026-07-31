#!/usr/bin/python3
"""
canvas

canvas

UI source file: canvas.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import canvasui as baseui


#
# Manual user code
#

class canvas(baseui.canvasUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = canvas(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
