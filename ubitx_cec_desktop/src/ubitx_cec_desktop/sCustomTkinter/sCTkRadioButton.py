#!/usr/bin/python3
"""
sCTkRadioButton

derived from radioButton

UI source file: sCTkRadioButton.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkRadioButtonui as baseui


#
# Manual user code
#

class sCTkRadioButton(baseui.sCTkRadioButtonUI):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "font": ("Arial", 15, "normal"),

            # 📝 Text matching your standard labels and checkboxes
            "text_color": ("#374151", "#D1D5DB"),
            "text_color_disabled": ("#94A3B8", "#64748B"),

            # 🔲 FIX: Increased unchecked border width from 2 to 4.
            # This gives the hover color a thicker surface area so it finally pops in light mode.
            "border_width_unchecked": 4,
            "border_width_checked": 6,
            "border_color": ("#64748B", "#64748B"),

            # 🎨 Active selection dot (matches OptionMenu/ComboBox base blue)
            "fg_color": ("#1A4375", "#2471A3"),

            # 🖱️ Uses your high-contrast navy/blue tones
            "hover_color": ("#112A4B", "#1F618D")
        }

        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkRadioButton(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
