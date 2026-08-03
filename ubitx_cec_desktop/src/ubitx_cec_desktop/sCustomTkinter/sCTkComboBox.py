#!/usr/bin/python3
"""
sCTkComboBox

derived from comboBox

UI source file: sCTkComboBox.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkComboBoxui as baseui


#
# Manual user code
#

class sCTkComboBox(baseui.sCTkComboBoxUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkComboBox(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
