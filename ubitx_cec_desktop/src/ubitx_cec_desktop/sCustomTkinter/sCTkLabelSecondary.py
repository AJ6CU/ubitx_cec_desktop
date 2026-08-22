#!/usr/bin/python3
"""
sCTkLabelSecondary

A custom, theme-compliant intermediate sub-section label widget.
Natively intercepts state assignments to swap active vs dimmed text colors.
"""
import customtkinter as ctk
from ThemeableWidget import ThemeableWidget


class sCTkLabelSecondary(ctk.CTkLabel, ThemeableWidget):
    _MANAGED_PROPERTIES = frozenset({"state"})

    def __init__(self, master=None, **kwargs):
        # 1. Trace and capture state parameters early out of input footprint
        self._current_state = str(kwargs.pop("state", "normal")).lower()
        if self._current_state not in ("normal", "disabled"):
            self._current_state = "normal"

        # 2. Fire our shared theme logic first. It automatically finds "sCTkLabelSecondary" in themes.json
        ThemeableWidget.__init__(self, kwargs)

        # 3. Store local style dictionary trackers onto instance memory channels
        self._local_defaults = self.final_kw
        self._custom_disabled_map = self._widget_disabled_map

        # 4. Initialize CustomTkinter natively with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

        # 5. Execute state evaluation pass immediately at the end of instantiation tracks
        self.state(self._current_state)

    def configure(self, *args, **kwargs):
        """Extended configure to handle Pygubu designer queries and state text dimming passes."""

        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Pygubu Inspector compatibility check)
        # -----------------------------------------------------------------
        if args and len(args) == 1:
            pname = args
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "text_color"]:
                val = self._custom_disabled_map.get(pname) if str(
                    self.state()).lower() == "disabled" else self._local_defaults.get(pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            return super().configure(pname)

        if args and isinstance(args, dict):
            kwargs = args | kwargs

        # -----------------------------------------------------------------
        # ZONE B: MULTI-STATE PAYLOAD INTERCEPTION
        # -----------------------------------------------------------------
        if "state" in kwargs:
            self._current_state = str(kwargs.pop("state")).lower()

            if self._current_state == "disabled":
                # Only apply an override color manually if the widget is explicitly disabled
                target_color = self._custom_disabled_map.get("text_color") or "gray50"
                super().configure(text_color=target_color)
            else:
                # 🛠️ THE SYSTEM MODE RESOLUTION FIX:
                # If the widget is returning to normal or active state, do NOT guess the color
                # or evaluate the OS mode inside the class code track! Simply check if themes.json
                # provided an explicit override tuple. If it didn't, pass CustomTkinter's native
                # dual-color tracking list string array down. This lets CustomTkinter's core
                # engine natively query your OS system setting and paint high-contrast crisp white!
                if self.final_kw.get("text_color"):
                    super().configure(text_color=self.final_kw.get("text_color"))
                else:
                    # Securely point the text_color tracker back to CustomTkinter's automatic theme defaults
                    super().configure(text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"])

        # -----------------------------------------------------------------
        # ZONE C: RUNTIME KEYWORDS MRO ROUTING PASS
        # -----------------------------------------------------------------
        if kwargs:
            return super().configure(**kwargs)
        return None

    config = configure

    def get_state(self):
        """Explicit getter synchronized with your standalone test harness script assertions."""
        return self.state()

    def state(self, mode: str = None):
        """Dedicated label state controller."""
        if mode is None:
            return getattr(self, "_current_state", "normal")

        # Route state string keywords directly through our multi-zone interceptor logic
        self.configure(state=mode)
        return None


# =====================================================================
# 3. INTERACTIVE WINDOW ASSEMBLY RUNNER MAIN
# =====================================================================
def toggle_label_states():
    """Cycles the label states between normal active and dimmed disabled profiles."""
    current_state = test_label.state()

    if current_state == "normal":
        # Lock down the label and switch to custom disabled map text colors
        test_label.state("disabled")
        btn_toggle.configure(text="Activate Label (Set 'normal')")
        lbl_status.configure(text="Current State Assertion: DISABLED")
    else:
        # Unlock the label and snap text color back onto default active layouts
        test_label.state("normal")
        btn_toggle.configure(text="Dim Label (Set 'disabled')")
        lbl_status.configure(text="Current State Assertion: NORMAL")

    # Log state queries to terminal to match your standalone harness requirements
    print(f"Logged Verification Hook -> test_label.get_state() = {test_label.get_state()}")
if __name__ == "__main__":
    # ctk.set_appearance_mode("Dark")  # Swap to "Light" to check alternative mode palettes

    root = ctk.CTk()
    root.geometry("450x280")
    root.title("sCTkLabelSecondary Testing Deck")

    # Layout a clean, padded workspace container
    container = ctk.CTkFrame(root, fg_color="transparent")
    container.pack(expand=True, fill="both", padx=30, pady=30)

    # Instantiate your custom secondary label targeting your name registry
    test_label = sCTkLabelSecondary(container, text="VFO STATUS PANEL: ACTIVE")
    test_label.pack(expand=True, pady=10)

    # Standard interaction trigger button to dispatch state transformations
    btn_toggle = ctk.CTkButton(
        container,
        text="Dim Label (Set 'disabled')",
        command=toggle_label_states,
        fg_color=("#2471A3", "#3B8ED0"),
        hover_color=("#112A4B", "#1F6AA5")
    )
    btn_toggle.pack(expand=True, pady=15)

    # Live state monitoring feedback label
    lbl_status = ctk.CTkLabel(container, text="Current State Assertion: NORMAL", font=("Arial", 10, "italic"))
    lbl_status.pack(side="bottom", pady=5)

    # Run the interactive boot tracking validation checks
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    print(f"Initial State Query = {test_label.get_state().upper()}")
    print("========================================\n")

    root.mainloop()