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

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # FIX: Pass exactly TWO dictionary arguments to stay synchronized with your master engine class
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

    def state(self, mode: str):
        """Dedicated draggable slider state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            # Natively unlock mouse tracking dragging pipelines safely
            self.configure(state="normal")

            # Dynamically pull the exact active colors straight out of your original values
            for key in ("fg_color", "progress_color", "button_color", "button_hover_color"):
                active_val = self.final_kw.get(key, self._local_defaults.get(key))
                try:
                    self.configure(**{key: active_val})
                except Exception:
                    pass

            self._custom_current_state = "normal"

        elif mode == "disabled":
            # Natively freeze sliders and lock out user manipulation parameters
            self.configure(state="disabled")

            # Pull your customized high-contrast muted configurations out of your map
            for key in ("fg_color", "progress_color", "button_color"):
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
