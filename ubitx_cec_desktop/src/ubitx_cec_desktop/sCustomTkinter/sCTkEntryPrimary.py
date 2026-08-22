#!/usr/bin/python3
"""
sCTkEntryPrimary

subclass of CTkEntry (Primary Form Input Field)
"""
import customtkinter as ctk
import sCTkEntryPrimaryui as baseui
from ThemeableWidget import ThemeableWidget


class sCTkEntryPrimary(baseui.sCTkEntryPrimaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # 1. PARAMETER POPPING: Capture text field attributes early
        textvariable = kw.pop("textvariable", None)
        placeholder_text = kw.pop("placeholder_text", None)

        # 2. Fire our shared theme logic first to resolve global configurations
        ThemeableWidget.__init__(self, kw)

        # 3. 🛠️ THE MUTATION SAFEGUARD FIX:
        # CustomTkinter's super().__init__ deletes keys directly out of dictionaries.
        # We explicitly save a true copy of final_kw into self._local_defaults BEFORE
        # initializing super. This ensures your normal state settings remain permanently preserved!
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
            self._update_current_visual_state()
            self._custom_current_state = "normal"

        elif mode == "disabled":
            super().configure(state="disabled")

            # Route custom muted gray configurations safely out of your preserved disabled map
            for key in ("fg_color", "border_color", "text_color", "placeholder_text_color"):
                if key in self._custom_disabled_map:
                    try:
                        super().configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"

    def _update_current_visual_state(self):
        """
        MASTER VISUAL ROUTER: Restores your true active theme layout configurations out of memory,
        safely falling back to native styles ONLY if a property is unassigned in themes.json.
        """
        # 🛠️ THE NORMAL STATE RESOLUTION:
        # We read directly out of your protected self._local_defaults copy instead of final_kw.
        # This completely guarantees that your true active configuration settings are pulled!
        config_payload = {}
        for key in ("fg_color", "border_color", "text_color", "placeholder_text_color"):
            val = self._local_defaults.get(key)
            if val is not None:
                config_payload[key] = val
            else:
                # If your themes.json skips configuring a unique active property,
                # fall back cleanly onto CustomTkinter's built-in theme parameters to prevent None type crashes.
                config_payload[key] = ctk.ThemeManager.theme["CTkEntry"].get(key)

        if config_payload:
            super().configure(**config_payload)


# !/usr/bin/python3
"""
sCTkEntryPrimary - Standalone Interactive Testing Harness
"""
import customtkinter as ctk
from sCTkFrame import sCTkFrame
# from sCTkEntryPrimary import sCTkEntryPrimary
from sCTkLabelSecondary import sCTkLabelSecondary


def toggle_operational_state():
    """Toggles the input lane between normal active and dimmed disabled profiles."""
    current_mode = input_field.get_state()
    target = "disabled" if current_mode == "normal" else "normal"

    input_field.configure(state=target)
    btn_toggle.configure(text="Lock Input (Set 'disabled')" if target == "normal" else "Unlock Input (Set 'normal')")
    print(f"Logged Verification Hook -> input_field.get_state() = {input_field.get_state()}")


if __name__ == "__main__":
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
