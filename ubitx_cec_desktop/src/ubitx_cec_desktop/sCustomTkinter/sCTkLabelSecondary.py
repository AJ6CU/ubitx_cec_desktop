#!/usr/bin/python3
"""
sCTkLabelSecondary

The secondary label used for general use.

UI source file: sCTkLabelSecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
import sCTkLabelSecondaryui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkLabelSecondary(baseui.sCTkLabelSecondaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        theme_defaults = THEME_DEFAULTS["sCTkLabelSecondary"]
        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # FIX: Aligned parameters to pass exactly TWO dictionary objects up to the base theme class
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

    def state(self, mode: str):
        """Dedicated secondary label state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            # Restore your original high-contrast body text colors
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

    widget = sCTkLabelSecondary(base, text="Squelch Threshold Level:")
    widget.pack(expand=True, fill="none", padx=10, pady=10)

    # Verify our custom cascading state system locks down the body text instantly!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("state =", widget.get_state())  # Output: disabled

    # Verify the cascade pipeline unlocks everything smoothly right back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("state =", widget.get_state())  # Output: normal

    root.mainloop()
