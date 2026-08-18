#!/usr/bin/python3
"""
sCTkSlider

derived from slider

UI source file: sCTkSlider.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
import sCTkSliderui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkSlider(baseui.sCTkSliderUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        theme_defaults = THEME_DEFAULTS["sCTkSlider"]

        # # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # FIX: Pass exactly TWO dictionary arguments to stay synchronized with your master engine class
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

    def configure(self, *args, **kwargs):
        """Handles both standard keyword configurations and Pygubu inspector queries."""
        # 1. POSITION INTERCEPT LOOP: Synchronizes the live Pygubu workspace preview
        if args and len(args) == 1:
            pname = args[0]

            # If Pygubu is inspecting the state, dynamically return colors based on that state
            if pname == "state":
                return ("state", "state", "state", "normal", super().cget("state"))

            if pname in ["fg_color", "progress_color", "button_color", "button_hover_color"]:
                current_state = str(super().cget("state")).lower()
                if current_state == "disabled" and self._custom_disabled_map:
                    # Feed the disabled theme metrics straight back into Pygubu's live canvas drawer
                    val = self._custom_disabled_map.get(pname)
                else:
                    val = self._local_defaults.get(pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            return super().configure(*args, **kwargs)

        # 2. KEYWORD SANITIZATION: Handles runtime code-driven transitions
        if "state" in kwargs:
            target_state = str(kwargs["state"]).lower()

            if target_state == "disabled" and self._custom_disabled_map:
                kwargs["fg_color"] = self._custom_disabled_map.get("fg_color")
                kwargs["progress_color"] = self._custom_disabled_map.get("progress_color")
                kwargs["button_color"] = self._custom_disabled_map.get("button_color")
                kwargs["button_hover_color"] = kwargs["button_color"]

            elif target_state in ["normal", "active"]:
                kwargs["fg_color"] = self._local_defaults.get("fg_color")
                kwargs["progress_color"] = self._local_defaults.get("progress_color")
                kwargs["button_color"] = self._local_defaults.get("button_color")
                kwargs["button_hover_color"] = self._local_defaults.get("button_hover_color")

        return super().configure(*args, **kwargs)

    def state(self, state_string=None):
        """Standard Tkinter state management mapping."""
        if state_string is not None:
            self.configure(state=state_string)
        return super().cget("state")

if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x150")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkSlider(base)
    # Settled expand to False to lock geometry baseline metrics cleanly
    widget.pack(expand=False, fill="x", padx=40, pady=10)
    widget.set(0.45)

    # Verify our custom state loop handles double-pass transitions flawlessly on the console
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("state (Disabled Pass) =", widget.get_state())  # Output: disabled

    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("state (Normal Pass)   =", widget.get_state())  # Output: normal

    root.mainloop()
