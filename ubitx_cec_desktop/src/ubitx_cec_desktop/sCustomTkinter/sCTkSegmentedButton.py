#!/usr/bin/python3
"""
sCTkSegmentedButton

segmentedButton

UI source file: sCTkSegmentedButton.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
import os
import sCTkSegmentedButtonui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkSegmentedButton(baseui.sCTkSegmentedButtonUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        theme_defaults = THEME_DEFAULTS["sCTkSegmentedButton"]

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # FIX: Pass exactly TWO dictionary arguments to stay synchronized with your master engine class
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array securely
        super().__init__(master, **self.final_kw)

    def state(self, mode: str):
        """Dedicated segmented button row state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            # Natively unlock mouse tracking click streams safely
            self.configure(state="normal")

            # Dynamically pull the exact active colors without hardwired strings
            for key in ("selected_color", "selected_hover_color", "unselected_color", "unselected_hover_color"):
                active_val = self.final_kw.get(key, self._local_defaults.get(key))
                try:
                    self.configure(**{key: active_val})
                except Exception:
                    pass

            # Re-apply crisp active text color settings to the internal navigation label buttons
            if hasattr(self, "_buttons_dict"):
                active_txt = self.final_kw.get("text_color", self._local_defaults.get("text_color"))
                for button in self._buttons_dict.values():
                    button.configure(text_color=active_txt)

            self._custom_current_state = "normal"

        elif mode == "disabled":
            # Natively freeze segment selections entirely
            self.configure(state="disabled")

            # Flatten the background track tabs into an identical muted look layout box
            updates = {}
            for key in ("selected_color", "selected_hover_color", "unselected_color", "unselected_hover_color"):
                if key in self._custom_disabled_map:
                    updates[key] = self._custom_disabled_map[key]

            try:
                self.configure(**updates)
            except Exception:
                pass

            # FIX: Reach deep into the internal button dictionary to override text color configurations!
            # This completely fixes CustomTkinter's native font coloring bug when disabled.
            if hasattr(self, "_buttons_dict"):
                disabled_txt = self._custom_disabled_map.get("text_color", ("#CBD5E1", "#94A3B8"))
                for button in self._buttons_dict.values():
                    button.configure(text_color=disabled_txt)

            self._custom_current_state = "disabled"

    def bind(self, sequence=None, command=None, add=None):
        if "PYGUBU_DESIGNER_RUNNING" in os.environ:
            pass
        else:
            return super().bind(sequence, command, add)


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("500x200")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # Instantiate with a sample parameter selector array
    widget = sCTkSegmentedButton(base, values=["VFO-A", "VFO-B", "MEM-BANK", "SPLIT"])
    widget.pack(expand=False, fill="none", padx=10, pady=10)
    widget.set("VFO-A")

    # Verify our custom cascading state system locks down the entire panel hierarchy instantly!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("state (Disabled Pass) =", widget.get_state())  # Output: disabled

    # FIX: Uncommented and standardized to cleanly verify the component successfully scales back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("state (Normal Pass)   =", widget.get_state())  # Output: normal

    root.mainloop()
