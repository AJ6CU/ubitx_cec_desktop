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
import sCTkOptionMenuSecondaryui as baseui

#
# Manual user code
#

class sCTkOptionMenuSecondary(ctk.CTkFrame, ThemeableWidget):

    def __init__(self, master=None, **kw):
        # 1. Capture drop-down specific string value arrays early
        values = kw.pop("values", [""])
        command = kw.pop("command", None)
        variable = kw.pop("variable", None)

        theme_defaults = THEME_DEFAULTS["sCTkOptionMenuSecondary"]

        # 2. FIXED: Assign instance memory BEFORE running master parent initializers
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # 3. Run shared theme logic safely now that variables exist
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # 4. Initialize the outer bordered container frame layout natively
        super().__init__(master,
                         border_width=self.final_kw.get("border_width"),
                         border_color=self.final_kw.get("border_color"),
                         fg_color=self.final_kw.get("fg_color"),
                         corner_radius=self.final_kw.get("corner_radius"))
        # super().__init__(master, **self.final_kw)
        self.final_kw.pop("border_color")
        self.final_kw.pop("border_width")

        # Force a safe baseline layout width so menu text never clips on small cells
        if "width" not in self.final_kw:
            self.configure(width=160)
        #
        # # Pass solid dummy colors here to stop CustomTkinter from raising a ValueError!
        self._menu = ctk.CTkOptionMenu(
            self,
            values=values,
            command=command,
            variable=variable)
        #     font=self.final_kw.get("font"),
        #     dropdown_font=self.final_kw.get("dropdown_font"),
        #     text_color=self.final_kw.get("text_color"),
        #     fg_color=("gray", "gray"),  # Dummy values to pass validation
        #     button_color=("gray", "gray"),  # Dummy values to pass validation
        #     button_hover_color=self.final_kw.get("button_hover_color"),
        #     dropdown_fg_color=self.final_kw.get("dropdown_fg_color"),
        #     dropdown_text_color=self.final_kw.get("dropdown_text_color"),
        #     dropdown_hover_color=self.final_kw.get("dropdown_hover_color"),
        #     corner_radius=0
        # )
        self._menu.pack(expand=True, fill="both", padx=1, pady=1)
        #
        # # Reach into the core canvas properties and strip colors post-creation!
        # # This gives us true transparency without triggering CustomTkinter's type checks.
        try:
            self._menu.configure(fg_color=self.final_kw.get("fg_color"), button_color=self.final_kw.get("fg_color"))
        except Exception:
            # Absolute raw fallback to force lookups
            if hasattr(self._menu, "_canvas"):
                self._menu._canvas.configure(background="")

    def configure(self, *args, **kwargs):
        """Handles Pygubu queries and manages composite state updates safely."""
        # 1. POSITION INTERCEPT LOOP: Synchronizes the live Pygubu workspace preview
        if args and len(args) == 1:
            pname = args
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))
            if pname in ["fg_color", "border_color", "text_color"]:
                current_state = str(self.state()).lower()
                if current_state == "disabled" and self._custom_disabled_map:
                    val = self._custom_disabled_map.get(pname)
                else:
                    val = self._local_defaults.get(pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))
            return super().configure(*args, **kwargs)

        # 2. KEYWORD SANITIZATION: Handles state-based color swapping dynamically
        if "state" in kwargs:
            target_state = str(kwargs["state"]).lower()

            if target_state == "disabled":
                self._menu.configure(state="disabled")
                # Apply disabled colors straight out of your custom map
                super().configure(
                    border_color=self._custom_disabled_map.get("border_color"),
                    fg_color=self._custom_disabled_map.get("fg_color")
                )
                self._menu.configure(
                    fg_color=self._custom_disabled_map.get("fg_color"),
                    button_color=self._custom_disabled_map.get("fg_color"),
                    text_color=self._custom_disabled_map.get("text_color")
                )
            elif target_state in ["normal", "enabled", "active"]:
                self._menu.configure(state="normal")
                # Restore original active theme colors
                super().configure(
                    border_color=self.final_kw.get("border_color", self._local_defaults.get("border_color")),
                    fg_color=self.final_kw.get("fg_color", self._local_defaults.get("fg_color"))
                )
                self._menu.configure(
                    fg_color=self.final_kw.get("fg_color", self._local_defaults.get("fg_color")),
                    button_color=self.final_kw.get("fg_color", self._local_defaults.get("fg_color")),
                    text_color=self.final_kw.get("text_color", self._local_defaults.get("text_color"))
                )

            # Pop state to prevent passing unsupported states down to CTkFrame base
            kwargs.pop("state")

        if kwargs:
            kwargs.pop("values", [""])
            # kwargs.pop("values")
            super().configure(**kwargs)

    def get_state(self):
        """Explicit getter to return the current composite state string safely."""
        return str(self.state()).lower()

    def state(self, mode=None):
        """Dedicated option menu composite state controller."""
        if mode is not None:
            # Route directly through our sanitized keyword config pipeline
            self.configure(state=mode)
        return self._menu.cget("state")

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

    # def bind(self, sequence=None, func=None, add=None):
    #     """
    #     Intercepts and safely wraps binding requests to prevent CustomTkinter
    #     from raising a NotImplementedError inside Pygubu-Designer's previewer.
    #     """
    #     try:
    #         # 1. First, attempt to bind to the outer container CTkFrame natively
    #         return super().bind(sequence, func, add)
    #     except NotImplementedError:
    #         # 2. Fallback gracefully to standard Tkinter syntax if CustomTkinter blocks it
    #         return tk.Frame.bind(self, sequence, func, add)
    #
    # def winfo_children(self):
    #     """
    #     Hides internal child components from Pygubu-Designer's preview engine.
    #     This prevents the previewer from recursively binding handlers to
    #     components that raise a NotImplementedError.
    #     """
    #     # Return an empty list so Pygubu treats this as a single atomic element
    #     return []




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