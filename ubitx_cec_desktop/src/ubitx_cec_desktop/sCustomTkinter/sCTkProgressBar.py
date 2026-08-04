#!/usr/bin/python3
"""
sCTkProgressBar.

derived from progressBar

UI source file: sCTkProgressBar.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import os
import sCTkProgressBarui as baseui


#
# Manual user code
#

class sCTkProgressBar(baseui.sCTkProgressBarUI):
    def __init__(self, master=None, **kw):
        theme_defaults = {
            # 📐 Physical Geometry (Passed via **kwargs)
            "width": 200,  # Standard horizontal track length
            "height": 6,  # FIX: Natively sets a sleek, ultra-thin 6px track height

            # 🎨 Color Map
            # Matches your slider's high-contrast unselected gray tones
            "fg_color": ("#E5E7EB", "#4B5563"),

            # Matches your primary OptionMenu/ComboBox brand blue
            "progress_color": ("#1A4375", "#2471A3"),

            # 🔘 Smooth continuous edge styling
            "corner_radius": 100  # Fully rounds off the left and right ends of the track
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
    widget = sCTkProgressBar(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
