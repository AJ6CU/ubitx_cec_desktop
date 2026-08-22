#!/usr/bin/python3
"""
sCTkEntryPrimary

subclass of CTkEntry via Pygubu UI Class Isolation (Primary Form Input Field)

UI source file: sCTkEntryPrimary.ui
"""
import customtkinter as ctk
import sCTkEntryPrimaryui as baseui
from ThemeableWidget import ThemeableWidget


class sCTkEntryPrimary(baseui.sCTkEntryPrimaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # 1. PARAMETER POPPING: Capture text field attributes early
        textvariable = kw.pop("textvariable", None)
        placeholder_text = kw.pop("placeholder_text", None)

        # 2. Fire our shared theme logic first to resolve global configurations natively
        ThemeableWidget.__init__(self, kw)

        # 3. 🛠️ THE MUTATION SAFEGUARD DEEP COPY:
        # Isolate your configuration rules inside protected memory structures BEFORE
        # initializing super, preserving your true active settings from native deletion loops.
        self._local_defaults = dict(self.final_kw)
        self._custom_disabled_map = dict(self._widget_disabled_map)

        # 4. Initialize CustomTkinter natively with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

        # 5. Build your inner custom properties using your popped parameters safely
        if textvariable:
            super().configure(textvariable=textvariable)
        if placeholder_text:
            super().configure(placeholder_text=placeholder_text)

        self._custom_current_state = "normal"

    def configure(self, *args, **kwargs):
        """Handles Pygubu designer queries and manages composite state updates safely."""
        if args and len(args) == 1:
            pname = args
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "border_color", "text_color", "placeholder_text_color"]:
                current_state = str(self.state()).lower()
                val = self._custom_disabled_map.get(pname) if current_state == "disabled" else self._local_defaults.get(
                    pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            return super().configure(pname)

        if args and isinstance(args, dict):
            kwargs = args | kwargs

        # Payload Routing
        if "textvariable" in kwargs:
            super().configure(textvariable=kwargs.pop("textvariable"))
        if "placeholder_text" in kwargs:
            super().configure(placeholder_text=kwargs.pop("placeholder_text"))

        if "state" in kwargs:
            target_state = kwargs.pop("state")
            self.state(target_state)

        # Clean empty strings passed by backspacing parameters in Pygubu to prevent exceptions
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
        """Dedicated text entry operational availability state controller."""
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
            for key in ("fg_color", "border_color", "text_color", "placeholder_text_color"):
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
        for key in ("fg_color", "border_color", "text_color", "placeholder_text_color", "border_width", "font"):
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
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkEntryPrimary import sCTkEntryPrimary

if __name__ == "__main__":
    # Natively resolves your package assets and populates configurations cleanly
    sCTkThemes.apply_sCTkThemes()

    root = ctk.CTk()
    root.geometry("450x260")
    root.title("sCTkEntryPrimary Testing Deck")

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # Label notice layer to catch floating text changes
    lbl_monitor = sCTkLabelSecondary(base, text="Console monitor active...")
    lbl_monitor.pack(pady=10)

    # Instantiate your custom input widget field
    input_field = sCTkEntryPrimary(base, placeholder_text="Enter Transceiver Frequency...")
    input_field.pack(expand=False, fill="x", padx=40, pady=10)

    # Attach interactive keyboard binding tracker to dump text entries straight to terminal loop
    input_field.bind("<KeyRelease>", lambda e: lbl_monitor.configure(text=f"Live Buffer: {input_field.get()}"))


    def toggle_operational_state():
        """Toggles the input lane between normal active and dimmed disabled profiles."""
        current_mode = input_field.get_state()
        target = "disabled" if current_mode == "normal" else "normal"

        input_field.configure(state=target)
        btn_toggle.configure(
            text="Lock Input (Set 'disabled')" if target == "normal" else "Unlock Input (Set 'normal')")
        print(f"Logged Verification Hook -> input_field.get_state() = {input_field.get_state()}")


    btn_toggle = ctk.CTkButton(base, text="Lock Input (Set 'disabled')", command=toggle_operational_state)
    btn_toggle.pack(side="bottom", pady=15)

    # Run the interactive boot tracking logs
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    input_field.state("disabled")
    print("state (Disabled Pass) =", input_field.get_state())  # Output: disabled

    input_field.state("normal")
    print("state (Normal Pass)   =", input_field.get_state())  # Output: normal
    print("========================================\n")

    root.mainloop()
