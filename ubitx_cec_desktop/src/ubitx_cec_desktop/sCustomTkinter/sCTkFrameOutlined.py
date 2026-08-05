#!/usr/bin/python3
"""
sCTkFrameOutlined

Standard CTk form but with an outline border

UI source file: sCTkFrameOutlined.ui
"""
import tkinter as tk
import customtkinter as ctk
import tkinter.ttk as ttk
import sCTkFrameOutlinedui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkFrameOutlined(baseui.sCTkFrameOutlinedUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "border_width": 1.5,
            # Light Mode: Crisp Slate Gray | Dark Mode: High-contrast Light Slate Gray
            "border_color": ("#64748B", "#94A3B8"),
            "corner_radius": 8,  # Smooth rounded container edges

            # 🎨 Base Canvas Surface Layers (Crisp solid container cards)
            "fg_color": ("#FFFFFF", "#111827"),

            # ⛔ Muted Disabled Overlay for the container border
            "disabled_map": {
                "border_color": ("#CBD5E1", "#374151")  # Soft silver trace light / Charcoal dark
            }
        }

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

    def state(self, mode: str):
        """
        Universal recursive outlined container state controller.
        Dims the outer boundary stroke lines and automatically commands
        all nested child components to freeze concurrently.
        """
        mode = mode.lower()

        if mode in ("normal", "enabled", "active"):
            # Restore your original crisp outer boundary card lines
            self.configure(border_color=self.final_kw.get("border_color", self._local_defaults.get("border_color")))
            self._custom_current_state = "normal"

        elif mode == "disabled":
            # Apply your custom soft muted silver-gray traces from your dictionary map
            if "border_color" in self._custom_disabled_map:
                self.configure(border_color=self._custom_disabled_map["border_color"])
            self._custom_current_state = "disabled"

        # 🚀 CASCADING NODE DISCOVERY: Discovers and locks down all widgets resting on this card panel frame
        for child in self.winfo_children():
            if hasattr(child, "winfo_children"):
                for inner_child in child.winfo_children():
                    if hasattr(inner_child, "state") and callable(getattr(inner_child, "state")):
                        try:
                            inner_child.state(mode)
                        except Exception:
                            pass

            if hasattr(child, "state") and callable(getattr(child, "state")):
                try:
                    child.state(mode)
                except Exception:
                    pass


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x300")

    # Drops your sharp outlined box panel card cleanly forward onto the canvas window
    widget = sCTkFrameOutlined(root)
    widget.pack(expand=True, fill="both", padx=30, pady=30)

    # Let's drop a themeable input child inside to test the cascade layer profile!
    from sCTkEntryPrimary import sCTkEntryPrimary

    test_input = sCTkEntryPrimary(widget)
    test_input.pack(padx=20, pady=20, fill="x")

    # Disabling the card panel grays out its border and locks down the nested text field instantly
    widget.state("disabled")
    print("Outlined Card panel tracker =", widget.get_state())
    print("Nested child Entry tracker  =", test_input.get_state())

    root.mainloop()
