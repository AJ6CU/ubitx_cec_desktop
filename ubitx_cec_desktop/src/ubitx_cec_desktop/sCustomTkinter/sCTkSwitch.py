#!/usr/bin/python3
"""
sCTkSwitch

subclass of CTkSwitch

UI source file: sCTkSwitch.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkSwitchui as baseui
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#

class sCTkSwitch(baseui.sCTkSwitchUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "font": ("Arial", 15, "normal"),

            # 📐 Physical Geometry (Thin Pill Silhouette Alignment Metrics)
            "width": 60,
            "height": 24,
            "switch_width": 42,
            "switch_height": 14,
            "corner_radius": 100,

            # 🎨 Color Map (OFF / Resting State)
            # 🔄 FIX: Darkened the Light Mode track line to #94A3B8 so it pops cleanly against white cards!
            "fg_color": ("#94A3B8", "#4B5563"),
            "text_color": ("#374151", "#D1D5DB"),

            # 📈 Active Palette (ON / Checked State)
            "progress_color": ("#1A4375", "#2471A3"),
            "button_color": ("#2471A3", "#2471A3"),
            "button_hover_color": ("#112A4B", "#1F618D"),

            # ⛔ Muted Soft-Contrast Disabled Overlay
            "disabled_map": {
                "text_color": ("#94A3B8", "#64748B"),
                "fg_color": ("#CBD5E1", "#374151"),
                "progress_color": ("#CBD5E1", "#4B5563"),
                "button_color": ("#475569", "#94A3B8")
            }
        }

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array securely
        super().__init__(master, **self.final_kw)

    def state(self, mode: str):
        """Dedicated switch toggle state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            # Natively unlock mouse clicking toggle interaction engines safely
            self.configure(state="normal")

            # Dynamically pull the exact active colors without hardwired strings
            for key in ("text_color", "fg_color", "progress_color", "button_color"):
                active_val = self.final_kw.get(key, self._local_defaults.get(key))
                try:
                    self.configure(**{key: active_val})
                except Exception:
                    pass

            self._custom_current_state = "normal"

        elif mode == "disabled":
            # Natively lock toggle parameters down tightly to freeze state adjustments
            self.configure(state="disabled")

            # Pull your customized high-contrast muted configurations out of your map
            for key in ("text_color", "fg_color", "progress_color", "button_color"):
                if key in self._custom_disabled_map:
                    try:
                        self.configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")

    root = ctk.CTk()
    root.geometry("400x200")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkSwitch(base, text="Lock Transceiver Pre-Amp Link")
    widget.pack(expand=True, fill="none", padx=10, pady=10)

    # Force disabled check to immediately verify layout contrast bounds
    widget.state("disabled")
    print("state (Disabled Pass) =", widget.get_state())  # Output: disabled

    # 🔄 FIX: Added normal pass check to ensure fluid bi-directional transition flows
    widget.state("normal")
    print("state (Normal Pass)   =", widget.get_state())  # Output: normal

    root.mainloop()
