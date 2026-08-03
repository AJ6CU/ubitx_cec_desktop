#!/usr/bin/python3
"""
sCTkLabelPrimary

The primary label used for headers etc.

UI source file: sCTkLabelPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkLabelPrimaryui as baseui


#
# Manual user code
#

class sCTkLabelPrimary(baseui.sCTkLabelPrimaryUI):
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
    widget = sCTkLabelPrimary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
