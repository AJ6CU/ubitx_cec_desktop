#!/usr/bin/python3
"""
sCTkButtonTertiary

subclass of CTkButton (Universal Platform Border-Driven Outline Latching Toggle Variant)

UI source file: sCTkButtonTertiary.ui
"""
import customtkinter as ctk
import sCTkButtonTertiaryui as baseui
from ThemeableWidget import ThemeableWidget


class sCTkButtonTertiary(baseui.sCTkButtonTertiaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # 1. Run the shared theme logic to load defaults out of themes.json
        ThemeableWidget.__init__(self, kw)

        # 2. 🛠️ THE SYSTEM ACCENT FALLBACK INTERCEPT:
        # Resolves your text_color mapping note. If sCTkThemes.json does not explicitly
        # provide a text color, we dynamically fetch CustomTkinter's live default button
        # accent colors instead of using rigid local file scripts.
        if "text_color" not in self.final_kw or self.final_kw["text_color"] is None:
            try:
                live_fg_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
                self.final_kw["text_color"] = tuple(live_fg_color)
            except Exception:
                self.final_kw["text_color"] = ("#3B8ED0", "#1F6AA5")

        # 3. 🛠️ THE MUTATION SAFEGUARD DEEP COPY:
        # Clone your configuration parameters into completely independent memory structures
        # BEFORE initializing super, protecting active color values from native corruption traps.
        self._local_defaults = dict(self.final_kw)
        self._custom_disabled_map = dict(self._widget_disabled_map)
        self._custom_pressed_map = dict(self._widget_pressed_map)

        # 4. Initialize CustomTkinter natively with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

        self.is_pressed = False
        self._custom_current_state = "normal"

    def configure(self, *args, **kwargs):
        """Handles Pygubu designer queries and manages state updates safely."""

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

    def _update_current_visual_state(self):
        """
        MASTER VISUAL ROUTER: Dynamically maps configuration layouts out of protected memory.
        """
        # A. PRESSED STATE TAKES PRIMARY LOCAL PRIORITY
        if getattr(self, "is_pressed", False):
            config_payload = {}
            for key in ("fg_color", "border_color", "hover_color", "text_color"):
                val = self._custom_pressed_map.get(key)
                if val is not None:
                    config_payload[key] = val

            config_payload.setdefault("hover_color", self._local_defaults.get("hover_color"))
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

    def set_pressed(self, pressed: bool):
        """Toggles the visual pressed state of the tertiary button cleanly."""
        if getattr(self, "_custom_current_state", "normal") == "disabled":
            return

        self.is_pressed = pressed
        self._update_current_visual_state()


# =====================================================================
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import sCTkThemes  # 🔍 Duplicate import kept close for script scannability
from sCTkFrame import sCTkFrame  # Testing application wrapper container frame
from sCTkButtonTertiary import sCTkButtonTertiary

if __name__ == "__main__":
    sCTkThemes.apply_sCTkThemes()

    root = ctk.CTk()
    root.geometry("450x300")
    root.title("Tertiary Outline Button Bench")

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget1 = sCTkButtonTertiary(base)
    widget = sCTkButtonTertiary(base)

    widget1.configure(
        text="Latching Preset Toggle",
        command=lambda: [
            widget1.set_pressed(not widget1.is_pressed),
            print(f"Logged Verification Hook -> widget1.is_pressed = {widget1.is_pressed}")
        ]
    )

    widget.configure(
        text="System Action",
        command=lambda: print("System Action Clicked")
    )

    widget.pack(expand=False, fill="none", padx=40, pady=10)
    widget1.pack(expand=False, fill="none", padx=40, pady=10)

    # Standard test assertions routine verification sequences
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    widget.state("disabled")
    print("widget (Disabled Pass) =", widget.get_state())

    widget.state("normal")
    print("widget (Normal Pass)   =", widget.get_state())
    print("========================================\n")

    root.mainloop()
