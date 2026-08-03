#!/usr/bin/python3
"""
sCTKSwitch

derived from ctk switch

UI source file: sCTkSwitch.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkSwitchui as baseui


#
# Manual user code
#

class sCTkSwitch(baseui.sCTkSwitchUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkSwitch(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
