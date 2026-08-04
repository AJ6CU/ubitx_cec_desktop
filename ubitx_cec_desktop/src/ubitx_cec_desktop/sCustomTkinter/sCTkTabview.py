#!/usr/bin/python3
"""
sCTkTabview

Built on top of CTkTabview.

UI source file: sCTkTabview.ui
"""
import os
import tkinter as tk
import tkinter.ttk as ttk
import sCTkTabviewui as baseui


#
# Manual user code
#

class sCTkTabview(baseui.sCTkTabviewUI):
    def __init__(self, master=None, **kw):
        theme_defaults = {
            # 🎨 Base Tabview Body Frame (The canvas area beneath the tabs)
            "fg_color": ("#FFFFFF", "#111827"),

            # 📝 Active selected tab text color remains crisp white
            "text_color": ("#FFFFFF", "#FFFFFF"),

            # 📝 Unselected tab text color uses high-contrast charcoal for readability
            "text_color_disabled": ("#112A4B", "#F9FAFB"),

            # 🔤 FIX: Intercepts and assigns the correct typeface to the hidden inner button array
            "segmented_button_font": ("Arial", 15, "normal"),

            # 🎨 Base Tab Track Background (Your perfect mid-neutral gray)
            "segmented_button_fg_color": ("#9E9E9E", "#111827"),

            # 📈 Selected / Active Tab Segment (Your primary brand navy blues)
            "segmented_button_selected_color": ("#1A4375", "#2471A3"),
            "segmented_button_selected_hover_color": ("#112A4B", "#1F618D"),

            # 🖱️ Unselected Tab Segments (Pure neutral gray—no blue undertone)
            "segmented_button_unselected_color": ("#9E9E9E", "#1F2937"),
            "segmented_button_unselected_hover_color": ("#7D7D7D", "#374151")
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
            # Send reques to parent class
            return super().bind(sequence, command, add)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkTabview(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
