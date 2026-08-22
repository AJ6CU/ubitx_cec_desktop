#!/usr/bin/python3
"""
sCTkCheckBox

subclass of CTkCheckBox

UI source file: sCTkCheckBox.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkCheckBoxui as baseui
from ThemeableWidget import ThemeableWidget


class sCTkCheckBox(baseui.sCTkCheckBoxUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # 1. Fire our shared theme logic first. It automatically finds "sCTkCheckBox" in the JSON
        ThemeableWidget.__init__(self, kw)

        # 2. Store your custom maps safely onto instance memory
        self._local_defaults = self.final_kw
        self._custom_disabled_map = self._widget_disabled_map

        # 3. Initialize CustomTkinter natively with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

    def configure(self, *args, **kwargs):
        """Handles Pygubu designer queries and manages composite state updates safely."""
        # ZONE A: Pygubu Inspector Position Intercept
        if args and len(args) == 1:
            pname = args[0]  # Fix array indexing unpacking
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "border_color", "text_color", "hover_color"]:
                current_state = str(self.state()).lower()
                val = self._custom_disabled_map.get(pname) if current_state == "disabled" else self._local_defaults.get(
                    pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            return super().configure(pname)

        # ZONE B: Payload Routing
        if "state" in kwargs:
            self.state(kwargs.pop("state"))

        if hasattr(super(), "configure"):
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
            # 🛠️ CLEANED: Bypassed volatile manual canvas re-binding hooks
            super().configure(state="normal")
            self._update_current_visual_state()
            self._custom_current_state = "normal"

        elif mode == "disabled":
            # 🛠️ CLEANED: Bypassed volatile manual canvas unbinding hooks
            super().configure(state="disabled")

            # Apply custom flat muted styling arrays directly down to the canvas
            for key in ("fg_color", "hover_color", "border_color", "text_color"):
                if key in self._custom_disabled_map:
                    try:
                        super().configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"

    def _update_current_visual_state(self):
        """MASTER VISUAL ROUTER: Restores active theme dimensions out of local configuration dictionaries."""
        super().configure(
            fg_color=self.final_kw.get("fg_color", self._local_defaults.get("fg_color")),
            border_color=self.final_kw.get("border_color", self._local_defaults.get("border_color")),
            hover_color=self.final_kw.get("hover_color", self._local_defaults.get("hover_color")),
            text_color=self.final_kw.get("text_color", self._local_defaults.get("text_color"))
        )


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x200")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkCheckBox(base, text="Enable Logging Framework")
    # 🛠️ Attach standard interactive command tracking cleanly
    widget.configure(command=lambda: print("Checked" if widget.get() == 1 else "Unchecked"))
    widget.pack(expand=True, fill="none", padx=10, pady=10)

    # Run the interactive boot tracking sequences
    widget.state("disabled")
    print("state (Disabled Pass) =", widget.get_state())  # Output: disabled

    # widget.state("normal")
    # print("state (Normal Pass)   =", widget.get_state())  # Output: normal

    root.mainloop()
