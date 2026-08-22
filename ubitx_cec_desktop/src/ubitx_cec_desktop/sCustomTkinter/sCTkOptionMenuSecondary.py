#!/usr/bin/python3
"""
sCTkOptionMenuSecondary

subclass of ctk.CTkFrame acting as a cleanly bordered composite OptionMenu
(Secondary / Helper Selection Controller Variant)

UI source file: sCTkOptionMenuSecondary.ui
"""
import customtkinter as ctk
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

        # 4. 🛠️ THE MUTATION SAFEGUARD DEEP COPY:
        # Clone your configuration parameters into completely independent memory structures
        # BEFORE initializing super, preserving your true active settings from native deletion loops.
        self._local_defaults = dict(self.final_kw)
        self._custom_disabled_map = dict(self._widget_disabled_map)

        # 5. 🛠️ THE INVERSION BLACKLIST FILTER:
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

        # 6. Initialize the native ctk.CTkFrame container using pure filtered frame options
        super().__init__(master, **self.final_kw)

        # 7. Initialize inner CustomTkinter option menu using cleanly popped parameters
        self._menu = ctk.CTkOptionMenu(
            self,
            values=values,
            command=command,
            variable=variable
        )
        self._menu.pack(expand=True, fill="both", padx=2, pady=2)

        # 8. Execute clean layout matching tracks smoothly
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
                val = self._custom_disabled_map.get(pname) if current_state == "disabled" else self._local_defaults.get(pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

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

                # Apply custom map profiles down across composite layout elements safely out of protected memory
                super().configure(
                    border_color=self._custom_disabled_map.get("border_color"),
                    fg_color=self._custom_disabled_map.get("fg_color")
                )
                self._menu.configure(
                    fg_color=self._custom_disabled_map.get("fg_color"),
                    button_color=self._custom_disabled_map.get("fg_color"),
                    text_color=self._custom_disabled_map.get("text_color"),
                    button_hover_color=self._custom_disabled_map.get("fg_color")
                )
                self._custom_current_state = "disabled"

        return self._menu.cget("state")

    def _update_current_visual_state(self):
        """MASTER VISUAL ROUTER: Dynamically applies extensible theme properties out of protected memory."""
        # 1. Capture base frame configuration definitions out of protected copies safely
        frame_config = {}
        for key in ("border_color", "fg_color", "border_width", "corner_radius"):
            if self._local_defaults.get(key) is not None:
                frame_config[key] = self._local_defaults[key]
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
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import customtkinter as ctk
import sCTkThemes                    # 🔍 Duplicate import kept close for script scannability
from sCTkFrame import sCTkFrame      # Testing application wrapper container frame
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkOptionMenuSecondary import sCTkOptionMenuSecondary

if __name__ == "__main__":
    # Natively resolves your package assets and populates configurations cleanly
    sCTkThemes.apply_sCTkThemes()

    root = ctk.CTk()
    root.geometry("450x320")
    root.title("sCTkOptionMenuSecondary Testing Deck")

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # 🛠️ TELEMETRY REPORTING LABEL: Monitors and reports the menu adjustment strings natively
    lbl_monitor = sCTkLabelSecondary(base, text="Active Selection: Filter: Narrow")
    lbl_monitor.pack(pady=10)

    # Instantiate your custom drop-down menu helper element chassis
    menu_field = sCTkOptionMenuSecondary(
        base,
        values=["Filter: Narrow", "Filter: Medium", "Filter: Wide"],
        command=lambda choice: lbl_monitor.configure(text=f"Active Selection: {choice}")
    )
    menu_field.pack(expand=False, fill="x", padx=40, pady=10)
    menu_field.set("Filter: Narrow")

    def toggle_operational_state():
        """Toggles the option menu between normal active and dimmed disabled profiles."""
        current_mode = menu_field.get_state()
        target = "disabled" if current_mode == "normal" else "normal"

        # Explicitly testing the dual-routing capability via configure()
        menu_field.configure(state=target)
        btn_toggle.configure(text="Lock Dropdown (Set 'disabled')" if target == "normal" else "Unlock Dropdown (Set 'normal')")
        print(f"Logged Verification Hook -> menu_field.get_state() = {menu_field.get_state()}")

    btn_toggle = ctk.CTkButton(base, text="Lock Dropdown (Set 'disabled')", command=toggle_operational_state)
    btn_toggle.pack(side="bottom", pady=15)

    # Run the interactive boot tracking logs
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    menu_field.state("disabled")
    print("state (Disabled Pass) =", menu_field.get_state())  # Output: disabled

    menu_field.state("normal")
    print("state (Normal Pass)   =", menu_field.get_state())  # Output: normal
    print("========================================\n")

    root.mainloop()

