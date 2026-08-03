#!/usr/bin/python3
"""
sCTkFrameOutlined

Standard CTk form but with an outline border

UI source file: sCTkFrameOutlined.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkFrameOutlinedui as baseui


#
# Manual user code
#

class sCTkFrameOutlined(baseui.sCTkFrameOutlinedUI):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "border_color": ("#a1bfa7", "#3d5242"),
            "border_width": 2,
            "fg_color": ("#d6d6d6", "#212121"),
        }
        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkFrameOutlined(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
