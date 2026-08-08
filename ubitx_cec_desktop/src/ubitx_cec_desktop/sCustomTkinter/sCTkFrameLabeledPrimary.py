#!/usr/bin/python3
"""
sCTkFrameLabeledPrimary

A clean CustomTkinter ScrollableFrame that natively hides its scrollbars
by matching their color profile to the frame background.
"""
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
from ThemeableWidget import ThemeableWidget


class sCTkFrameLabeledPrimary(ctk.CTkScrollableFrame, ThemeableWidget):
    properties = frozenset()

    def __init__(self, master=None, **kwargs):
        theme_defaults = THEME_DEFAULTS.get("sCTkFrameLabeledPrimary", {})
        ThemeableWidget.__init__(self, theme_defaults, kwargs)
        super().__init__(master, **self.final_kw)

        bg_color = self.cget("fg_color")
        if hasattr(self, "_scrollbar"):
            self._scrollbar.configure(
                fg_color=bg_color,
                button_color=bg_color,
                button_hover_color=bg_color,
                width=0
            )

    def get_container(self):
        return self
