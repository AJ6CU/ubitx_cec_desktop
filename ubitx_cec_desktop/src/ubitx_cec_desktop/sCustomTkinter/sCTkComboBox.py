#!/usr/bin/python3
"""
sCTkComboBox

subclass of CTkComboBox

UI source file: sCTkComboBox.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkComboBoxui as baseui
from ThemeableWidget import ThemeableWidget


class sCTkComboBox(baseui.sCTkComboBoxUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # 1. Capture drop-down specific string value arrays early
        values = kw.pop("values", [""])
        command = kw.pop("command", None)
        variable = kw.pop("variable", None)

        # 2. Fire our shared theme logic first
        ThemeableWidget.__init__(self, kw)

        # 3. Store your custom maps safely onto instance memory
        self._local_defaults = self.final_kw
        self._custom_disabled_map = self._widget_disabled_map

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
            pname = args[0]
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "border_color", "text_color", "hover_color"]:
                current_state = str(self.state()).lower()
                val = self._custom_disabled_map.get(pname) if current_state == "disabled" else self._local_defaults.get(
                    pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            return super().configure(pname)

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

        # Pass any remaining properties down through your verified ThemeableWidget configuration track
        if hasattr(super(), "configure"):
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
            self._update_current_visual_state()
            self._custom_current_state = "normal"

        elif mode == "disabled":
            super().configure(state="disabled")

            # Apply custom flat muted gray states safely via super
            for key in (
                    "fg_color", "border_color", "text_color", "button_color",
                    "button_hover_color", "dropdown_fg_color", "dropdown_text_color", "dropdown_hover_color"
            ):
                if key in self._custom_disabled_map:
                    try:
                        super().configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"

    def _update_current_visual_state(self):
        """
        MASTER VISUAL ROUTER: Restores active theme layouts out of memory.
        """
        super().configure(
            fg_color=self.final_kw.get("fg_color", self._local_defaults.get("fg_color")),
            border_color=self.final_kw.get("border_color", self._local_defaults.get("border_color")),
            text_color=self.final_kw.get("text_color", self._local_defaults.get("text_color")),
            button_color=self.final_kw.get("button_color", self._local_defaults.get("button_color")),
            button_hover_color=self.final_kw.get("button_hover_color", self._local_defaults.get("button_hover_color")),
            dropdown_fg_color=self.final_kw.get("dropdown_fg_color", self._local_defaults.get("dropdown_fg_color")),
            dropdown_text_color=self.final_kw.get("dropdown_text_color",
                                                  self._local_defaults.get("dropdown_text_color")),
            dropdown_hover_color=self.final_kw.get("dropdown_hover_color",
                                                   self._local_defaults.get("dropdown_hover_color"))
        )


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x200")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # Instantiate with dummy options test list array values and click reporter logs
    widget = sCTkComboBox(
        base,
        values=["Channel A (VHF)", "Channel B (UHF)", "Direct Audio Feed"],
        command=lambda choice: print(f"ComboBox Option Latched: {choice}")
    )
    widget.pack(expand=True, fill="none", padx=10, pady=10)

    # Test tracking loop sequences on your console window
    widget.state("disabled")
    print("state (Disabled Pass) =", widget.get_state())  # Output: disabled

    widget.state("normal")
    print("state (Normal Pass)   =", widget.get_state())  # Output: normal

    root.mainloop()
