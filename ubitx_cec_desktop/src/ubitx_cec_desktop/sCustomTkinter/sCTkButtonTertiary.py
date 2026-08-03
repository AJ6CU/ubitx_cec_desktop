#!/usr/bin/python3
"""
sCTkButtonTertiary

ghost ctk button

UI source file: sCTkButtonTertiary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import platform

import customtkinter as ctk
import sCTkButtonTertiaryui as baseui


#
# Manual user code
#
# Detect platform
IS_MAC = platform.system() == "Darwin"

class sCTkButtonTertiary(baseui.sCTkButtonTertiaryUI):
    def __init__(self, master=None, **kw):
        #
        #   Figure out defaults for this widget
        #

        accent_colors = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        # High-contrast settings tailored specifically for macOS rendering
        if IS_MAC:
            theme_defaults = {
                "fg_color": "transparent",
                "border_width": 1.5,
                "border_color": ("#CBD5E1", "#475569"),
                "hover_color": ("#E2E8F0", "#334155"),
                "text_color": accent_colors,  # Keep text vibrant
                "text_color_disabled": ("#94A3B8", "#64748B")
            }
        else:
            # Standby default rules for Windows/Linux
            theme_defaults = {
                "fg_color": "transparent",
                "border_width": 1,
                "border_color": ("#D1D5DB", "#374151"),
                "hover_color": ("#F3F4F6", "#1F2937"),
                "text_color": accent_colors
            }

        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkButtonTertiary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
