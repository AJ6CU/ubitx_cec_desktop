#!/usr/bin/python3
"""
sCTkLabelPrimary

A custom, theme-compliant dominant header label widget.
Natively intercepts state assignments to swap active vs dimmed text colors.
"""
import os
import sys
import customtkinter as ctk

_local_dir = os.path.dirname(os.path.abspath(__file__))
if _local_dir not in sys.path:
    sys.path.insert(0, _local_dir)

from sCTkThemes import THEME_DEFAULTS
from ThemeableWidget import ThemeableWidget


class sCTkLabelPrimary(ctk.CTkLabel, ThemeableWidget):
    _MANAGED_PROPERTIES = frozenset({"state"})

    def __init__(self, master=None, **kwargs):
        # Extract initial state seed ahead of baseline constructor passes
        self._current_state = str(kwargs.pop("state", "normal")).lower()
        if self._current_state not in ("normal", "disabled"):
            self._current_state = "normal"

        theme_defaults = THEME_DEFAULTS.get("sCTkLabelPrimary", {})
        ThemeableWidget.__init__(self, theme_defaults, kwargs)

        super().__init__(master, **self.final_kw)

        # Apply initial visual color styles
        self.configure(state=self._current_state)

    def configure(self, cnf=None, **kw):
        """Extended configure to handle state text dimming passes."""
        if cnf is not None:
            kw = cnf | kw

        if "state" in kw:
            self._current_state = str(kw.pop("state")).lower()
            theme = self.final_kw

            if self._current_state == "disabled":
                d_map = getattr(self, "_widget_disabled_map", theme.get("disabled_map", {}))
                # Fall back to gray50 if the text_color field is entirely missing from themes
                target_color = d_map.get("text_color") or d_map.get("row_text_color") or "gray50"
                super().configure(text_color=target_color)
            else:
                target_color = theme.get("text_color") or self._apply_appearance_mode(
                    ctk.ThemeManager.theme["CTkLabel"]["text_color"])
                super().configure(text_color=target_color)

        if kw:
            return super().configure(**kw)

    config = configure
