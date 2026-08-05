#!/usr/bin/python3
"""
sCTkLabelPrimary

The primary label used for headers etc.

UI source file: sCTkLabelPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkLabelPrimaryui as baseui
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#

class sCTkLabelPrimary(baseui.sCTkLabelPrimaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            # 📈 Bolds and scales up to 18px to stand out cleanly above form fields as a header title
            "font": ("Arial", 18, "bold"),
            "fg_color": "transparent",
            "text_color": ("#111827", "#F9FAFB"),  # Uses your maximum high-contrast text metrics

            "disabled_map": {
                "text_color": ("#94A3B8", "#64748B")  # Soft slate tone across both modes uniformly
            }
        }

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

    def state(self, mode: str):
        """Dedicated primary label state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            # Restore your original bold, high-contrast title look
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
    root.geometry("500x400")

    # 🔄 FIX: Explicitly import your container dependencies to prevent NameError loop crashes!
    from sCTkFrameLabeledPrimary import sCTkFrameLabeledPrimary
    from sCTkLabelSecondary import sCTkLabelSecondary
    from sCTkButtonPrimary import sCTkButtonPrimary

    # 🔲 Create the main container panel card
    widget = sCTkFrameLabeledPrimary(root, label_text="System Transceiver Configuration Logs")
    widget.pack(expand=True, fill="both", padx=30, pady=30)

    # Injects 20 secondary placeholder lines to test the component density constraints layout
    for row_index in range(1, 21):
        log_line = sCTkLabelSecondary(
            widget,
            text=f"[{row_index:02d}] VFO A Tuning Sequence Status Code: 0x2A - Channel Active",
            anchor="w"
        )
        log_line.pack(fill="x", padx=15, pady=4)

    # Let's add a clear themeable interactive action node at the very bottom
    action_btn = sCTkButtonPrimary(widget, text="Purge Session Buffer Logs")
    action_btn.pack(padx=20, pady=15)

    # 🔄 Verify our custom cascading state system locks down all 20 lines instantly!
    widget.state("disabled")
    print("Primary Container Frame state (Disabled Sequence) =", widget.get_state())

    # 🔄 Verify the cascade pipeline unlocks everything smoothly right back to normal
    widget.state("normal")
    print("Primary Container Frame state (Normal Sequence)   =", widget.get_state())

    root.mainloop()
