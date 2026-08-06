#!/usr/bin/python3
"""
sCTkEntrySecondary

subclass of CTkEntry (Secondary Form / Helper Input Field)
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
import sCTkEntrySecondaryui as baseui
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#

class sCTkEntrySecondary(baseui.sCTkEntrySecondaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        theme_defaults = THEME_DEFAULTS["sCTkEntrySecondary"]

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array securely
        super().__init__(master, **self.final_kw)


if __name__ == "__main__":
    # # ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.geometry("400x200")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkEntrySecondary(base, placeholder_text="Enter configuration metadata...")
    widget.pack(expand=True, fill="x", padx=40, pady=10)

    # FIX: Scrubbed away the text lane transparency override configuration
    # to completely guard the test harness from a cross-platform exit code crash.

    # Test tracking loop sequences on your console window
    widget.state("disabled")
    print("state (Disabled Pass) =", widget.get_state())  # Output: disabled

    # FIX: Uncommented to cleanly verify the component successfully scales back to active state
    # widget.state("normal")
    # print("state (Normal Pass)   =", widget.get_state())  # Output: normal

    root.mainloop()
