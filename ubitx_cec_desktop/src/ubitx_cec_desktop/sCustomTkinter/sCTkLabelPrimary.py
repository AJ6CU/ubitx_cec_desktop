#!/usr/bin/python3
"""
sCTkLabelPrimary

A custom, theme-compliant dominant header label widget.
Natively intercepts state assignments to swap active vs dimmed text colors.
"""
import customtkinter as ctk
from ThemeableWidget import ThemeableWidget


class sCTkLabelPrimary(ctk.CTkLabel, ThemeableWidget):
    _MANAGED_PROPERTIES = frozenset({"state"})

    def __init__(self, master=None, **kwargs):
        # 1. Trace and capture state parameters early out of input footprint
        self._current_state = str(kwargs.pop("state", "normal")).lower()
        if self._current_state not in ("normal", "disabled"):
            self._current_state = "normal"

        # 2. Fire our shared theme logic first. It automatically finds "sCTkLabelPrimary" in themes.json
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

        # Handle Pygubu positional dictionary merging layers cleanly
        if args and isinstance(args, dict):
            kwargs = args | kwargs

        # -----------------------------------------------------------------
        # ZONE B: MULTI-STATE PAYLOAD INTERCEPTION
        # -----------------------------------------------------------------
        if "state" in kwargs:
            self._current_state = str(kwargs.pop("state")).lower()

            if self._current_state == "disabled":
                target_color = self._custom_disabled_map.get("text_color") or "gray50"
                super().configure(text_color=target_color)
            else:
                # If the widget is active, let CustomTkinter's core engine
                # natively paint high-contrast white text for Dark Mode from the system.
                if self.final_kw.get("text_color"):
                    super().configure(text_color=self.final_kw.get("text_color"))
                else:
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
            # 🛠️ THE STATE FIXED RETURN:
            # Safely return the current state string variable directly from memory.
            return getattr(self, "_current_state", "normal")

        self.configure(state=mode)
        return None


# !/usr/bin/python3
import customtkinter as ctk

# !/usr/bin/python3
import customtkinter as ctk
from sCTkLabelPrimary import sCTkLabelPrimary


# =====================================================================
# RUNTIME EVENT UTILITIES
# =====================================================================
def toggle_label_states():
    """Cycles the dominant header label states between normal and disabled profiles."""
    current_state = primary_label.get_state()

    if current_state == "normal":
        # Apply the disabled dimming mapping rules
        primary_label.state("disabled")
        btn_toggle.configure(text="Activate Header (Set 'normal')")
        lbl_status.configure(text="Current State Assertion: DISABLED")
    else:
        # Revert back to the active high-visibility look
        primary_label.state("normal")
        btn_toggle.configure(text="Dim Header (Set 'disabled')")
        lbl_status.configure(text="Current State Assertion: NORMAL")

    # Log state updates to terminal for validation tracking
    print(f"Logged Verification Hook -> primary_label.get_state() = {primary_label.get_state()}")


# =====================================================================
# INTERACTIVE WINDOW ASSEMBLY RUNNER MAIN
# =====================================================================
if __name__ == "__main__":
    # Let the operating system handle the layout theme automatically.
    root = ctk.CTk()
    root.geometry("450x280")
    root.title("sCTkLabelPrimary Testing Deck")

    # Layout a clean, padded workspace container frame panel
    from sCTkFrame import sCTkFrame

    container = sCTkFrame(root, fg_color="transparent")
    container.pack(expand=True, fill="both", padx=30, pady=30)

    # Instantiate your custom primary header label widget
    primary_label = sCTkLabelPrimary(container, text="MAIN RADIO DECK CONSOLE")
    primary_label.pack(expand=True, pady=10)

    # Standard interaction trigger button to dispatch state transformations
    btn_toggle = ctk.CTkButton(
        container,
        text="Dim Header (Set 'disabled')",
        command=toggle_label_states,
        fg_color=("#1A4375", "#3B8ED0"),
        hover_color=("#112A4B", "#1F6AA5")
    )
    btn_toggle.pack(expand=True, pady=15)

    # Live state monitoring feedback label
    lbl_status = ctk.CTkLabel(container, text="Current State Assertion: NORMAL", font=("Arial", 10, "italic"))
    lbl_status.pack(side="bottom", pady=5)

    # Run the interactive boot tracking validation checks
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    print(f"Initial State Query = {primary_label.get_state().upper()}")
    print("========================================\n")

    root.mainloop()
