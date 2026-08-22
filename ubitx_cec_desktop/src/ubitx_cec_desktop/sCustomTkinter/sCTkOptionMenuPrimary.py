#!/usr/bin/python3
"""
sCTkOptionMenuPrimary

subclass of CTkOptionMenu (Primary Selection Controller)

UI source file: sCTkOptionMenuPrimary.ui
"""
import customtkinter as ctk
import sCTkOptionMenuPrimaryui as baseui
from ThemeableWidget import ThemeableWidget

class sCTkOptionMenuPrimary(baseui.sCTkOptionMenuPrimaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # 1. 🛠️ PARAMETER POPPING: Capture operational list specifics early
        # This keeps complex array strings from polluting final_kw or causing crashes
        values = kw.pop("values", None)
        command = kw.pop("command", None)
        variable = kw.pop("variable", None)

        # 2. Fire our shared theme logic first. It automatically finds the class section inside themes.json
        ThemeableWidget.__init__(self, kw)

        # 3. 🛠️ THE MUTATION SAFEGUARD COPY:
        # Isolate your configuration rules inside protected memory structures BEFORE
        # initializing super, preserving your true active settings from native deletion loops.
        self._local_defaults = dict(self.final_kw)
        self._custom_disabled_map = dict(self._widget_disabled_map)

        # 4. Initialize CustomTkinter natively with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

        # 5. Build your inner custom properties using your popped parameters safely
        if values is not None:
            super().configure(values=values)
        if command is not None:
            super().configure(command=command)
        if variable is not None:
            super().configure(variable=variable)

        self._custom_current_state = "normal"

    def configure(self, *args, **kwargs):
        """Processes Pygubu designer workspace queries and manages theme state updates cleanly."""

        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Feeds values to Pygubu Inspector)
        # -----------------------------------------------------------------
        if args and len(args) == 1:
            pname = args[0]
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "button_color", "button_hover_color", "text_color"]:
                current_state = str(self.state()).lower()
                val = self._custom_disabled_map.get(pname) if current_state == "disabled" else self._local_defaults.get(pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            return super().configure(pname)

        # Handle Pygubu positional dictionary merging layers cleanly
        if args and isinstance(args, dict):
            kwargs = args | kwargs

        # -----------------------------------------------------------------
        # ZONE B: SUB-COMPONENT PAYLOAD ROUTING
        # -----------------------------------------------------------------
        if "values" in kwargs:
            super().configure(values=kwargs.pop("values"))
        if "command" in kwargs:
            super().configure(command=kwargs.pop("command"))
        if "variable" in kwargs:
            super().configure(variable=kwargs.pop("variable"))

        # -----------------------------------------------------------------
        # ZONE C: STATE CONTROLLER (Swaps colors safely based on current mode)
        # -----------------------------------------------------------------
        if "state" in kwargs:
            target_state = str(kwargs.pop("state")).lower()
            self.state(target_state)

        # Clean empty strings passed by backspacing parameters in Pygubu to prevent exceptions
        for k, v in list(kwargs.items()):
            if v == "":
                kwargs.pop(k)

        # -----------------------------------------------------------------
        # ZONE D: RUNTIME KEYWORDS MRO ROUTING PASS
        # -----------------------------------------------------------------
        if kwargs:
            return super().configure(**kwargs)
        return None

    def get_state(self):
        """Explicit getter synchronized with your standalone test harness script assertions."""
        return self.state()

    def state(self, mode: str = None):
        """Standard Tkinter state management mapping helper."""
        if mode is None:
            return str(super().cget("state")).lower()

        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            super().configure(state="normal")
            self._custom_current_state = "normal"
            self._update_current_visual_state()

        elif mode == "disabled":
            super().configure(state="disabled")

            # Route custom muted gray configurations safely out of your preserved disabled map safely
            config_payload = {}
            for key in ("fg_color", "button_color", "button_hover_color", "text_color", "dropdown_fg_color", "dropdown_text_color"):
                if key in self._custom_disabled_map and self._custom_disabled_map[key] is not None:
                    config_payload[key] = self._custom_disabled_map[key]

            if config_payload:
                super().configure(**config_payload)

            self._custom_current_state = "disabled"

    def _update_current_visual_state(self):
        """
        MASTER VISUAL ROUTER: Dynamically applies extensible theme properties out of protected memory.
        Completely free of hardcoded property name fallback strings, ensuring total extensibility.
        """
        # 🛠️ THE BOUNDED DYNAMIC FILTER SHIELD:
        # We parse your preserved local defaults instead of the mutated final_kw.
        # If an item evaluates to None, it is skipped entirely so CustomTkinter
        # defaults step forward natively, blocking any ValueError exceptions.
        config_payload = {}
        for key in ("fg_color", "button_color", "button_hover_color", "text_color", "dropdown_fg_color", "dropdown_text_color", "font"):
            val = self._local_defaults.get(key)
            if val is not None:
                config_payload[key] = val

        if config_payload:
            super().configure(**config_payload)

    def update_list(self, new_values: list, default_index: int = 0):
        """Safely updates the items list and resets the visible value."""
        if not new_values:
            self.configure(values=[""])
            self.set("")
            return

        self.configure(values=new_values)

        # Guard against index out of bounds errors
        if default_index < len(new_values):
            self.set(new_values[default_index])
        else:
            self.set(new_values[0])


# =====================================================================
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import sCTkThemes                    # 🔍 Duplicate import kept close for script scannability
from sCTkFrame import sCTkFrame      # Testing application wrapper container frame
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkOptionMenuPrimary import sCTkOptionMenuPrimary

if __name__ == "__main__":
    # Natively resolves your package assets and populates configurations cleanly
    sCTkThemes.apply_sCTkThemes()

    root = ctk.CTk()
    root.geometry("450x320")
    root.title("sCTkOptionMenuPrimary Testing Deck")

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # Label notice layer to monitor menu adjustments
    lbl_monitor = sCTkLabelSecondary(base, text="Active Selection: None")
    lbl_monitor.pack(pady=10)

    # Instantiate your custom drop-down menu element
    menu_field = sCTkOptionMenuPrimary(
        base,
        values=["Mode 1: USB", "Mode 2: LSB", "Mode 3: CW"],
        command=lambda choice: lbl_monitor.configure(text=f"Active Selection: {choice}")
    )
    menu_field.pack(expand=False, fill="x", padx=40, pady=10)
    menu_field.set("Mode 1: USB")

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
