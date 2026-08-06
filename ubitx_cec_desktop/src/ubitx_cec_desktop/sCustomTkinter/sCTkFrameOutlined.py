#!/usr/bin/python3
"""
sCTkFrameOutlined

Standard CTk form but with an outline border

UI source file: sCTkFrameOutlined.ui
"""
import tkinter as tk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
import tkinter.ttk as ttk
import sCTkFrameOutlinedui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkFrameOutlined(baseui.sCTkFrameOutlinedUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        theme_defaults = THEME_DEFAULTS["sCTkFrameOutlined"]

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Centralized cleanup using Themeable Widget parsing before creation pass!
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

        # Self-correcting parent background lookup check loop
        try:
            parent_bg = self.master.cget("fg_color")
        except Exception:
            try:
                parent_bg = self.master.cget("bg")
            except Exception:
                parent_bg = ("#112A4B", "#1A1A1A")

        # Applied parent color to bg_color, keeping your crisp foreground layers intact!
        self.configure(bg_color=parent_bg)


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x300")

    # Drops your sharp outlined box panel card cleanly forward onto the canvas window
    widget = sCTkFrameOutlined(root)
    widget.pack(expand=True, fill="both", padx=30, pady=30)

    # Let's drop a themeable input child inside to test the cascade layer profile!
    from sCTkEntryPrimary import sCTkEntryPrimary

    # FIX: Safely discover and route the child component to the frame's true inner content container
    # to maintain pristine geometric alignment with Pygubu Designer specifications!
    target_container = getattr(widget, "w_child_container", widget)

    test_input = sCTkEntryPrimary(target_container)
    test_input.pack(padx=20, pady=20, fill="x")

    # Verify our custom cascading state system locks down the container block!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("Outlined Card panel tracker =", widget.get_state())
    print("Nested child Entry tracker  =", test_input.get_state())

    # Verify the cascade pipeline unlocks everything smoothly right back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("Outlined Card panel tracker =", widget.get_state())
    print("Nested child Entry tracker  =", test_input.get_state())

    root.mainloop()

