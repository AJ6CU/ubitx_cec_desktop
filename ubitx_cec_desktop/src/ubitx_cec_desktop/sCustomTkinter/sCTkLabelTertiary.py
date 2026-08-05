#!/usr/bin/python3
"""
sCTkLabelTertiary

3rd level Label used for notes

UI source file: sCTkLabelTertiary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkLabelTertiaryui as baseui
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#

class sCTkLabelTertiary(baseui.sCTkLabelTertiaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            # 📉 Scaled down to size 13 to serve as secondary context, captions, or helper hint messages
            "font": ("Arial", 13, "normal"),
            "fg_color": "transparent",
            "text_color": ("#4B5563", "#9CA3AF"),  # Slightly softer text colors so it is less loud on layout

            "disabled_map": {
                "text_color": ("#94A3B8", "#64748B")  # Standardizes locking behavior across text weights
            }
        }

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Aligned parameters to pass exactly TWO dictionary objects up to the base theme class
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

    def state(self, mode: str):
        """Dedicated tertiary label state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            # Restore your original soft caption text colors
            active_fallback = self._local_defaults.get("text_color")
            self.configure(text_color=self.final_kw.get("text_color", active_fallback))
            self._custom_current_state = "normal"

        elif mode == "disabled":
            # Apply your custom muted slate gray strings from your dictionary map
            if "text_color" in self._custom_disabled_map:
                self.configure(text_color=self._custom_disabled_map["text_color"])
            self._custom_current_state = "disabled"


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x150")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkLabelTertiary(base, text="* Note: Tuning frequency locks automatically after 3 seconds.")
    widget.pack(expand=True, fill="none", padx=10, pady=10)

    # 🔄 Verify our custom cascading state system locks down the caption text instantly!
    widget.state("disabled")
    print("state (Disabled Sequence) =", widget.get_state())  # Output: disabled

    # 🔄 FIX: Uncommented to cleanly verify the component successfully scales back to normal
    widget.state("normal")
    print("state (Normal Sequence)   =", widget.get_state())  # Output: normal

    root.mainloop()
