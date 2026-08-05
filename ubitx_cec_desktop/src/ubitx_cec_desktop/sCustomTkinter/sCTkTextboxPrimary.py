#!/usr/bin/python3
"""
sCTkTextboxPrimary

update to ctktextbox

UI source file: sCTkTextboxPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
import sCTkTextboxPrimaryui as baseui
from ThemeableWidget import ThemeableWidget
from sCTkFrame import sCTkFrame


class sCTkTextboxPrimary(baseui.sCTkTextboxPrimaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        theme_defaults = THEME_DEFAULTS["sCTkTextboxPrimary"]

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries safely
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array securely
        super().__init__(master, **self.final_kw)

        # FIX: Self-correcting transparency workaround!
        # If the text box lands on top of a transparent container panel, it dynamically
        # climbs up the layout tree to fetch the window's true underlying background colors,
        # perfectly matching your camouflage look without triggering a transparency error!
        try:
            current_fg = self.cget("fg_color")
            if current_fg == "transparent" or current_fg == "":
                # Fallback to the master's true background asset tuple
                parent_bg = self.master.cget("fg_color")
                if parent_bg != "transparent" and parent_bg != "":
                    self.configure(fg_color=parent_bg)
        except Exception:
            pass

    def state(self, mode: str):
        """Dedicated text field state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            self.configure(state="normal")

            # Dynamically restore all active properties out of final_kw
            for key in ("fg_color", "border_color", "text_color", "scrollbar_button_color",
                        "scrollbar_button_hover_color"):
                active_val = self.final_kw.get(key, self._local_defaults.get(key))
                try:
                    self.configure(**{key: active_val})
                except Exception:
                    pass

            self._custom_current_state = "normal"

        elif mode == "disabled":
            self.configure(state="disabled")

            # Dynamically apply your complete high-contrast disabled muted configurations out of your map!
            for key in ("fg_color", "border_color", "text_color", "scrollbar_button_color",
                        "scrollbar_button_hover_color"):
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

    widget = sCTkTextboxPrimary(base)
    widget.pack(expand=True, fill="both", padx=10, pady=10)

    # Pre-populate sample message streams to check text visibility metrics
    widget.insert("0.0", "System Telemetry Buffer Active...\nListening on COM-04 trace line...\n")

    # Verify our custom cascading state system locks down the text box workspace!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("state (Disabled Sequence) =", widget.get_state())  # Output: disabled

    # FIX: Re-activated to verify fluid return-to-normal configurations tracking flows flawlessly
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("state (Normal Sequence)   =", widget.get_state())  # Output: normal

    root.mainloop()
