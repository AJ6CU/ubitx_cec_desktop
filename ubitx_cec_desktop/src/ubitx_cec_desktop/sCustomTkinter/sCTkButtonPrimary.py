#!/usr/bin/python3
"""
sCTkButtonPrimary

subclass of CTkButton via Pygubu UI Class Isolation (Primary Action Controller)

UI source file: sCTkButtonPrimary.ui
"""
import customtkinter as ctk
import sCTkButtonPrimaryui as baseui
import sCTkThemes
from ThemeableWidget import ThemeableWidget


class sCTkButtonPrimary(baseui.sCTkButtonPrimaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # 1. Fire our shared theme logic first. It automatically finds "sCTkButtonPrimary" in the JSON
        ThemeableWidget.__init__(self, kw)

        # 2. 🛠️ THE MUTATION SAFEGUARD DEEP COPY:
        # Clone your configuration parameters into completely independent memory structures
        # BEFORE initializing super, protecting active color values from native corruption traps.
        self._local_defaults = dict(self.final_kw)
        self._custom_disabled_map = dict(self._widget_disabled_map)
        self._custom_pressed_map = dict(self._widget_pressed_map)
        self._custom_alarm_map = dict(self._widget_alarm_map)

        # 3. Initialize CustomTkinter natively with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

        self.is_pressed = False
        self.is_alarm = False
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
                if current_state == "disabled" and self._custom_disabled_map:
                    val = self._custom_disabled_map.get(pname)
                elif getattr(self, "is_alarm", False) and self._custom_alarm_map:
                    val = self._custom_alarm_map.get(pname)
                elif getattr(self, "is_pressed", False) and self._custom_pressed_map:
                    val = self._custom_pressed_map.get(pname)
                else:
                    val = self._local_defaults.get(pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            return super().configure(pname)

        # Handle Pygubu positional dictionary merging layers cleanly
        if args and isinstance(args, dict):
            kwargs = args | kwargs

        # -----------------------------------------------------------------
        # ZONE B: SUB-COMPONENT PAYLOAD ROUTING / STATE INTERCEPTION
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
        """Dedicated button state controller."""
        if mode is None:
            return str(super().cget("state")).lower()

        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            try:
                self._canvas.bind("<Enter>", self._on_enter)
                self._canvas.bind("<Leave>", self._on_leave)
                self._canvas.bind("<Button-1>", self._on_clicked)
                self._canvas.bind("<ButtonRelease>", self._on_clicked)
            except Exception:
                pass

            super().configure(state="normal", hover=True)
            self._custom_current_state = "normal"
            self._update_current_visual_state()

        elif mode == "disabled":
            try:
                self._canvas.unbind("<Enter>")
                self._canvas.unbind("<Leave>")
                self._canvas.unbind("<Button-1>")
                self._canvas.unbind("<ButtonRelease>")
            except Exception:
                pass

            super().configure(state="disabled", hover=False)

            # Apply custom flat muted gray states safely out of protected local maps
            config_payload = {}
            for key in ("fg_color", "hover_color", "border_color", "text_color"):
                if key in self._custom_disabled_map and self._custom_disabled_map[key] is not None:
                    config_payload[key] = self._custom_disabled_map[key]

            if config_payload:
                super().configure(**config_payload)

            self._custom_current_state = "disabled"

    def set_pressed(self, pressed: bool):
        """Toggles the visual pressed state of the button cleanly."""
        if getattr(self, "_custom_current_state", "normal") == "disabled" or self.is_alarm:
            return

        self.is_pressed = pressed
        self._update_current_visual_state()

    def set_alarm_state(self, active: bool):
        """Forces the button into a high-visibility warning red state cleanly."""
        if getattr(self, "_custom_current_state", "normal") == "disabled":
            return

        self.is_alarm = active
        if self.is_alarm:
            self.is_pressed = False

        self._update_current_visual_state()

    def _update_current_visual_state(self):
        """
        MASTER VISUAL ROUTER: Dynamically maps configuration layouts out of protected memory.
        """
        # A. ALARM STATE TAKES IMMEDIATE PRIORITY
        if self.is_alarm:
            config_payload = {}
            for key in ("fg_color", "hover_color", "border_color", "text_color"):
                val = self._custom_alarm_map.get(key)
                if val is not None:
                    config_payload[key] = val
            config_payload["hover"] = False
            super().configure(**config_payload)

        # B. PRESSED STATE TAKES SECONDARY PRIORITY
        elif self.is_pressed:
            config_payload = {}
            for key in ("fg_color", "hover_color", "border_color", "text_color"):
                val = self._custom_pressed_map.get(key)
                if val is not None:
                    config_payload[key] = val
            config_payload["hover"] = False
            super().configure(**config_payload)

        # C. FALLBACK TO NORMAL THEME
        else:
            config_payload = {}
            for key in ("fg_color", "hover_color", "border_color", "text_color", "border_width", "corner_radius",
                        "font"):
                val = self._local_defaults.get(key)
                if val is not None:
                    config_payload[key] = val

            config_payload["hover"] = True
            if config_payload:
                super().configure(**config_payload)


# =====================================================================
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import sCTkThemes  # 🔍 Duplicate import kept close for script scannability
from sCTkFrame import sCTkFrame  # Testing application wrapper container frame
from sCTkButtonPrimary import sCTkButtonPrimary

if __name__ == "__main__":
    # Natively resolves your package assets and populates configurations cleanly
    sCTkThemes.apply_sCTkThemes()

    root = ctk.CTk()
    root.geometry("450x300")
    root.title("Primary Command Button Telemetry Bench")

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # 1. Instantiate your custom primary action execution button element
    command_btn = sCTkButtonPrimary(base, text="Primary Action Control")
    command_btn.pack(expand=False, fill="x", padx=40, pady=10)


    # 2. 🛠️ THE ALARM STATE TOGGLE BUTTON TRACK:
    # Alternates alternative selection sequences to force the primary button
    # to jump in and out of high-visibility alarm warning states dynamically.
    def toggle_system_alarm():
        new_alarm_mode = not command_btn.is_alarm
        command_btn.set_alarm_state(new_alarm_mode)

        # Sync toggle button text indicator rules
        btn_alarm_switch.configure(
            text="System Alarm (ACTIVE - Click to Clear)" if new_alarm_mode else "System Alarm"
        )
        print(f"Logged Verification Hook -> command_btn.is_alarm = {command_btn.is_alarm}")


    btn_alarm_switch = ctk.CTkButton(base, text="System Alarm", command=toggle_system_alarm)
    btn_alarm_switch.pack(side="bottom", pady=15)

    # Standard test assertions routine verification sequences
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    command_btn.state("disabled")
    print("state (Disabled Pass) =", command_btn.get_state())

    command_btn.state("normal")
    print("state (Normal Pass)   =", command_btn.get_state())
    print("========================================\n")

    root.mainloop()
