#!/usr/bin/python3
"""
labelPrimary

The primary label used for headers etc.

UI source file: labelPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import labelPrimaryui as baseui


#
# Manual user code
#

class labelPrimary(baseui.labelPrimaryUI):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "font": ("Arial", 18, "bold"),
            "fg_color": "transparent",
            "text_color": ("#111827", "#F9FAFB"),
            "text_color_disabled": ("#94A3B8", "#64748B")
        }
        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = labelPrimary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
