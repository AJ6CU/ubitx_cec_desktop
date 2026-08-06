#!/usr/bin/python3
"""
sCTkLabelPrimary

The primary label used for headers etc.

UI source file: sCTkLabelPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
import sCTkLabelPrimaryui as baseui
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#

class sCTkLabelPrimary(baseui.sCTkLabelPrimaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        theme_defaults = THEME_DEFAULTS["sCTkLabelPrimary"]

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("500x400")

    # Explicitly import your container dependencies to prevent NameError loop crashes
    from sCTkFrameLabeledPrimary import sCTkFrameLabeledPrimary
    from sCTkLabelSecondary import sCTkLabelSecondary
    from sCTkButtonPrimary import sCTkButtonPrimary

    # 🔲 Create the main container panel card
    widget = sCTkFrameLabeledPrimary(root, label_text="System Transceiver Configuration Logs")
    widget.pack(expand=True, fill="both", padx=30, pady=30)

    # FIX: Safely route child widgets to the container's true inner packing layout content panel layer!
    target_container = getattr(widget, "w_child_container", widget)

    # Injects 20 secondary placeholder lines to test the component density constraints layout
    for row_index in range(1, 21):
        log_line = sCTkLabelSecondary(
            target_container,
            text=f"[{row_index:02d}] VFO A Tuning Sequence Status Code: 0x2A - Channel Active",
            anchor="w"
        )
        log_line.pack(fill="x", padx=15, pady=4)

    # Let's add a clear themeable interactive action node inside the container bottom region
    action_btn = sCTkButtonPrimary(target_container, text="Purge Session Buffer Logs")
    action_btn.pack(padx=20, pady=15)

    # Verify our custom cascading state system locks down all 20 lines instantly!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("Primary Container Frame state (Disabled Sequence) =", widget.get_state())
    print("Nested child log line state                       =", log_line.get_state())

    # Verify the cascade pipeline unlocks everything smoothly right back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("Primary Container Frame state (Normal Sequence)   =", widget.get_state())
    print("Nested child log line state                       =", log_line.get_state())

    root.mainloop()
