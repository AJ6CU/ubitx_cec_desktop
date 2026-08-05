#!/usr/bin/python3
"""
sCTkOptionMenuSecondary

subclass of CTkFrame acting as a cleanly bordered composite OptionMenu
(Secondary / Helper Selection Controller Variant)

UI source file: sCTkOptionMenuSecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#

class sCTkOptionMenuSecondary(ctk.CTkFrame, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # Capture drop-down specific string value arrays early
        values = kw.pop("values", [""])
        command = kw.pop("command", None)
        variable = kw.pop("variable", None)

        theme_defaults = THEME_DEFAULTS["sCTkOptionMenuSecondary"]

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize the outer bordered container frame layout natively
        super().__init__(master,
                         border_width=self.final_kw.get("border_width"),
                         border_color=self.final_kw.get("border_color"),
                         fg_color=self.final_kw.get("fg_color"),
                         corner_radius=self.final_kw.get("corner_radius"))

        # Pass solid dummy colors here to stop CustomTkinter from raising a ValueError!
        self._menu = ctk.CTkOptionMenu(
            self,
            values=values,
            command=command,
            variable=variable,
            font=self.final_kw.get("font"),
            dropdown_font=self.final_kw.get("dropdown_font"),
            text_color=self.final_kw.get("text_color"),
            fg_color=("gray", "gray"),  # Dummy values to pass validation
            button_color=("gray", "gray"),  # Dummy values to pass validation
            button_hover_color=self.final_kw.get("button_hover_color"),
            dropdown_fg_color=self.final_kw.get("dropdown_fg_color"),
            dropdown_text_color=self.final_kw.get("dropdown_text_color"),
            dropdown_hover_color=self.final_kw.get("dropdown_hover_color"),
            corner_radius=0
        )
        self._menu.pack(expand=True, fill="both", padx=1, pady=1)

        # Reach into the core canvas properties and strip colors post-creation!
        # This gives us true transparency without triggering CustomTkinter's type checks.
        try:
            self._menu.configure(fg_color=self.final_kw.get("fg_color"), button_color=self.final_kw.get("fg_color"))
        except Exception:
            # Absolute raw fallback to force lookups
            if hasattr(self._menu, "_canvas"):
                self._menu._canvas.configure(background="")

    def state(self, mode: str):
        """Dedicated option menu composite state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            self._menu.configure(state="normal")

            # Apply border and frame card updates cleanly
            self.configure(
                border_color=self.final_kw.get("border_color", self._local_defaults.get("border_color")),
                fg_color=self.final_kw.get("fg_color", self._local_defaults.get("fg_color"))
            )
            self._menu.configure(
                text_color=self.final_kw.get("text_color", self._local_defaults.get("text_color"))
            )
            self._custom_current_state = "normal"

        elif mode == "disabled":
            self._menu.configure(state="disabled")

            # Pull your customized high-contrast muted configurations out of your map
            if "border_color" in self._custom_disabled_map:
                self.configure(border_color=self._custom_disabled_map["border_color"])
            if "fg_color" in self._custom_disabled_map:
                self.configure(fg_color=self._custom_disabled_map["fg_color"])
            if "text_color" in self._custom_disabled_map:
                self._menu.configure(text_color=self._custom_disabled_map["text_color"])

            self._custom_current_state = "disabled"

    def update_list(self, new_values: list, default_index: int = 0):
        """Safely updates the items list and resets the visible value."""
        if not new_values:
            self._menu.configure(values=[""])
            self._menu.set("")
            return

        self._menu.configure(values=new_values)

        if default_index < len(new_values):
            self._menu.set(new_values[default_index])
        else:
            self._menu.set(new_values[0])

    def set(self, value: str):
        self._menu.set(value)

    def get(self) -> str:
        return self._menu.get()


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x200")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkOptionMenuSecondary(base, values=["Helper Option A", "Helper Option B"])
    widget.pack(expand=True, fill="x", padx=40, pady=10)

    print("Populating secondary parameters track values list...")
    widget.update_list(["Filter: Narrow", "Filter: Medium", "Filter: Wide"], default_index=0)

    # Verify our custom cascading state system locks down the composite selector!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("state (Disabled Sequence) =", widget.get_state())  # Output: disabled

    # Verify the cascade pipeline unlocks everything smoothly right back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("state (Normal Sequence)   =", widget.get_state())  # Output: normal

    root.mainloop()