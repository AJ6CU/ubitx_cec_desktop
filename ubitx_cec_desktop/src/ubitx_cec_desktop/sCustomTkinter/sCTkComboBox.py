#!/usr/bin/python3
"""
sCTkComboBox

derived from comboBox

UI source file: sCTkComboBox.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkComboBoxui as baseui


#
# Manual user code
#

class sCTkComboBox(baseui.sCTkComboBoxUI):
    def __init__(self, master=None, **kw):
        theme_defaults = {
             "font": ("Arial", 15, "normal"),
    "dropdown_font": ("Arial", 15, "normal"),
    "border_width": 1.5,

    # 🔲 Blue frame matches your OptionMenu background exactly
    "border_color": ("#1A4375", "#64748B"),

    # 🎨 The main text input area stays rich navy blue
    "fg_color": ("#1A4375", "#111827"),

    # 🏹 FIX: Button is a slightly brighter blue in light mode to break it apart from fg_color.
    # It is still dark enough to keep the arrow asset white and preserve the right border edge!
    "button_color": ("#2471A3", "#64748B"),

    # 🏹 Text & Arrow remain high-contrast white
    "text_color": ("#FFFFFF", "#FFFFFF"),

    # 🖱️ Hover state darkens the arrow button cleanly
    "button_hover_color": ("#112A4B", "#1F618D"),

    # 📋 Dropdown Lists
    "dropdown_fg_color": ("#FFFFFF", "#1F2937"),
    "dropdown_text_color": ("#1F2937", "#F9FAFB"),
    "dropdown_hover_color": ("#E5E7EB", "#374151")

        }
        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkComboBox(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
