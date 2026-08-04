#!/usr/bin/python3
"""
sCTkSlider

derived from slider

UI source file: sCTkSlider.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkSliderui as baseui


#
# Manual user code
#

class sCTkSlider(baseui.sCTkSliderUI):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            # 📐 Physical Geometry (Passed via **kwargs)
            "width": 200,
            "height": 24,
            "button_length": 12,
            "border_width": 9,

            # 🎨 Color Map
            # FIX: Changed Dark Mode track color from #1F2937 to #4B5563 for sharp visibility
            "fg_color": ("#E5E7EB", "#4B5563"),

            "progress_color": ("#1A4375", "#2471A3"),
            "button_color": ("#2471A3", "#2471A3"),
            "button_hover_color": ("#112A4B", "#1F618D")
        }

        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkSlider(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
