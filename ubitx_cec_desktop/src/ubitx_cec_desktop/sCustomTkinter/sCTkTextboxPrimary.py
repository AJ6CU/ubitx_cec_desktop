#!/usr/bin/python3
"""
sCTkTextboxPrimary

update to ctktextbox

UI source file: sCTkTextboxPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkTextboxPrimaryui as baseui


#
# Manual user code
#

class sCTkTextboxPrimary(baseui.sCTkTextboxPrimaryUI):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #

        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkTextboxPrimary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
