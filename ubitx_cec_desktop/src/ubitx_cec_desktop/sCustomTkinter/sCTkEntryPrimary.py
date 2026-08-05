#!/usr/bin/python3
"""
sCTkEntryPrimary

subclass of CTkEntry (Primary Form Input Field)
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkEntryPrimaryui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkEntryPrimary(baseui.sCTkEntryPrimaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "font": ("Arial", 15, "normal"),
            "border_width": 1.5,

            # 🎨 Active Look (Brand Blue Outline Rim / High Contrast Entry Layer)
            "border_color": ("#1A4375", "#64748B"),  # Brand blue / slate dark outline ring
            "fg_color": ("#FFFFFF", "#111827"),  # Clean entry input channel background canvas
            "text_color": ("#1F2937", "#F9FAFB"),  # High contrast text typography
            "corner_radius": 6,

            # ⛔ Muted Disabled Overlay
            "disabled_map": {
                "fg_color": ("#F3F4F6", "#1F2937"),  # Drops frame luminosity track down 1 step
                "border_color": ("#CBD5E1", "#475569"),  # Softens bounding outer container grid lines
                "text_color": ("#94A3B8", "#64748B")  # Fades typed alphanumeric strings
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
        """Dedicated text input state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            # 🔄 FIX: Directly unlock text inputs by executing native un-wrapped Tkinter calls
            try:
                tk.Entry.configure(self._entry, state="normal")
            except Exception:
                pass

            # Formally let CustomTkinter update its internal shell properties as well
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
            # 🔄 FIX: Force deep component locking via native un-wrapped Tkinter calls!
            # This completely freezes typing, echoes, and backspaces instantly at the C-level.
            try:
                tk.Entry.configure(self._entry, state="disabled")
            except Exception:
                pass

            # Formally freeze the CustomTkinter outer wrapper state
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
    # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x200")

    # Simple container frame wrapper to simulate app placement environment
    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkEntryPrimary(base, placeholder_text="Enter Transceiver Frequency...")
    widget.pack(expand=True, fill="x", padx=40, pady=10)


    # Sync backgrounds dynamically
    frame_color = base.cget("fg_color")
    widget.configure(fg_color=frame_color)

    # Test tracking loop sequences on your console window
    widget.state("disabled")
    print("state =", widget.get_state())  # Output: disabled

    # widget.state("normal")
    # print("state =", widget.get_state())  # Output: normal

    root.mainloop()
