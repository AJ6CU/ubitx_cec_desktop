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
                val = self._custom_disabled_map.get(pname) if current_state == "disabled" else self._local_defaults.get(
                    pname)
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
            self._update_current_visual_state()
            self._custom_current_state = "normal"

        elif mode == "disabled":
            super().configure(state="disabled")

            # Route custom muted gray configurations safely out of your preserved disabled map
            config_payload = {}
            for key in ("fg_color", "button_color", "button_hover_color", "text_color"):
                if key in self._custom_disabled_map:
                    config_payload[key] = self._custom_disabled_map[key]

            if config_payload:
                super().configure(**config_payload)

            self._custom_current_state = "disabled"

    def _update_current_visual_state(self):
        """
        MASTER VISUAL ROUTER: Restores your true active theme layout configurations out of memory,
        safely falling back to native styles ONLY if a property is unassigned in themes.json.
        """
        config_payload = {}
        for key in ("fg_color", "button_color", "button_hover_color", "text_color"):
            val = self._local_defaults.get(key)
            if val is not None:
                config_payload[key] = val
            else:
                config_payload[key] = ctk.ThemeManager.theme["CTkOptionMenu"].get(key)

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


# !/usr/bin/python3
"""
sCTkOptionMenuPrimary - Standalone Interactive Testing Harness
"""
import customtkinter as ctk
from sCTkFrame import sCTkFrame
# from sCTkOptionMenuPrimary import sCTkOptionMenuPrimary
from sCTkLabelSecondary import sCTkLabelSecondary


def toggle_operational_state():
    """Toggles the option menu between normal active and dimmed disabled profiles."""
    current_mode = option_menu.get_state()
    target = "disabled" if current_mode == "normal" else "normal"

    option_menu.configure(state=target)
    btn_toggle.configure(
        text="Lock Option Menu (Set 'disabled')" if target == "normal" else "Unlock Option Menu (Set 'normal')")
    print(f"Logged Verification Hook -> option_menu.get_state() = {option_menu.get_state()}")


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("450x260")
    root.title("sCTkOptionMenuPrimary Testing Deck")

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # Monitor tag layer to track live menu choices
    lbl_monitor = sCTkLabelSecondary(base, text="Active choice telemetry pending...")
    lbl_monitor.pack(pady=10)

    # Instantiate your custom option menu widget
    option_menu = sCTkOptionMenuPrimary(
        base,
        values=["Initial Mode A", "Initial Mode B"],
        command=lambda choice: lbl_monitor.configure(text=f"Selection Captured: {choice}")
    )
    option_menu.pack(expand=False, fill="x", padx=40, pady=10)

    # Verify that your dynamic updating pipeline operates smoothly
    print("Populating updated parameters track values list...")
    option_menu.update_list(["Mode: USB", "Mode: LSB", "Mode: AM", "Mode: CW"], default_index=1)

    btn_toggle = ctk.CTkButton(base, text="Lock Option Menu (Set 'disabled')", command=toggle_operational_state)
    btn_toggle.pack(side="bottom", pady=15)

    # Run the interactive boot tracking validation checks
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    option_menu.state("disabled")
    print("state (Disabled Pass) =", option_menu.get_state())  # Output: disabled

    option_menu.state("normal")
    print("state (Normal Pass)   =", option_menu.get_state())  # Output: normal
    print("========================================\n")

    root.mainloop()
