#!/usr/bin/python3
"""
comboBox

derived from comboBox

UI source file: comboBox.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import comboBoxui as baseui


#
# Manual user code
#

class comboBox(baseui.comboBoxUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = comboBox(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
