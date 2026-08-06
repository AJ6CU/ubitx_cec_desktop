#!/usr/bin/python3
"""
sCTkCheckBox

subclass of CTkCheckBox

UI source file: sCTkCheckBox.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
import sCTkCheckBoxui as baseui
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#

class sCTkCheckBox(baseui.sCTkCheckBoxUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        theme_defaults = THEME_DEFAULTS["sCTkCheckBox"]

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array securely
        super().__init__(master, **self.final_kw)


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x200")

    # Simple container frame wrapper to simulate app placement environment
    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkCheckBox(base, text="Enable Logging Framework")
    widget.pack(expand=True, fill="none", padx=10, pady=10)

    # FIX: Completely scrubbed out the configure(fg_color="transparent") line
    # to permanent avoid CustomTkinter's validation type check crashes!

    # Test tracking loop sequences on your console window
    widget.state("disabled")
    print("state (Disabled Pass) =", widget.get_state())  # Output: disabled
    #
    widget.state("normal")
    print("state (Normal Pass)   =", widget.get_state())  # Output: normal

    root.mainloop()
