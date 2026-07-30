#!/usr/bin/python3
"""
textBoxSecondary

Similer to ttk.labelframe built on ctkscrollableframe with scrollbars hidden. This textBox is typically used for user information or explanations as there is no border and the font is smaller.

UI source file: textBoxSecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import textBoxSecondaryui as baseui


#
# Manual user code
#

class textBoxSecondary(baseui.textBoxSecondaryUI):
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
    widget = textBoxSecondary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
