#!/usr/bin/python3
"""
sCTkProgressBar

Derived from progressBar
Natively fortified with polymorphic state controllers and direct visual trackers.

UI source file: sCTkProgressBar.ui
"""
import os
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkProgressBarui as baseui
from ThemeableWidget import ThemeableWidget


class sCTkProgressBar(baseui.sCTkProgressBarUI, ThemeableWidget):
    def __init__(self, master=None, **kwargs):
        # 1. INITIAL RUNTIME SCRUB: Safely shield native frame from state validation checks
        state_init = kwargs.pop("state", "normal")

        # 2. ENFORCE SYSTEM REGISTRY INTERACTION:
        # Pass kwargs cleanly to the theme mixin to engage the name-introspection pipeline natively.
        ThemeableWidget.__init__(self, kwargs)

        # 3. 🛠️ THE MUTATION SAFEGUARD DEEP COPY SHIELD:
        self._local_defaults = dict(self.final_kw)
        self._custom_disabled_map = dict(self._widget_disabled_map)

        # Remove custom parameters from final_kw to prevent parent collisions
        self.final_kw.pop("state", None)

        # 4. Initialize CustomTkinter natively with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

        # 5. ROUTE TO CONFIG: Safely pass parameters through your validation engine
        self._state_str = "normal"
        self.configure(state=state_init)

    def configure(self, *args, **kwargs):
        """Processes Pygubu designer queries and manages state changes safely."""
        if args and len(args) == 1:
            pname = args if isinstance(args, (list, tuple)) else args
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "progress_color", "border_color"]:
                current_state = str(self.state()).lower()
                val = self._custom_disabled_map.get(pname) if current_state == "disabled" else self._local_defaults.get(
                    pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            return super().configure(*args, **kwargs)

        if args and isinstance(args, dict):
            kwargs = args | kwargs

        if "state" in kwargs:
            self.state(kwargs.pop("state"))

        if kwargs:
            super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        """Safely intercept custom properties like 'state' from throwing errors."""
        if str(attribute_name).lower() == "state":
            return self.state()
        return super().cget(attribute_name)

    def get_state(self) -> str:
        """Explicit getter synchronized with your standalone test harness script assertions."""
        return self.state()

    def state(self, mode: str = None) -> str:
        """Dedicated polymorphic state manager forcing internal indicator lane repaints."""
        if mode is None:
            return str(getattr(self, "_state_str", "normal")).lower()

        target_state = mode.lower()
        self._state_str = target_state

        if target_state == "disabled":
            # Extract the raw desaturated hex tokens out of your theme mapping data
            disabled_fg = self._custom_disabled_map.get("fg_color", ("#E2E8F0", "#1E293B"))
            disabled_progress = self._custom_disabled_map.get("progress_color", ("#94A3B8", "#475569"))

            # Inject the gray colors up to the CustomTkinter base class layers natively
            super().configure(
                fg_color=self._resolve_color(disabled_fg),
                progress_color=self._resolve_color(disabled_progress)
            )

        elif target_state in ["normal", "active", "enabled"]:
            # Revert straight back to the clean active operational theme configurations
            active_fg = self._local_defaults.get("fg_color", ("#E2E8F0", "#2D2D2D"))
            active_progress = self._local_defaults.get("progress_color", ("#3B82F6", "#1F6AA5"))

            super().configure(
                fg_color=self._resolve_color(active_fg),
                progress_color=self._resolve_color(active_progress)
            )

        return self._state_str

    def bind(self, sequence=None, command=None, add=None):
        if "PYGUBU_DESIGNER_RUNNING" in os.environ:
            return None
        return super().bind(sequence, command, add)


# =====================================================================
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
if __name__ == "__main__":
    import sCTkThemes
    from sCTkFrame import sCTkFrame
    from sCTkButtonPrimary import sCTkButtonPrimary
    from sCTkLabelSecondary import sCTkLabelSecondary

    root = ctk.CTk()
    root.geometry("450x260")
    root.title("sCTkProgressBar Interactive Testing Deck")

    sCTkThemes.apply_sCTkThemes()

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # 1. Percentage Progress Monitoring Display Label Notice
    initial_val = 0.45
    lbl_status = sCTkLabelSecondary(
        base,
        text=f"Telemetry Progress Output: {int(initial_val * 100)}% / 100%"
    )
    lbl_status.pack(pady=(10, 5))

    # 2. Instantiate your custom themed progression indicator bar layout
    widget = sCTkProgressBar(base)
    widget.pack(expand=False, fill="x", padx=40, pady=10)
    widget.set(initial_val)


    # 3. Dynamic Progress Modifier Event Handler Callback
    def step_progress():
        if widget.get_state() == "disabled":
            print("⚠️ Cannot modify progress channel: Widget is currently locked!")
            return

        current_val = widget.get()
        # Increment by an operational 5% step delta slice
        next_val = current_val + 0.05

        # Safe threshold ceiling clamp condition
        if next_val > 1.0:
            next_val = 0.0  # Cycle back to zero when reaching full scale

        widget.set(next_val)
        lbl_status.configure(text=f"Telemetry Progress Output: {int(next_val * 100)}% / 100%")


    # 4. Interactive Simulation Control Button Triggers
    btn_step = sCTkButtonPrimary(base, text="Step Telemetry Track (+5%)", command=step_progress)
    btn_step.pack(pady=(5, 5))


    def toggle_operational_lock():
        current_mode = widget.get_state()
        target = "disabled" if current_mode == "normal" else "normal"
        widget.configure(state=target)
        btn_lock.configure(text="Lock Indicator Track" if target == "normal" else "Unlock Indicator Track")
        btn_step.configure(state=target)  # Keep action triggers tightly bound to structural locks


    btn_lock = ctk.CTkButton(base, text="Lock Indicator Track", command=toggle_operational_lock)
    btn_lock.pack(side="bottom", pady=(5, 10))

    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    widget.state("disabled")
    print("state (Disabled Pass) =", widget.get_state())  # Output: disabled
    widget.state("normal")
    print("state (Normal Pass)   =", widget.get_state())  # Output: normal
    print("========================================\n")

    root.mainloop()
