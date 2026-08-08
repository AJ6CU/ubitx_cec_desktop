#!/usr/bin/python3
"""
sCTkFrameOutlined

A clean, theme-compliant outlined CustomTkinter container frame.
Acts as a passive layout group following native Tkinter patterns.
"""
import os
import sys
import customtkinter as ctk

_local_dir = os.path.dirname(os.path.abspath(__file__))
if _local_dir not in sys.path:
    sys.path.insert(0, _local_dir)

from sCTkThemes import THEME_DEFAULTS
from ThemeableWidget import ThemeableWidget


class sCTkFrameOutlined(ctk.CTkFrame, ThemeableWidget):
    properties = frozenset()

    def __init__(self, master=None, **kwargs):
        theme_defaults = THEME_DEFAULTS.get("sCTkFrameOutlined", {})
        if not theme_defaults:
            theme_defaults = THEME_DEFAULTS.get("sCTkFrame", {})

        ThemeableWidget.__init__(self, theme_defaults, kwargs)
        super().__init__(master, **self.final_kw)


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Passive Outline Frame Test Suite")
    app.geometry("400x200")

    frame_group = sCTkFrameOutlined(app, border_width=2)
    frame_group.pack(fill="both", expand=True, padx=20, pady=20)

    mock_entry = ctk.CTkEntry(frame_group, placeholder_text="Standard data field...")
    mock_entry.pack(pady=10, padx=10, fill="x")

    app.mainloop()
