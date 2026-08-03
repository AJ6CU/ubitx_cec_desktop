#!/usr/bin/python3
"""
sCTkLabelTertiary

3rd level Label used for notes

UI source file: sCTkLabelTertiary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkLabelTertiaryui as baseui


#
# Manual user code
#

class sCTkLabelTertiary(baseui.sCTkLabelTertiaryUI):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "font": ("Arial", 12, "normal"),
            "fg_color": "transparent",
            "text_color": ("#4B5563", "#9CA3AF"),
            "text_color_disabled": ("#94A3B8", "#64748B")
        }
        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkLabelTertiary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
