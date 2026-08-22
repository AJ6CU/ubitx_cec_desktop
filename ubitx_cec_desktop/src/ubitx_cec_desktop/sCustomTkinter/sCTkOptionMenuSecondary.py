#!/usr/bin/python3
"""
sCTkOptionMenuSecondary

subclass of ctk.CTkFrame acting as a cleanly bordered composite OptionMenu
(Secondary / Helper Selection Controller Variant)

UI source file: sCTkOptionMenuSecondary.ui
"""
import customtkinter as ctk
import sCTkThemes
from ThemeableWidget import ThemeableWidget


class sCTkOptionMenuSecondary(ctk.CTkFrame, ThemeableWidget):

    def __init__(self, master=None, width=160, height=28, **kw):
        # 1. PARAMETER POPPING: Capture menu-specific operational attributes early
        values = kw.pop("values", [""])
        command = kw.pop("command", None)
        variable = kw.pop("variable", None)

        # 2. Assign standard constructor fallback geometric limits directly
        kw.setdefault("width", width)
        kw.setdefault("height", height)

        # 3. Fire our shared theme logic to resolve json asset lookups safely
        ThemeableWidget.__init__(self, kw)

        # 4. 🛠️ THE INVERSION BLACKLIST FILTER:
        # Dynamically separate dropdown-specific keywords out of final_kw.
        # This protects the parent frame layer from seeing illegal arguments
        # (like 'font') and throwing an immediate CustomTkinter ValueError.
        MENU_KEYS = {
            "font", "dropdown_font", "text_color", "disabled_text_color",
            "dropdown_fg_color", "dropdown_text_color", "dropdown_hover_color",
            "button_hover_color"
        }
        self._menu_theme_kw = {}
        for key in MENU_KEYS:
            if key in self.final_kw:
                self._menu_theme_kw[key] = self.final_kw.pop(key)

        # 5. Initialize the native ctk.CTkFrame container using pure filtered frame options
        super().__init__(master, **self.final_kw)

        # 6. Initialize inner CustomTkinter option menu using cleanly popped parameters
        self._menu = ctk.CTkOptionMenu(
            self,
            values=values,
            command=command,
            variable=variable
        )
        self._menu.pack(expand=True, fill="both", padx=2, pady=2)

        # 7. Execute clean layout matching tracks smoothly
        self._update_current_visual_state()
        self._custom_current_state = "normal"

    def configure(self, *args, **kwargs):
        """Handles Pygubu designer queries and manages composite state updates safely."""
        if args and len(args) == 1:
            pname = args[0]
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "border_color", "text_color", "width", "height"]:
                current_state = str(self.state()).lower()
                val = self._widget_disabled_map.get(pname) if current_state == "disabled" else self.final_kw.get(pname)
                return (pname, pname, pname, str(self.final_kw.get(pname)), str(val))

            return super().configure(pname)

        if args and isinstance(args, dict):
            kwargs = args | kwargs

        # Dynamic Payload Routing Passes
        if "values" in kwargs:
            self._menu.configure(values=kwargs.pop("values"))
        if "command" in kwargs:
            self._menu.configure(command=kwargs.pop("command"))
        if "variable" in kwargs:
            self._menu.configure(variable=kwargs.pop("variable"))

        if "state" in kwargs:
            self.state(kwargs.pop("state"))

        if kwargs:
            # Clear empty strings passed by backspacing variables inside Pygubu Designer panel slots
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
            mode = mode.lower()
            if mode in ("normal", "enabled", "active"):
                self._menu.configure(state="normal")
                self._update_current_visual_state()
                self._custom_current_state = "normal"
            elif mode == "disabled":
                self._menu.configure(state="disabled")

                # Apply custom map profiles down across composite layout elements safely
                super().configure(
                    border_color=self._widget_disabled_map.get("border_color"),
                    fg_color=self._widget_disabled_map.get("fg_color")
                )
                self._menu.configure(
                    fg_color=self._widget_disabled_map.get("fg_color"),
                    button_color=self._widget_disabled_map.get("fg_color"),
                    text_color=self._widget_disabled_map.get("text_color"),
                    button_hover_color=self._widget_disabled_map.get("fg_color")
                )
                self._custom_current_state = "disabled"

        return self._menu.cget("state")

    def _update_current_visual_state(self):
        """MASTER VISUAL ROUTER: Dynamically applies extensible theme properties out of memory."""
        # 1. Capture base frame configuration definitions
        frame_config = {}
        for key in ("border_color", "fg_color", "border_width", "corner_radius"):
            if self.final_kw.get(key) is not None:
                frame_config[key] = self.final_kw[key]
        if frame_config:
            super().configure(**frame_config)

        # 2. Compile and map inner menu text and color properties dynamically
        menu_payload = dict(self._menu_theme_kw)

        # Merge transparent ghost layout characteristics cleanly
        if "fg_color" in frame_config:
            menu_payload["fg_color"] = frame_config["fg_color"]
            menu_payload["button_color"] = frame_config["fg_color"]
            menu_payload.setdefault("button_hover_color", frame_config["fg_color"])

        if menu_payload:
            self._menu.configure(**menu_payload)

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


# =====================================================================
# 🛠️ INTEGRATED REPOSITORY COMPLIANT INLINE TESTING HARNESS
# =====================================================================
import sCTkThemes
from sCTkOptionMenuSecondary import sCTkOptionMenuSecondary

if __name__ == "__main__":

    sCTkThemes.apply_sCTkThemes()

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
    print("state (Disabled Sequence) =", widget.get_state())

    # Verify the cascade pipeline unlocks everything smoothly right back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("state (Normal Sequence)   =", widget.get_state())

    root.mainloop()
