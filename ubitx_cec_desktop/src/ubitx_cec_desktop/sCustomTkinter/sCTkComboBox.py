#!/usr/bin/python3
"""
sCTkComboBox

subclass of CTkComboBox

UI source file: sCTkComboBox.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkComboBoxui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkComboBox(baseui.sCTkComboBoxUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "font": ("Arial", 15, "normal"),
            "dropdown_font": ("Arial", 15, "normal"),
            "border_width": 1.5,

            # 🎨 Active Palette (Primary Brand Blue and High-Contrast Grays)
            "border_color": ("#1A4375", "#64748B"),  # Brand blue line / slate dark line
            "fg_color": ("#FFFFFF", "#111827"),  # Text entry field background layer
            "text_color": ("#1F2937", "#FFFFFF"),  # Input text characters
            "button_color": ("#2471A3", "#64748B"),  # The arrow clickable dropdown button box
            "button_hover_color": ("#112A4B", "#1F618D"),  # Arrow box cursor feedback highlight

            # 📂 Floating Popup Dropdown Selection Card List View Menu Styling
            "dropdown_fg_color": ("#FFFFFF", "#1F2937"),
            "dropdown_text_color": ("#1F2937", "#F9FAFB"),
            "dropdown_hover_color": ("#E5E7EB", "#374151"),

            # ⛔ Muted Disabled Overlay
            "disabled_map": {
                "fg_color": ("#F3F4F6", "#1F2937"),  # Shades input container slightly
                "border_color": ("#E5E7EB", "#374151"),  # Softens bounding lines profile
                "text_color": ("#94A3B8", "#64748B"),  # Fades input text out of focus
                "button_color": ("#94A3B8", "#4B5563")  # Dulls arrow dropdown box container
            }
        }

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries via pipe operator
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array securely
        super().__init__(master, **self.final_kw)

    def state(self, mode: str):
        """Dedicated combo box state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            # 🔄 Natively unlock typing input and list selection capabilities safely
            self.configure(state="normal")

            # Dynamically pull the exact active colors without hardwired strings
            for key in ("fg_color", "border_color", "text_color", "button_color"):
                active_val = self.final_kw.get(key, self._local_defaults.get(key))
                try:
                    self.configure(**{key: active_val})
                except Exception:
                    pass

            self._custom_current_state = "normal"

        elif mode == "disabled":
            # 🔄 Natively freeze list clicks and lock text entry parameters down tightly
            self.configure(state="disabled")

            # Pull your customized high-contrast muted configurations out of your map
            for key in ("fg_color", "border_color", "text_color", "button_color"):
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

    # Instantiate with dummy options test list array values
    widget = sCTkComboBox(base, values=["Channel A (VHF)", "Channel B (UHF)", "Direct Audio Feed"])
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
