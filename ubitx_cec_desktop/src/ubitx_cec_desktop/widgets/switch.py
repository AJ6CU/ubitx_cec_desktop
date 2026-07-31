#!/usr/bin/python3
"""
switchPrimary

derived from ctk switch

UI source file: switch.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import switchui as baseui


#
# Manual user code
#

class switch(baseui.switchUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = switch(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
