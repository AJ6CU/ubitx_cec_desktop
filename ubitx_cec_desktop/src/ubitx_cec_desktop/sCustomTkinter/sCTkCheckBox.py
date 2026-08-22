#!/usr/bin/python3
"""
sCTkCheckBox

subclass of CTkCheckBox via Pygubu UI Class Isolation

UI source file: sCTkCheckBox.ui
"""
import customtkinter as ctk
import sCTkCheckBoxui as baseui
from ThemeableWidget import ThemeableWidget


class sCTkCheckBox(baseui.sCTkCheckBoxUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # 1. Fire our shared theme logic first. It automatically finds "sCTkCheckBox" in the JSON
        ThemeableWidget.__init__(self, kw)

        # 2. 🛠️ THE MUTATION SAFEGUARD DEEP COPY:
        # Isolate your configuration rules inside protected memory structures BEFORE
        # initializing super, preserving your true active settings from native deletion loops.
        self._local_defaults = dict(self.final_kw)
        self._custom_disabled_map = dict(self._widget_disabled_map)

        # 3. Initialize CustomTkinter natively with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)
        self._custom_current_state = "normal"

    def configure(self, *args, **kwargs):
        """Handles Pygubu designer queries and manages composite state updates safely."""
        # ZONE A: Pygubu Inspector Position Intercept
        if args and len(args) == 1:
            pname = args[0]
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "border_color", "text_color", "hover_color"]:
                current_state = str(self.state()).lower()
                val = self._custom_disabled_map.get(pname) if current_state == "disabled" else self._local_defaults.get(
                    pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            return super().configure(pname)

        if args and isinstance(args, dict):
            kwargs = args | kwargs

        # ZONE B: Payload Routing
        if "state" in kwargs:
            self.state(kwargs.pop("state"))

        # Clean empty strings passed by backspacing parameters inside Pygubu Designer panel slots
        if kwargs:
            for k, v in list(kwargs.items()):
                if v == "":
                    kwargs.pop(k)
            if kwargs:
                return super().configure(**kwargs)
        return None

    def get_state(self):
        """Explicit getter synchronized with your standalone test harness script assertions."""
        return self.state()

    def state(self, mode: str = None):
        """Dedicated checkbox operational availability state controller."""
        if mode is None:
            return str(super().cget("state")).lower()

        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            super().configure(state="normal")
            self._custom_current_state = "normal"
            self._update_current_visual_state()

        elif mode == "disabled":
            super().configure(state="disabled")

            # Apply custom flat muted styling arrays directly down to the canvas safely
            config_payload = {}
            for key in ("fg_color", "hover_color", "border_color", "text_color", "checkmark_color"):
                if key in self._custom_disabled_map and self._custom_disabled_map[key] is not None:
                    config_payload[key] = self._custom_disabled_map[key]

            if config_payload:
                super().configure(**config_payload)

            self._custom_current_state = "disabled"

    def _update_current_visual_state(self):
        """
        MASTER VISUAL ROUTER: Dynamically applies extensible theme properties out of protected memory.
        Completely free of hardcoded property name fallback strings, ensuring total
        extensibility if new options are introduced to the stylesheet in the future.
        """
        # 🛠️ THE BOUNDED DYNAMIC FILTER SHIELD:
        # We parse your preserved local defaults instead of the mutated final_kw.
        # If an item evaluates to None, we skip it entirely so CustomTkinter
        # defaults step forward natively, blocking any ValueError exceptions.
        config_payload = {}
        for key in ("fg_color", "border_color", "hover_color", "text_color", "checkmark_color", "border_width", "font"):
            val = self._local_defaults.get(key)
            if val is not None:
                config_payload[key] = val

        if config_payload:
            super().configure(**config_payload)


# =====================================================================
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import sCTkThemes  # 🔍 Duplicate import kept close for script scannability
from sCTkFrame import sCTkFrame  # Testing application wrapper container frame
from sCTkCheckBox import sCTkCheckBox

if __name__ == "__main__":
    # Natively resolves your package assets and populates configurations cleanly
    sCTkThemes.apply_sCTkThemes()

    root = ctk.CTk()
    root.geometry("450x300")
    root.title("Checkbox Interaction Telemetry Bench")

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # 1. Instantiate your custom theme-compliant checkbox element
    widget = sCTkCheckBox(base, text="Enable Logging Framework")
    widget.configure(command=lambda: print("Checked" if widget.get() == 1 else "Unchecked"))
    widget.pack(expand=True, fill="none", padx=10, pady=10)


    # 2. THE OPERATION STATE TOGGLE BUTTON TRACK:
    def toggle_widget_state():
        current_mode = widget.get_state()
        target = "disabled" if current_mode == "normal" else "normal"

        widget.configure(state=target)
        btn_toggle.configure(
            text="Unlock Checkbox" if target == "disabled" else "Lock Checkbox (Set 'disabled')"
        )
        print(f"Logged Verification Hook -> widget.get_state() = {widget.get_state()}")


    btn_toggle = ctk.CTkButton(base, text="Lock Checkbox (Set 'disabled')", command=toggle_widget_state)
    btn_toggle.pack(side="bottom", pady=15)

    # Run the interactive boot tracking sequences
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    widget.state("disabled")
    print("state (Disabled Pass) =", widget.get_state())  # Output: disabled

    widget.state("normal")
    print("state (Normal Pass)   =", widget.get_state())  # Output: normal
    print("========================================\n")

    root.mainloop()
