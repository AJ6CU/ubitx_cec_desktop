#!/usr/bin/python3
"""
sCTkRadioButton

derived from radioButton

UI source file: sCTkRadioButton.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkRadioButtonui as baseui
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#

class sCTkRadioButton(baseui.sCTkRadioButtonUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # 📐 Universal Flat Theme Defaults
        theme_defaults = {
            "font": ("Arial", 15, "normal"),

            # 📝 Text matching your standard labels and checkboxes
            "text_color": ("#374151", "#D1D5DB"),

            # 🔲 Thicker unchecked rings give hover highlights an excellent surface area to pop!
            "border_width_unchecked": 4,
            "border_width_checked": 6,
            "border_color": ("#64748B", "#94A3B8"),

            # 🎨 Active selection dot (matches OptionMenu/ComboBox base blue)
            "fg_color": ("#1A4375", "#2471A3"),

            # 🖱️ High-contrast navy/blue tones for tracking cursor movements
            "hover_color": ("#112A4B", "#1F618D"),

            # ⛔ Muted Soft-Contrast Disabled Overlay
            "disabled_map": {
                "text_color": ("#94A3B8", "#64748B"),
                "fg_color": ("#CBD5E1", "#374151"),  # Inner dot drops to a soft silver in light mode
                "border_color": ("#CBD5E1", "#475569")  # Outer circle matches the soft silver trace look
            }
        }

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries safely
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

    def state(self, mode: str):
        """Dedicated radio button state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            # Natively unlock mouse clicking selections
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
            # Natively freeze indicators and click tracking layers
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
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x150")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # Simple explicit string tracking variable to connect radio groups
    radio_var = tk.StringVar(value="VFO_A")

    widget = sCTkRadioButton(base, text="Primary VFO A Link Target", variable=radio_var, value="VFO_A")
    # 🔄 FIX: Settled expand to False to lock geometry baseline metrics cleanly
    widget.pack(expand=False, fill="none", padx=10, pady=10)

    # Test tracking loop sequences on your console window
    widget.state("disabled")
    print("state =", widget.get_state())  # Output: disabled

    widget.state("normal")
    print("state =", widget.get_state())  # Output: normal

    root.mainloop()
