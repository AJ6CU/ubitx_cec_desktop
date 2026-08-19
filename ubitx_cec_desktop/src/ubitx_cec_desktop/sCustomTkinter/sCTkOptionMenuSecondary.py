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

        # 2. Assign instance memory BEFORE running master parent initializers
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # 3. Run shared theme logic safely now that variables exist
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # 4. FIXED: Inject a safe fallback layout width natively into final_kw
        # before any constructor execution loops can cause an early crash!
        if "width" not in self.final_kw or self.final_kw["width"] == "":
            self.final_kw["width"] = 160
        if "height" not in self.final_kw or self.final_kw["height"] == "":
            self.final_kw["height"] = 28

        # 5. Initialize the outer bordered container frame layout natively
        super().__init__(master,
                         width=self.final_kw.get("width"),
                         height=self.final_kw.get("height"),
                         border_width=self.final_kw.get("border_width"),
                         border_color=self.final_kw.get("border_color"),
                         fg_color=self.final_kw.get("fg_color"),
                         corner_radius=self.final_kw.get("corner_radius"))

        # Clean unmapped layout properties safely
        self.final_kw.pop("border_color", None)
        self.final_kw.pop("border_width", None)

        # 6. Pass solid dummy colors here to stop CustomTkinter from raising a ValueError!
        self._menu = ctk.CTkOptionMenu(
            self,
            values=values,
            command=command,
            variable=variable)

        self._menu.pack(expand=True, fill="both", padx=2, pady=2)

        # 7. Reach into the core canvas properties and strip colors post-creation!
        # This gives us true transparency without triggering CustomTkinter's type checks.
        try:
            self._menu.configure(fg_color=self.final_kw.get("fg_color"), button_color=self.final_kw.get("fg_color"))
        except Exception:
            if hasattr(self._menu, "_canvas") and self._menu._canvas:
                self._menu._canvas.configure(background="")

    def configure(self, *args, **kwargs):
        """Handles Pygubu designer queries and manages composite state updates safely."""

        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Pygubu Inspector compatibility check)
        # -----------------------------------------------------------------
        if args and len(args) == 1:
            pname = args[0]
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "border_color", "text_color"]:
                current_state = str(self.state()).lower()
                if current_state == "disabled" and self._custom_disabled_map:
                    val = self._custom_disabled_map.get(pname)
                else:
                    val = self._local_defaults.get(pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            # FIXED: Avoid forwarding unnecessary **kwargs dictionary buffers down to super
            return super().configure(pname)

        # -----------------------------------------------------------------
        # ZONE B: SUB-COMPONENT PAYLOAD ROUTING
        # -----------------------------------------------------------------
        # Route dropdown values, bindings, or tkVariables directly into the inner widget
        if "values" in kwargs:
            self._menu.configure(values=kwargs.pop("values"))
        if "command" in kwargs:
            self._menu.configure(command=kwargs.pop("command"))
        if "variable" in kwargs:
            self._menu.configure(variable=kwargs.pop("variable"))

        # -----------------------------------------------------------------
        # ZONE C: STATE CONTROLLER (Apply disabled configurations and cascade parameters)
        # -----------------------------------------------------------------
        if "state" in kwargs:
            target_state = str(kwargs.pop("state")).lower()

            if target_state == "disabled":
                self._menu.configure(state="disabled")
                # Apply disabled configurations out of your custom map profile
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
                # FIXED: Strictly reference local default dictionary indices to enforce hard-stops!
                # If these keys are missing from sCTkThemes, the widget will execute a loud KeyError crash.
                super().configure(
                    border_color=self._local_defaults["border_color"],
                    fg_color=self._local_defaults["fg_color"]
                )
                self._menu.configure(
                    fg_color=self._local_defaults["fg_color"],
                    button_color=self._local_defaults["fg_color"],
                    text_color=self._local_defaults["text_color"]
                )

        # -----------------------------------------------------------------
        # ZONE D: EXECUTE BASE CONTAINER LAYER INITIALIZATION
        # -----------------------------------------------------------------
        if kwargs:
            # Clean out empty strings passed by backspacing parameters in Pygubu to prevent C-engine validation exceptions
            for k, v in list(kwargs.items()):
                if v == "":
                    kwargs.pop(k)
            if kwargs:
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