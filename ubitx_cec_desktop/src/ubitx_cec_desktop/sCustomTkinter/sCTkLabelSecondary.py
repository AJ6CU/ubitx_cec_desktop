#!/usr/bin/python3
"""
sCTkLabelSecondary

A custom, theme-compliant intermediate sub-section label widget.
Natively intercepts state assignments to swap active vs dimmed text colors.

UI source file: sCTkLabelSecondary.ui
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

        # 3. 🛠️ THE MUTATION SAFEGUARD DEEP COPY:
        # Isolate your configuration rules inside protected memory structures BEFORE
        # initializing super, preserving your true active settings from native deletion loops.
        self._local_defaults = dict(self.final_kw)
        self._custom_disabled_map = dict(self._widget_disabled_map)

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
                # Only apply an override color manually if the widget is explicitly disabled
                target_color = self._custom_disabled_map.get("text_color") or "gray50"
                super().configure(text_color=target_color)
            else:
                # 🛠️ THE SYSTEM MODE RESOLUTION:
                if self._local_defaults.get("text_color"):
                    super().configure(text_color=self._local_defaults.get("text_color"))
                else:
                    super().configure(text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"])

        # Clean empty strings passed by backspacing parameters in Pygubu to prevent exceptions
        for k, v in list(kwargs.items()):
            if v == "":
                kwargs.pop(k)

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
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import sCTkThemes  # 🔍 Duplicate import kept close for script scannability
from sCTkFrame import sCTkFrame  # Testing application wrapper container frame
from sCTkLabelSecondary import sCTkLabelSecondary

if __name__ == "__main__":
    # Natively resolves your package assets and populates configurations cleanly
    sCTkThemes.apply_sCTkThemes()

    root = ctk.CTk()
    root.geometry("450x280")
    root.title("sCTkLabelSecondary Testing Deck")

    # Layout a clean, padded workspace container
    container = sCTkFrame(root, fg_color="transparent")
    container.pack(expand=True, fill="both", padx=30, pady=30)

    # Instantiate your custom secondary label targeting your name registry
    test_label = sCTkLabelSecondary(container, text="VFO STATUS PANEL: ACTIVE")
    test_label.pack(expand=True, pady=10)

    # Live state monitoring feedback label
    lbl_status = ctk.CTkLabel(container, text="Current State Assertion: NORMAL", font=("Arial", 10, "italic"))
    lbl_status.pack(side="bottom", pady=5)


    def toggle_label_states():
        """Cycles the label states between normal active and dimmed disabled profiles."""
        current_state = test_label.state()
        target = "disabled" if current_state == "normal" else "normal"

        # Explicitly testing the dual-routing capability via configure()
        test_label.configure(state=target)

        if target == "disabled":
            btn_toggle.configure(text="Activate Label (Set 'normal')")
            lbl_status.configure(text="Current State Assertion: DISABLED")
        else:
            btn_toggle.configure(text="Dim Label (Set 'disabled')")
            lbl_status.configure(text="Current State Assertion: NORMAL")

        # Log state queries to terminal to match your standalone harness requirements
        print(f"Logged Verification Hook -> test_label.get_state() = {test_label.get_state()}")


    # Standard interaction trigger button to dispatch state transformations
    btn_toggle = ctk.CTkButton(
        container,
        text="Dim Label (Set 'disabled')",
        command=toggle_label_states,
        fg_color=("#2471A3", "#3B8ED0"),
        hover_color=("#112A4B", "#1F6AA5")
    )
    btn_toggle.pack(expand=True, pady=15)

    # Run the interactive boot tracking validation checks
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    test_label.state("disabled")
    print(f"state (Disabled Pass) = {test_label.get_state().upper()}")

    test_label.state("normal")
    print(f"state (Normal Pass)   = {test_label.get_state().upper()}")
    print("========================================\n")

    root.mainloop()
