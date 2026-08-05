#!/usr/bin/python3
"""
sCTkOptionMenuPrimary

subclass of CTkOptionMenu (Primary Selection Controller)

UI source file: sCTkOptionMenuPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
import sCTkOptionMenuPrimaryui as baseui
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#

class sCTkOptionMenuPrimary(baseui.sCTkOptionMenuPrimaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        theme_defaults = THEME_DEFAULTS["sCTkOptionMenuPrimary"]

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array securely
        super().__init__(master, **self.final_kw)

    def state(self, mode: str):
        """Dedicated option menu state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            # Natively unlock mouse clicking expansion events safely
            self.configure(state="normal")

            # Dynamically pull the exact active colors without hardwired strings
            for key in ("fg_color", "button_color", "text_color"):
                active_val = self.final_kw.get(key, self._local_defaults.get(key))
                try:
                    self.configure(**{key: active_val})
                except Exception:
                    pass

            self._custom_current_state = "normal"

        elif mode == "disabled":
            # Natively freeze popups and lock out user interaction parameters
            self.configure(state="disabled")

            # Pull your customized high-contrast muted configurations out of your map
            for key in ("fg_color", "button_color", "text_color"):
                if key in self._custom_disabled_map:
                    try:
                        self.configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"

    def update_list(self, new_values: list, default_index: int = 0):
        """Safely updates the items list and resets the visible value."""
        if not new_values:
            self.configure(values=[""])
            self.set("")
            return

        self.configure(values=new_values)

        # Guard against index out of bounds errors
        if default_index < len(new_values):
            self.set(new_values[default_index])
        else:
            self.set(new_values[0])


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x200")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkOptionMenuPrimary(base, values=["Initial Mode A", "Initial Mode B"])
    widget.pack(expand=True, fill="x", padx=40, pady=10)

    # Verify that your dynamic updating pipeline operates smoothly
    print("Populating updated parameters track values list...")
    widget.update_list(["Mode: USB", "Mode: LSB", "Mode: AM", "Mode: CW"], default_index=1)

    # Verify our custom cascading state system locks down the option menu instantly!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("state =", widget.get_state())  # Output: disabled

    # Verify the cascade pipeline unlocks everything smoothly right back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("state =", widget.get_state())  # Output: normal

    root.mainloop()