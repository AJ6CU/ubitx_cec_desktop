#!/usr/bin/python3
"""
sCTkEntrySecondary

Customized ctk Entry field. - Secondary version

UI source file: sCTkEntrySecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkEntrySecondaryui as baseui


#
# Manual user code
#

class sCTkEntrySecondary(baseui.sCTkEntrySecondaryUI):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "fg_color": "transparent",
            "text_color": ("#4B5563", "#D1D5DB"),
            "border_width": 1.5,  # Ensure border renders
            "border_color": ("#CBD5E1", "#4B5563"),
            "placeholder_text_color": ("#757575", "#757575")
        }
        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkEntrySecondary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
