#!/usr/bin/python3
"""
sCTkRadioButton

derived from radioButton

UI source file: sCTkRadioButton.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
import sCTkRadioButtonui as baseui
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#

class sCTkRadioButton(baseui.sCTkRadioButtonUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        theme_defaults = THEME_DEFAULTS["sCTkRadioButton"]

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries safely
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x150")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # Simple explicit string tracking variable to connect radio groups
    radio_var = tk.StringVar(value="VFO_A")

    widget = sCTkRadioButton(base, text="Primary VFO A Link Target", variable=radio_var, value="VFO_A")
    # Settled expand to False to lock geometry baseline metrics cleanly
    widget.pack(expand=False, fill="none", padx=10, pady=10)

    # Verify our custom cascading state system locks down the component!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("state =", widget.get_state())  # Output: disabled

    # Verify the cascade pipeline unlocks everything smoothly right back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("state =", widget.get_state())  # Output: normal

    root.mainloop()
