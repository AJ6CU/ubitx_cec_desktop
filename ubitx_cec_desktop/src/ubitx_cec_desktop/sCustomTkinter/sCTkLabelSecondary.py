#!/usr/bin/python3
"""
sCTkLabelSecondary

A custom, theme-compliant intermediate sub-section label widget.
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


class sCTkLabelSecondary(ctk.CTkLabel, ThemeableWidget):
    _MANAGED_PROPERTIES = frozenset({"state"})

    def __init__(self, master=None, **kwargs):
        self._current_state = str(kwargs.pop("state", "normal")).lower()
        if self._current_state not in ("normal", "disabled"):
            self._current_state = "normal"

        theme_defaults = THEME_DEFAULTS.get("sCTkLabelSecondary", {})
        if not theme_defaults:
            theme_defaults = THEME_DEFAULTS.get("sCTkLabelPrimary", {})

        ThemeableWidget.__init__(self, theme_defaults, kwargs)
        super().__init__(master, **self.final_kw)
        # FIXED: Removed the redundant duplicate self._current_state configuration line

        # Ensure ThemeableWidget's interceptor runs immediately at the end of creation
        self.configure(state=kwargs.get("state", getattr(self, "_current_state", "normal")))

    def configure(self, cnf=None, **kw):
        """Extended configure to handle state text dimming passes."""
        if cnf is not None:
            kw = cnf | kw

        if "state" in kw:
            self._current_state = str(kw.pop("state")).lower()
            theme = self.final_kw

            if self._current_state == "disabled":
                d_map = getattr(self, "_widget_disabled_map", theme.get("disabled_map", {}))
                target_color = d_map.get("text_color") or d_map.get("row_text_color") or "gray50"
                super().configure(text_color=target_color)
            else:
                target_color = theme.get("text_color") or self._apply_appearance_mode(
                    ctk.ThemeManager.theme["CTkLabel"]["text_color"])
                super().configure(text_color=target_color)

        if kw:
            return super().configure(**kw)

    config = configure
