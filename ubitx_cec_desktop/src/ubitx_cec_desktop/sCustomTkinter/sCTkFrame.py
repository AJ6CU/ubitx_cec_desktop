#!/usr/bin/python3
"""
sCTkFrame

A clean, theme-compliant standard CustomTkinter container frame.
"""
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
from ThemeableWidget import ThemeableWidget


class sCTkFrame(ctk.CTkFrame, ThemeableWidget):
    properties = frozenset()

    def __init__(self, master=None, **kwargs):
        theme_defaults = THEME_DEFAULTS.get("sCTkFrame", {})
        ThemeableWidget.__init__(self, theme_defaults, kwargs)
        super().__init__(master, **self.final_kw)
