#!/usr/bin/python3
"""
sCTkSegmentedButton

segmentedButton

UI source file: sCTkSegmentedButton.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import os
import sCTkSegmentedButtonui as baseui


#
# Manual user code
#

class sCTkSegmentedButton(baseui.sCTkSegmentedButtonUI):
    def __init__(self, master=None, **kw):
        theme_defaults = {
            # 🔤 Typography matching your core form controls
            "font": ("Arial", 15, "normal"),

            # 🎨 Base Track Background (Pure neutral medium gray / dark container)
            "fg_color": ("#9E9E9E", "#111827"),

            # 📝 Active selected text remains crisp white over the brand blue
            "text_color": ("#FFFFFF", "#FFFFFF"),

            # 📝 Unselected text color uses high-contrast charcoal for readability
            "text_color_disabled": ("#111827", "#F9FAFB"),

            # 📈 Selected / Active Segment (Your primary OptionMenu/ComboBox brand navy blues)
            "selected_color": ("#1A4375", "#2471A3"),
            "selected_hover_color": ("#112A4B", "#1F618D"),

            # 🖱️ FIX: The perfect mid-dark neutral gray tone
            "unselected_color": ("#9E9E9E", "#1F2937"),
            "unselected_hover_color": ("#7D7D7D", "#374151")  # Smoothly deepens on hover
        }

        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)

    def bind(self, sequence=None, command=None, add=None):
        if "PYGUBU_DESIGNER_RUNNING" in os.environ:
            # Avoid error, do nothing.
            pass
        else:
            # Send request to parent class
            return super().bind(sequence, command, add)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkSegmentedButton(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
