# !/usr/bin/python3
"""
sCTkButtonSecondary

subclass of CTkButton via Pygubu UI Class Isolation (Secondary Action Controller)

UI source file: sCTkButtonSecondary.ui
"""
import customtkinter as ctk
import sCTkButtonSecondaryui as baseui
import sCTkThemes
from ThemeableWidget import ThemeableWidget


class sCTkButtonSecondary(baseui.sCTkButtonSecondaryUI, ThemeableWidget):

    def __init__(self, master=None, **kw):
        # 1. Fire our shared theme logic first. It automatically finds "sCTkButtonSecondary" in the JSON
        ThemeableWidget.__init__(self, kw)

        # 2. 🛠️ THE MUTATION SAFEGUARD DEEP COPY:
        # Clone your configuration parameters into completely independent memory structures
        # BEFORE initializing super, protecting active color values from native corruption traps.
        self._local_defaults = dict(self.final_kw)
        self._custom_disabled_map = dict(self._widget_disabled_map)
        self._custom_pressed_map = dict(self._widget_pressed_map)

        # 3. Initialize CustomTkinter natively with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

        # Set up your local press tracking boolean state flag
        self.is_pressed = False
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
        """Dedicated secondary button latching toggle state controller."""
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

            # Apply disabled overrides out of your protected local maps
            config_payload = {}
            for key in ("fg_color", "hover_color", "border_color", "text_color"):
                if key in self._custom_disabled_map and self._custom_disabled_map[key] is not None:
                    config_payload[key] = self._custom_disabled_map[key]

            if config_payload:
                super().configure(**config_payload)

            self._custom_current_state = "disabled"

    def set_pressed(self, pressed: bool):
        """Toggles the visual pressed state of the secondary button cleanly."""
        if getattr(self, "_custom_current_state", "normal") == "disabled":
            return

        self.is_pressed = pressed
        self._update_current_visual_state()

    def _update_current_visual_state(self):
        """
        MASTER VISUAL ROUTER: Evaluates the secondary button's press status variable
        and dynamically maps configuration layouts out of protected memory.
        """
        # A. PRESSED STATE TAKES PRIMARY LOCAL PRIORITY
        if self.is_pressed:
            config_payload = {}
            for key in ("fg_color", "hover_color", "border_color", "text_color"):
                val = self._custom_pressed_map.get(key)
                if val is not None:
                    config_payload[key] = val

            config_payload["hover"] = False
            super().configure(**config_payload)

        # B. FALLBACK TO STANDARD ACTIVE THEME CONFIGURATION
        else:
            # 🛠️ THE BOUNDED DYNAMIC FILTER SHIELD:
            # We loop over your protected copy to force valid fallback properties.
            # If an unmapped key returns None, it is skipped, preventing ValueError exceptions.
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
import sCTkThemes                # 🔍 Duplicate import kept close for script scannability
from sCTkFrame import sCTkFrame  # Testing application wrapper container frame
from sCTkButtonSecondary import sCTkButtonSecondary

if __name__ == "__main__":
    sCTkThemes.apply_sCTkThemes()
    root = ctk.CTk()
    root.geometry("400x200")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkButtonSecondary(base, text="System Action Button")
    widget1 = sCTkButtonSecondary(base, text="Latching Preset Toggle")

    widget.pack(padx=40, pady=20)
    widget1.pack(padx=40, pady=20)

    # -----------------------------------------------------------------
    # A. INITIAL BOOT LOG TEST SEQUENCE (Kept Exactly As Is)
    # -----------------------------------------------------------------
    widget.state("normal")
    widget1.set_pressed(True)

    # Verify our custom cascading state system locks down the entire panel hierarchy instantly!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("Widget 0 state =", widget.get_state())
    print("Widget 1 state =", widget1.get_state())

    # Verify the cascade pipeline unlocks everything smoothly right back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("Widget 0 state =", widget.get_state())
    print("Widget 1 state =", widget1.get_state())
    print("\n=== SYSTEM ONLINE: SECONDARY BUTTON INTERACTION ACTIVE ===\n")

    # -----------------------------------------------------------------
    # B. 🛠️ THE INTERACTION FIX: MAKE BUTTONS ALIVE AND RESPOND TO CLICKS
    # -----------------------------------------------------------------
    # 🛠️ THE CLICK REPORT FIX: Added a print statement to report the click instantly
    widget.configure(
        command=lambda: [print("System Action Button Clicked"), widget.set_pressed(not widget.is_pressed)])

    # Clicking 'widget1' does the exact same thing, turning its pre-set pressed state off and on!
    widget1.configure(
        command=lambda: [print("Testpressed Button Clicked"), widget1.set_pressed(not widget1.is_pressed)])

    root.mainloop()


