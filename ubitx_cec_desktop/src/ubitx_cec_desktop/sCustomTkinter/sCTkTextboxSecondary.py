#!/usr/bin/python3
"""
sCTkTextboxSecondary

based on ctktextbox

UI source file: sCTkTextboxSecondary.ui
"""
import tkinter as tk

import tkinter.ttk as ttk

import sCTkTextboxSecondaryui as baseui


#
# Manual user code
#

class sCTkTextboxSecondary(baseui.sCTkTextboxSecondaryUI):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "border_width": 0,
            "border_color": ("#b5beb6", "#3d5242"),  # Matches frame outlines
            "fg_color": ("#cbcfcb", "#1a1a1a"),  # Recessed input surface
            "text_color": ("#1c1d1c", "#e3ece4"),  # High legibility text pairing
            "scrollbar_button_color": ("#2ed158", "#11802b"),  # Brand green handles
            "scrollbar_button_hover_color": ("#1f9c40", "#0b541c"),  # Interactive hover green
            "font": ("Arial", 11, "normal"),
            "wrap": "word"
        }
        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)



if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkTextboxSecondary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
