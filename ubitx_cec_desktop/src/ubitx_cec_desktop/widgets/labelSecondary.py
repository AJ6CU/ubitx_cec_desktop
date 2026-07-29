#!/usr/bin/python3
"""
labelSecondary

The secondary label used for general use.

UI source file: labelSecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import labelSecondaryui as baseui


#
# Manual user code
#

class labelSecondary(baseui.labelSecondaryUI):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "font": ("Arial", 15, "normal"),
            "fg_color": "transparent",
            "text_color": ("#374151", "#D1D5DB"),
            "text_color_disabled": ("#94A3B8", "#64748B")
        }
        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = labelSecondary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
