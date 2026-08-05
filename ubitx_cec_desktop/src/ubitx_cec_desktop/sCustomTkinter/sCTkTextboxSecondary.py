#!/usr/bin/python3
"""
sCTkTextboxSecondary

based on ctktextbox

UI source file: sCTkTextboxSecondary.ui
"""
import tkinter as tk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
import tkinter.ttk as ttk
import sCTkTextboxSecondaryui as baseui
from ThemeableWidget import ThemeableWidget
from sCTkFrame import sCTkFrame


#
# Manual user code
#

class sCTkTextboxSecondary(baseui.sCTkTextboxSecondaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        theme_defaults = THEME_DEFAULTS["sCTkTextboxSecondary"]

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries safely
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array securely
        super().__init__(master, **self.final_kw)

        # Apply your custom internal text padding override safely
        if hasattr(self, "_text_widget") and self._text_widget is not None:
            self._text_widget.configure(padx=5, pady=5)

        # FIX: Self-correcting transparency workaround!
        # Climbs the parent frame hierarchy automatically to pull and match solid colors
        # if placed on top of your completely see-through structural spacer frames.
        try:
            current_fg = self.cget("fg_color")
            if current_fg == "transparent" or current_fg == "":
                parent_bg = self.master.cget("fg_color")
                if parent_bg != "transparent" and parent_bg != "":
                    self.configure(fg_color=parent_bg)
        except Exception:
            pass

    def state(self, mode: str):
        """Dedicated text state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            self.configure(state="normal")

            # FIX: Dynamically restore all active properties out of final_kw
            for key in ("fg_color", "text_color", "scrollbar_button_color", "scrollbar_button_hover_color"):
                active_val = self.final_kw.get(key, self._local_defaults.get(key))
                try:
                    self.configure(**{key: active_val})
                except Exception:
                    pass

            self._custom_current_state = "normal"

        elif mode == "disabled":
            self.configure(state="disabled")

            # FIX: Dynamically apply your complete high-contrast disabled muted configurations out of your map!
            for key in ("fg_color", "text_color", "scrollbar_button_color", "scrollbar_button_hover_color"):
                if key in self._custom_disabled_map:
                    try:
                        self.configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("500x400")

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkTextboxSecondary(base)
    widget.pack(expand=True, fill="both", padx=10, pady=10)

    # Pre-populate sample session streams to verify text metrics
    widget.insert("0.0", "Secondary Metadata Stream Buffer Active...\nReading squelch tracking lines...\n")

    # Verify our custom cascading state system locks down the canvas and text elements instantly!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("state (Disabled Sequence) =", widget.get_state())  # Output: disabled

    # FIX: Verification hook successfully flushes properties back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("state (Normal Sequence)   =", widget.get_state())  # Output: normal

    root.mainloop()
