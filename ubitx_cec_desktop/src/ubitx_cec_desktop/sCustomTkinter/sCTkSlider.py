#!/usr/bin/python3
"""
sCTkSlider

derived from slider

UI source file: sCTkSlider.ui
"""
import customtkinter as ctk
import sCTkSliderui as baseui
from ThemeableWidget import ThemeableWidget


class sCTkSlider(baseui.sCTkSliderUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # 1. Fire our shared theme logic first. It automatically finds "sCTkSlider" in themes.json
        ThemeableWidget.__init__(self, kw)

        # 2. Store your custom maps safely onto instance memory channels
        self._local_defaults = self.final_kw
        self._custom_disabled_map = self._widget_disabled_map

        # 3. Initialize CustomTkinter natively with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

    def configure(self, *args, **kwargs):
        """Handles both standard keyword configurations and Pygubu inspector queries."""

        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Pygubu Inspector compatibility check)
        # -----------------------------------------------------------------
        if args and len(args) == 1:
            pname = args[0]

            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "progress_color", "button_color", "button_hover_color", "text_color"]:
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
            target_state = str(kwargs.pop("state")).lower()

            if target_state == "disabled" and self._custom_disabled_map:
                super().configure(state="disabled")

                # Apply disabled overrides from your map safely via super core channels
                for key in ("fg_color", "progress_color", "button_color"):
                    if key in self._custom_disabled_map:
                        try:
                            super().configure(**{key: self._custom_disabled_map[key]})
                        except Exception:
                            pass
                try:
                    super().configure(button_hover_color=self._custom_disabled_map.get("button_color"))
                except Exception:
                    pass

            elif target_state in ["normal", "active"]:
                super().configure(state="normal")
                self._update_current_visual_state()

        # -----------------------------------------------------------------
        # ZONE C: RUNTIME KEYWORDS MRO ROUTING PASS
        # -----------------------------------------------------------------
        if kwargs:
            return super().configure(**kwargs)
        return None

    def get_state(self):
        """Explicit getter synchronized with your standalone test harness script assertions."""
        return self.state()

    def state(self, state_string=None):
        """Standard Tkinter state management mapping."""
        if state_string is not None:
            self.configure(state=state_string)
        return str(super().cget("state")).lower()

    def _update_current_visual_state(self):
        """MASTER VISUAL ROUTER: Restores active theme dimensions out of local configuration dictionaries."""
        super().configure(
            fg_color=self.final_kw.get("fg_color", self._local_defaults.get("fg_color")),
            progress_color=self.final_kw.get("progress_color", self._local_defaults.get("progress_color")),
            button_color=self.final_kw.get("button_color", self._local_defaults.get("button_color")),
            button_hover_color=self.final_kw.get("button_hover_color", self._local_defaults.get("button_hover_color"))
        )


# =====================================================================
# 🛠️ UPDATED LIVE INTERACTIVE TEST HARNESS ASSEMBLY RUNNER MAIN
# =====================================================================
if __name__ == "__main__":
    # Ensure local theme profiles exist if running outside your active main window deck

    root = ctk.CTk()
    root.geometry("450x220")
    root.title("Slider Real-Time Telemetry Monitor")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    from sCTkLabelSecondary import sCTkLabelSecondary

    # 🔍 Live feedback layer to catch floating point data changes instantly
    lbl_telemetry = sCTkLabelSecondary(base, text="Slider Coordinate: 0.450", font=("Courier New", 12, "bold"))

    widget = sCTkSlider(base)

    # 🛠️ THE TELEMETRY FIX: Intercept value changes, print them to terminal,
    # and update the text label dynamically in real time
    widget.configure(
        command=lambda val: [
            lbl_telemetry.configure(text=f"Slider Coordinate: {val:.3f}")
        ]
    )

    widget.pack(expand=False, fill="x", padx=40, pady=15)
    widget.set(0.45)
    lbl_telemetry.pack(pady=10)

    # Verify our custom state loop handles double-pass transitions flawlessly on the console
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("state (Disabled Pass) =", widget.get_state())  # Output: disabled

    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("state (Normal Pass)   =", widget.get_state())  # Output: normal

    root.mainloop()
