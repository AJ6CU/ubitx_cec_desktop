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

    def configure(self, *args, **kwargs):
        """Processes Pygubu designer workspace queries and manages theme state updates cleanly."""
        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Feeds values to Pygubu Inspector)
        # -----------------------------------------------------------------
        if args and len(args) == 1:
            pname = args[0]
            if pname == "state":
                return ("state", "state", "state", "normal", str(super().cget("state")))

            if pname in ["fg_color", "button_color", "button_hover_color", "text_color"]:
                current_state = str(super().cget("state")).lower()
                if current_state == "disabled" and self._custom_disabled_map:
                    val = self._custom_disabled_map.get(pname)
                else:
                    val = self._local_defaults.get(pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            return super().configure(*args, **kwargs)

        # -----------------------------------------------------------------
        # ZONE C: STATE CONTROLLER (Swaps colors safely based on current mode)
        # -----------------------------------------------------------------
        if "state" in kwargs:
            target_state = str(kwargs["state"]).lower()

            if target_state == "disabled" and self._custom_disabled_map:
                # Apply explicit disabled map values from sCTkThemes
                kwargs["fg_color"] = self._custom_disabled_map.get("fg_color")
                kwargs["button_color"] = self._custom_disabled_map.get("button_color")
                kwargs["button_hover_color"] = self._custom_disabled_map.get("button_color")
                kwargs["text_color"] = self._custom_disabled_map.get("text_color")

            elif target_state in ["normal", "active"]:
                # Revert to normal active brand colors (No hardwired fallbacks!)
                # Strictly uses keys from your local defaults dictionary to enforce a hard stop if broken
                kwargs["fg_color"] = self._local_defaults["fg_color"]
                kwargs["button_color"] = self._local_defaults["button_color"]
                kwargs["button_hover_color"] = self._local_defaults["button_hover_color"]
                kwargs["text_color"] = self._local_defaults["text_color"]

        # ZONE D: EXECUTE BASE CLASS INITIALIZATION (Do not pop 'state' - native widget needs it)
        return super().configure(**kwargs)

    def state(self, state_string=None):
        """Standard Tkinter state management mapping helper."""
        if state_string is not None:
            self.configure(state=state_string)
        return str(super().cget("state")).lower()

    def get_state(self):
        """Explicit getter synchronized with your standalone test harness script assertions."""
        return self.state()

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