#!/usr/bin/python3
"""
sCTkEntrySecondary

subclass of CTkEntry (Secondary Form / Helper Input Field)
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkEntrySecondaryui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkEntrySecondary(baseui.sCTkEntrySecondaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "font": ("Arial", 13, "normal"),  # Scaled down context fields
            "border_width": 1,  # Thinner layout border tracking

            # 🎨 Active Look (Neutral borders / Shaded recessed entry track layer)
            "border_color": ("#9CA3AF", "#4B5563"),  # Neutral border frame profile
            "fg_color": ("#F3F4F6", "#1F2937"),  # Recessed background entry layer
            "text_color": ("#4B5563", "#D1D5DB"),  # Softer primary gray typography
            "corner_radius": 6,

            # ⛔ Muted Disabled Overlay
            "disabled_map": {
                "fg_color": ("#F3F4F6", "#0B0F19"),  # Further drops frame luminosity values
                "border_color": ("#CBD5E1", "#374151"),  # Finalized soft silver trace for Light Mode!
                "text_color": ("#94A3B8", "#64748B")  # Standardizes locking typography behavior
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
        """Dedicated secondary text input state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            # Directly unlock text inputs by executing native un-wrapped Tkinter calls
            try:
                tk.Entry.configure(self._entry, state="normal")
            except Exception:
                pass

            self.configure(state="normal")

            # Dynamically pull the exact active colors without hardwired strings
            for key in ("fg_color", "border_color", "text_color"):
                active_val = self.final_kw.get(key, self._local_defaults.get(key))
                try:
                    self.configure(**{key: active_val})
                except Exception:
                    pass

            self._custom_current_state = "normal"

        elif mode == "disabled":
            # Force deep component locking via native un-wrapped Tkinter calls
            try:
                tk.Entry.configure(self._entry, state="disabled")
            except Exception:
                pass

            self.configure(state="disabled")

            # Safely apply your custom muted gray palette strings
            for key in ("fg_color", "border_color", "text_color"):
                if key in self._custom_disabled_map:
                    try:
                        self.configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"


if __name__ == "__main__":
    # ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.geometry("400x200")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkEntrySecondary(base, placeholder_text="Enter configuration metadata...")
    widget.pack(expand=True, fill="x", padx=40, pady=10)

    frame_color = base.cget("fg_color")
    widget.configure(fg_color=frame_color)

    # Verify tracking loop sequence
    widget.state("disabled")
    print("state =", widget.get_state())  # Output: disabled

    # widget.state("normal")
    # print("state =", widget.get_state())  # Output: normal

    root.mainloop()
