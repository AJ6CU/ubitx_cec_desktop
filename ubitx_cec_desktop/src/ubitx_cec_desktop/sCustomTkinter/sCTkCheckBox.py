#!/usr/bin/python3
"""
sCTkCheckBox

derived from CTkCheckBox

UI source file: sCTkCheckBox.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkCheckBoxui as baseui


#
# Manual user code
#

class sCTkCheckBox(baseui.sCTkCheckBoxUI):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "font": ("Arial", 15, "normal"),

            # 📝 Text matching your standard labels
            "text_color": ("#374151", "#D1D5DB"),
            "text_color_disabled": ("#94A3B8", "#64748B"),

            # 🔲 Outer box borders
            "border_width": 2,
            "border_color": ("#64748B", "#64748B"),

            # 🎨 Checked state: Fills with the OptionMenu/ComboBox main brand blues
            "fg_color": ("#1A4375", "#2471A3"),

            # 🖱️ Hover state: Perfectly matches your ComboBox button colors
            "hover_color": ("#2471A3", "#1F618D"),

            # 🏹 Checkmark check icon color
            "checkmark_color": ("#FFFFFF", "#FFFFFF")
        }
        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkCheckBox(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
