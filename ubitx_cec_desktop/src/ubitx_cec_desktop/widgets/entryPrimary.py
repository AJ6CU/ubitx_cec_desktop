#!/usr/bin/python3
"""
entryPrimary

Customized ctk Entry field. - Primary version

UI source file: entryPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import entryPrimaryui as baseui


#
# Manual user code
#

class entryPrimary(baseui.entryPrimaryUI):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "fg_color": ("#FFFFFF", "#111827"),
            "text_color": ("#1F2937", "#F9FAFB"),
            "border_width": 1.5,
            "border_color": ("#64748B", "#64748B"),
            "placeholder_text_color": ("#757575", "#757575")
        }
        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = entryPrimary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
