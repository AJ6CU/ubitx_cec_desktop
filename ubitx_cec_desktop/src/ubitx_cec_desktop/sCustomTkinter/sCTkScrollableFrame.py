#!/usr/bin/python3
"""
sCTkScrollableFrame

A clean, theme-compliant scrollable viewport container frame.
"""
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
from ThemeableWidget import ThemeableWidget


class sCTkScrollableFrame(ctk.CTkScrollableFrame, ThemeableWidget):
    properties = frozenset()

    def __init__(self, master=None, **kwargs):
        theme_defaults = THEME_DEFAULTS.get("sCTkScrollableFrame", {})
        ThemeableWidget.__init__(self, theme_defaults, kwargs)
        super().__init__(master, **self.final_kw)
