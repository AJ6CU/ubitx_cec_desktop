#!/usr/bin/python3
"""
sCTkCheckBox

subclass of CTkCheckBox

UI source file: sCTkCheckBox.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkCheckBoxui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkCheckBox(baseui.sCTkCheckBoxUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "font": ("Arial", 15, "normal"),
            "border_width": 3,

            # 🎨 Active Palette (Primary Brand Blue Accents)
            "border_color": ("#64748B", "#94A3B8"),  # High-visibility structural rims
            "fg_color": ("#1A4375", "#2471A3"),  # Inner fill color when checked
            "hover_color": ("#112A4B", "#1F618D"),  # Smooth feedback glow on cursor over
            "text_color": ("#374151", "#D1D5DB"),  # Crisp standard body typography

            # ⛔ Muted Disabled Overlay
            "disabled_map": {
                "text_color": ("#94A3B8", "#64748B"),  # Fades label text out of active focus
                "fg_color": ("#E5E7EB", "#374151"),  # Dulls the core inner box fill
                "border_color": ("#CBD5E1", "#475569")  # Softens the outer ring track line
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
        """Dedicated checkbox state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            # Natively unlock mouse clicking interactions
            self.configure(state="normal")

            # Dynamically pull the exact active colors without hardwired strings
            for key in ("text_color", "fg_color", "border_color", "hover_color"):
                active_val = self.final_kw.get(key, self._local_defaults.get(key))
                try:
                    self.configure(**{key: active_val})
                except Exception:
                    pass

            self._custom_current_state = "normal"

        elif mode == "disabled":
            # Natively lock out mouse interaction events safely
            self.configure(state="disabled")

            # Pull your customized high-contrast muted configurations out of your map
            for key in ("text_color", "fg_color", "border_color"):
                if key in self._custom_disabled_map:
                    try:
                        self.configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x200")

    # Simple container frame wrapper to simulate app placement environment
    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkCheckBox(base, text="Enable Logging Framework")
    widget.pack(expand=True, fill="none", padx=10, pady=10)

    # Sync backgrounds dynamically
    frame_color = base.cget("fg_color")
    widget.configure(fg_color=frame_color)

    # Test tracking loop sequences on your console window
    widget.state("disabled")
    print("state =", widget.get_state())  # Output: disabled

    # widget.state("normal")
    # print("state =", widget.get_state())  # Output: normal

    root.mainloop()
