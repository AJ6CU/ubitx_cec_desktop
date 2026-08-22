#!/usr/bin/python3
"""
sCTkComboBox

subclass of CTkComboBox via Pygubu UI Class Isolation

UI source file: sCTkComboBox.ui
"""
import customtkinter as ctk
import sCTkComboBoxui as baseui
from ThemeableWidget import ThemeableWidget


class sCTkComboBox(baseui.sCTkComboBoxUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # 1. PARAMETER POPPING: Capture combobox-specific tracking parameters early
        values = kw.pop("values", [""])
        command = kw.pop("command", None)
        variable = kw.pop("variable", None)

        # 2. Fire our shared theme logic first. It automatically finds "sCTkComboBox" in the JSON
        ThemeableWidget.__init__(self, kw)

        # 3. 🛠️ THE MUTATION SAFEGUARD DEEP COPY:
        # Isolate your configuration rules inside protected memory structures BEFORE
        # initializing super, preserving your true active settings from native deletion loops.
        self._local_defaults = dict(self.final_kw)
        self._custom_disabled_map = dict(self._widget_disabled_map)

        # 4. Initialize CustomTkinter natively with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

        # 5. Build your inner custom properties using your popped parameters safely
        if values:
            super().configure(values=values)

            # 🛠️ THE STARTUP FIX: If options are present, manually force the combobox
            # to snap to the very first string item inside your array, erasing the class text!
            if isinstance(values, list) and len(values) > 0 and values[0] != "":
                self.set(values[0])

        if command:
            super().configure(command=command)
        if variable:
            super().configure(variable=variable)

        self._custom_current_state = "normal"

    def configure(self, *args, **kwargs):
        """Handles Pygubu designer queries and manages composite state updates safely."""

        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Pygubu Inspector compatibility check)
        # -----------------------------------------------------------------
        if args and len(args) == 1:
            pname = args
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
        # ZONE C: STATE & FRAMEWORK INTERCEPTION MRO PASS
        # -----------------------------------------------------------------
        if "state" in kwargs:
            target_state = kwargs.pop("state")
            self.state(target_state)

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
        """Dedicated combobox state controller."""
        if mode is None:
            return str(super().cget("state")).lower()

        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            super().configure(state="normal")
            self._custom_current_state = "normal"
            self._update_current_visual_state()

        elif mode == "disabled":
            super().configure(state="disabled")

            # Apply custom flat muted gray states safely via super out of your protected local maps
            config_payload = {}
            for key in (
                    "fg_color", "border_color", "text_color", "button_color",
                    "button_hover_color", "dropdown_fg_color", "dropdown_text_color", "dropdown_hover_color"
            ):
                if key in self._custom_disabled_map and self._custom_disabled_map[key] is not None:
                    config_payload[key] = self._custom_disabled_map[key]

            if config_payload:
                super().configure(**config_payload)

            self._custom_current_state = "disabled"

    def _update_current_visual_state(self):
        """
        MASTER VISUAL ROUTER: Dynamically applies extensible theme properties out of protected memory.
        Completely free of hardcoded property name fallback strings, ensuring total
        extensibility if new options are introduced to the framework.
        """
        # 🛠️ THE BOUNDED DYNAMIC FILTER SHIELD:
        # We parse your preserved local defaults instead of the mutated final_kw.
        # If an item evaluates to None, it is skipped entirely so CustomTkinter
        # defaults step forward natively, blocking any ValueError exceptions.
        config_payload = {}
        for key in (
                "fg_color", "border_color", "text_color", "button_color", "button_hover_color",
                "dropdown_fg_color", "dropdown_text_color", "dropdown_hover_color", "border_width", "font"
        ):
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
from sCTkComboBox import sCTkComboBox

if __name__ == "__main__":
    # Natively resolves your package assets and populates configurations cleanly
    sCTkThemes.apply_sCTkThemes()

    root = ctk.CTk()
    root.geometry("450x300")
    root.title("ComboBox Interaction Telemetry Bench")

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # 1. Instantiate with dummy options test list array values and click reporter logs
    widget = sCTkComboBox(
        base,
        values=["Channel A (VHF)", "Channel B (UHF)", "Direct Audio Feed"],
        command=lambda choice: print(f"ComboBox Option Latched: {choice}")
    )
    widget.pack(expand=True, fill="none", padx=10, pady=10)


    # 2. THE OPERATION STATE TOGGLE BUTTON TRACK:
    def toggle_widget_state():
        current_mode = widget.get_state()
        target = "disabled" if current_mode == "normal" else "normal"

        widget.configure(state=target)
        btn_toggle.configure(
            text="Unlock Dropdown" if target == "disabled" else "Lock Dropdown (Set 'disabled')"
        )
        print(f"Logged Verification Hook -> widget.get_state() = {widget.get_state()}")


    btn_toggle = ctk.CTkButton(base, text="Lock Dropdown (Set 'disabled')", command=toggle_widget_state)
    btn_toggle.pack(side="bottom", pady=15)

    # Test tracking loop sequences on your console window
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    widget.state("disabled")
    print("state (Disabled Pass) =", widget.get_state())  # Output: disabled

    widget.state("normal")
    print("state (Normal Pass)   =", widget.get_state())  # Output: normal
    print("========================================\n")

    root.mainloop()
