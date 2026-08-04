#!/usr/bin/python3
"""
sCTKSwitch

derived from ctk switch

UI source file: sCTkSwitch.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkSwitchui as baseui


#
# Manual user code
#

class sCTkSwitch(baseui.sCTkSwitchUI):
    def init__(self, master=None, **kw):
        theme_defaults = {
            # 📐 Physical Geometry (Passed via **kwargs)
            "width": 60,  # Total width of the switch box
            "height": 24,  # Height matching your slider layout
            "switch_width": 42,  # Horizontal length of the internal toggle track [1]
            "switch_height": 14,  # FIX: Thins the track down for a modern, sleek look [1]
            "corner_radius": 100,  # Fully rounds out the capsule pill track edges [1]

            # 📝 Text layout matching your regular labels and checkboxes
            "font": ("Arial", 15, "normal"),
            "text_color": ("#374151", "#D1D5DB"),
            "text_color_disabled": ("#94A3B8", "#64748B"),

            # 🎨 Color Map (OFF State)
            # Track background matches your high-contrast slider resting rail gray
            "fg_color": ("#E5E7EB", "#4B5563"),

            # 📈 Color Map (ON State)
            # Track turns into your primary brand blue when flipped on
            "progress_color": ("#1A4375", "#2471A3"),

            # 🎛️ The round interactive moving knob
            # Base color uses your brighter blue; hovers with your darkest navy/rich blue tones
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
    widget = sCTkSwitch(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
