#!/usr/bin/python3
"""
sCTkProgressBar

derived from progressBar

UI source file: sCTkProgressBar.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import os
import sCTkProgressBarui as baseui
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#

class sCTkProgressBar(baseui.sCTkProgressBarUI, ThemeableWidget):
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
            "corner_radius": 100,  # Fully rounds off the left and right ends of the track

            # ⛔ Muted Disabled Overlay
            "disabled_map": {
                "fg_color": ("#CBD5E1", "#374151"),  # Dulls unselected track backing
                "progress_color": ("#94A3B8", "#4B5563")  # Mutes current metric level bar contrast
            }
        }

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array securely
        super().__init__(master, **self.final_kw)

    def state(self, mode: str):
        """Dedicated progress bar state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            # Restore your original vibrant branding progress color configurations
            for key in ("fg_color", "progress_color"):
                active_val = self.final_kw.get(key, self._local_defaults.get(key))
                try:
                    self.configure(**{key: active_val})
                except Exception:
                    pass
            self._custom_current_state = "normal"

        elif mode == "disabled":
            # Apply your custom muted slate/charcoal gray strings from your dictionary map
            for key in ("fg_color", "progress_color"):
                if key in self._custom_disabled_map:
                    try:
                        self.configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass
            self._custom_current_state = "disabled"

    def bind(self, sequence=None, command=None, add=None):
        if "PYGUBU_DESIGNER_RUNNING" in os.environ:
            # Avoid error, do nothing.
            pass
        else:
            # Send request to parent class
            return super().bind(sequence, command, add)


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x150")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkProgressBar(base)
    # 🔄 FIX: Changed expand to False to prevent the 6px track height from over-expanding vertically!
    widget.pack(expand=False, fill="x", padx=40, pady=10)

    # Simulate a partial tracking progress status value filling the bar
    widget.set(0.65)

    # Test tracking loop sequences on your console window
    widget.state("disabled")
    print("state =", widget.get_state())  # Output: disabled

    widget.state("normal")
    print("state =", widget.get_state())  # Output: normal

    root.mainloop()
