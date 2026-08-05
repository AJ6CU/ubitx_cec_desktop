#!/usr/bin/python3
"""
sCTkFrame

subclass of Frame tuned for this ux

UI source file: sCTkFrame.ui
"""
import tkinter as tk
import customtkinter as ctk
import tkinter.ttk as ttk
import sCTkFrameui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkFrame(baseui.sCTkFrameUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "border_width": 0,
            "corner_radius": 0,

            # Valid color tuple satisfies type validation checks safely
            "border_color": ("gray", "gray"),

            # Fully allows transparent fills to let background containers bleed through cleanly!
            "fg_color": "transparent"
        }

        # Run our shared theme logic first to sanitize parameters and build self.final_kw
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

    def state(self, mode: str):
        """
        Universal recursive layout container state controller.
        Maintains complete panel transparency while cascading state
        commands down to all nested child components dynamically.
        """
        mode = mode.lower()

        if mode in ("normal", "enabled", "active"):
            self._custom_current_state = "normal"
        elif mode == "disabled":
            self._custom_current_state = "disabled"

        # 🚀 CASCADING NODE DISCOVERY: Discovers inner components at runtime
        # and tunnels state instructions straight down through the transparent layer mesh
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

    # This frame drops on your window completely invisible as a layout placeholder panel container!
    widget = sCTkFrame(root)
    widget.pack(expand=True, fill="both", padx=30, pady=30)

    # Let's drop a themeable input child inside to verify the invisible cascade routing
    from sCTkEntryPrimary import sCTkEntryPrimary

    test_input = sCTkEntryPrimary(widget)
    test_input.pack(padx=20, pady=20, fill="x")

    # Disabling the invisible layout frame now smoothly tunnels down to freeze the input!
    widget.state("disabled")
    print("Transparent Panel tracker  =", widget.get_state())
    print("Nested child Entry tracker =", test_input.get_state())

    root.mainloop()
