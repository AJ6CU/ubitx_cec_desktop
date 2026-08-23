#!/usr/bin/python3
"""
sCTkScrollbar - Piece 1 of 3

An advanced, theme-compliant custom scrollbar component.
Inherits cleanly from ctk.CTkScrollbar to preserve native macOS high-precision
touchpad event streams and keep global light/dark theme tracking active.
"""
import os
import sys
import platform
import tkinter as tk
import customtkinter as ctk
from ThemeableWidget import ThemeableWidget

class sCTkScrollbar(ctk.CTkScrollbar, ThemeableWidget):
    def __init__(self, master=None, **kwargs):
        # 1. INITIAL RUNTIME SCRUB: Safely shield native frame from state validation checks
        state_init = kwargs.pop("state", "normal")
        orientation = kwargs.get("orientation", "vertical").lower()
        self._is_horizontal = orientation == "horizontal"

        # 2. ENFORCE SYSTEM REGISTRY INTERACTION:
        ThemeableWidget.__init__(self, kwargs)

        # 3. THE MUTATION SAFEGUARD DEEP COPY SHIELD & SIZING MATRIX:
        self._local_defaults = dict(self.final_kw)
        self._custom_disabled_map = dict(self._widget_disabled_map)

        if self._is_horizontal:
            self.final_kw.setdefault("height", 14)
        else:
            self.final_kw.setdefault("width", 14)

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

            if pname in ["fg_color", "button_color", "button_hover_color"]:
                current_state = str(self.state()).lower()
                val = self._custom_disabled_map.get(pname) if current_state == "disabled" else self._local_defaults.get(pname)
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
        """Dedicated polymorphic state manager syncing drag mechanics."""
        if mode is None:
            return str(getattr(self, "_state_str", "normal")).lower()

        target_state = mode.lower()
        self._state_str = target_state

        if target_state in ["normal", "active", "enabled"]:
            super().configure(
                button_color=self._resolve_color(self._local_defaults.get("button_color")),
                button_hover_color=self._resolve_color(self._local_defaults.get("button_hover_color"))
            )
        elif target_state == "disabled":
            disabled_color = self._resolve_color(self._custom_disabled_map.get("button_color", ("#E5E7EB", "#1F2937")))
            super().configure(button_color=disabled_color, button_hover_color=disabled_color)

        return self._state_str


# =====================================================================
# 🛠️ NATIVE HIGH-LOAD MULTI-ROW TEST HARNESS (RESET BASELINE)
# =====================================================================
if __name__ == "__main__":
    import sCTkThemes
    from sCTkFrame import sCTkFrame
    from sCTkButtonPrimary import sCTkButtonPrimary
    from sCTkLabelSecondary import sCTkLabelSecondary

    root = ctk.CTk()
    root.geometry("480x450")
    root.title("sCTkScrollbar Full Multi-Row Deck")

    sCTkThemes.apply_sCTkThemes()

    # 1. Main visual layout shell container panel
    main_layout = sCTkFrame(root)
    main_layout.pack(expand=True, fill="both", padx=15, pady=15)

    # Live Operational Telemetry Status Monitoring Bar
    status_monitor = sCTkLabelSecondary(
        main_layout,
        text="SYSTEM STATUS CORE TRACK LANE: [ACTIVE / NORMAL]"
    )
    status_monitor.pack(fill="x", padx=10, pady=(5, 5))


    # TOP-DECK INTERACTIVE MANAGEMENT MATRIX
    def toggle_operational_lock():
        global _view_locked

        if not _view_locked:
            target = "disabled"
            _view_locked = True
            btn_lock.configure(text="Enable Telemetry View")
            status_monitor.configure(text="SYSTEM STATUS CORE TRACK LANE: [LOCKED / DISABLED]")
        else:
            target = "normal"
            _view_locked = False
            btn_lock.configure(text="Disable Telemetry View")
            status_monitor.configure(text="SYSTEM STATUS CORE TRACK LANE: [ACTIVE / NORMAL]")

        scrollbar.configure(state=target)

        # 🔑 FIX: Removed scroll_view.configure(state=target) to prevent CustomTkinter
        # validation errors. Passive structural containers do not accept state arguments!

        # Cascade configuration maps safely ONLY to content text label elements
        for label_widget in scroll_content.winfo_children():
            if hasattr(label_widget, "state") and "Label" in label_widget.__class__.__name__:
                label_widget.state(target)


    def toggle_appearance_skin():
        current_mode = ctk.get_appearance_mode()
        target = "Light" if current_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(target)


    _view_locked = False

    btn_lock = sCTkButtonPrimary(main_layout, text="Disable Telemetry View", command=toggle_operational_lock)
    btn_lock.pack(fill="x", padx=10, pady=(2, 5))

    btn_theme = sCTkButtonPrimary(main_layout, text="Toggle Theme Skin (Dark / Light)", command=toggle_appearance_skin)
    btn_theme.pack(fill="x", padx=10, pady=(0, 10))

    # Initialize the custom external scrollbar on the right channel lane first
    scrollbar = sCTkScrollbar(main_layout, orientation="vertical")
    scrollbar.pack(side="right", fill="y", padx=(5, 10), pady=10)

    # Standard layout background container frame card panel (Our clean backplane)
    content_chassis = sCTkFrame(main_layout)
    content_chassis.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

    # We use CustomTkinter's native public CTkScrollableFrame container
    scroll_view = ctk.CTkScrollableFrame(content_chassis, fg_color="transparent")
    scroll_view.pack(fill="both", expand=True)

    # Unpack the underlying frame window out of CustomTkinter safely
    scroll_content = scroll_view._parent_frame

    # Populate with theme-aware secondary text label rows using native compliant grid parameters
    for i in range(25):
        lbl_item = sCTkLabelSecondary(scroll_content,
                                      text=f"▶ Transceiver Core Channel Lane Code: {100 + i} [STATUS: OK]")
        lbl_item.grid(row=i, column=0, sticky="w", padx=10, pady=4)

    root.mainloop()

