#!/usr/bin/python3
"""
labelSecondary

The secondary label used for general use.

UI source file: labelSecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import labelSecondaryui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class labelSecondary(baseui.labelSecondaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            # 🔤 Uniform size 15 font matching checkboxes and option menu baselines
            "font": ("Arial", 15, "normal"),
            "fg_color": "transparent",
            "text_color": ("#374151", "#D1D5DB"),

            "disabled_map": {
                "text_color": ("#94A3B8", "#64748B")  # Soft slate tone across both modes uniformly
            }
        }

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries safely
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

    widget = labelSecondary(base, text="Receiver Audio Volume level:")
    widget.pack(expand=True, fill="none", padx=10, pady=10)

    # Test tracking loop sequences on your console window
    widget.state("disabled")
    print("state =", widget.get_state())  # Output: disabled

    # widget.state("normal")
    # print("state =", widget.get_state())  # Output: normal

    root.mainloop()
