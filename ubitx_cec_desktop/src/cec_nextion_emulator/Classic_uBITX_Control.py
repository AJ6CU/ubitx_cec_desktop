#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
import Classic_uBITX_Controlui as baseui


#
# Manual user code
#

class Classic_uBITX_Control(baseui.Classic_uBITX_ControlUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = Classic_uBITX_Control(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
