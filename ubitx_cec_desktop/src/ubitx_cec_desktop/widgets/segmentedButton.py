#!/usr/bin/python3
"""
segmentedButton

segmentedButton

UI source file: segmentedButton.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import segmentedButtonui as baseui


#
# Manual user code
#

class segmentedButton(baseui.segmentedButtonUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = segmentedButton(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
