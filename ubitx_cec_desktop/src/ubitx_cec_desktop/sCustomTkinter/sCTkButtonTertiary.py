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
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#
# !/usr/bin/python3
"""
sCTkButtonTertiary

subclass of CTkButton (Universal Platform Border-Driven Outline Variant)
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkButtonTertiaryui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkButtonTertiary(baseui.sCTkButtonTertiaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # 🎨 Pull dynamic accent themes straight from CustomTkinter's active skin manager
        accent_colors = ctk.ThemeManager.theme["CTkButton"]["fg_color"]

        # 📐 Universal Flat Theme Defaults (Looks spectacular across all operating systems!)
        # 📐 Universal Flat Theme Defaults (Looks spectacular across all operating systems!)
        # 📐 Universal Flat Theme Defaults (Looks spectacular across all operating systems!)
        theme_defaults = {
            "font": ("Arial", 15, "normal"),
            "fg_color": "transparent",
            "text_color": accent_colors,
            "corner_radius": 6,

            # 🔄 FIX: Darkened for Light Mode, brightened for Dark Mode to ensure high-contrast boundaries!
            "border_width": 1.25,
            "border_color": ("#64748B", "#94A3B8"),  # Light Mode: Solid Slate Gray | Dark Mode: Bright Light Slate
            "hover_color": ("#E2E8F0", "#1E293B"),  # Synchronized hover panel tints

            "disabled_map": {
                "border_color": ("#E5E7EB", "#374151"),
                "text_color": ("#94A3B8", "#64748B")
            },

            # Tactile Pressed Mapping (Matches your signature cobalt desaturated blue palette)
            "pressed_map": {
                "fg_color": ("#E2E8F0", "#1E293B"),
                "border_color": ("#112A4B", "#1F618D"),
                "text_color": ("#112A4B", "#1F618D")
            }
        }

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})
        self._custom_pressed_map = theme_defaults.get("pressed_map", {})

        # Run our shared theme logic to sanitize and merge dictionaries via pipe operator
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

        self.is_pressed = False

    def state(self, mode: str):
        """Dedicated button state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            try:
                self._canvas.bind("<Enter>", self._on_enter)
                self._canvas.bind("<Leave>", self._on_leave)
                self._canvas.bind("<Button-1>", self._on_clicked)
                self._canvas.bind("<ButtonRelease-1>", self._on_clicked)
            except Exception:
                pass

            self.configure(state="normal", hover=True)
            self._update_current_visual_state()
            self._custom_current_state = "normal"

        elif mode == "disabled":
            try:
                self._canvas.unbind("<Enter>")
                self._canvas.unbind("<Leave>")
                self._canvas.unbind("<Button-1>")
                self._canvas.unbind("<ButtonRelease-1>")
            except Exception:
                pass

            self.configure(state="disabled", hover=False)

            # Apply disabled overrides from your map
            for key in ("fg_color", "border_color", "hover_color", "text_color"):
                if key in self._custom_disabled_map:
                    try:
                        self.configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"

    def set_pressed(self, pressed: bool):
        """Toggles the visual pressed state of the tertiary button cleanly."""
        if getattr(self, "_custom_current_state", "normal") == "disabled":
            return

        self.is_pressed = pressed
        self._update_current_visual_state()

    def _update_current_visual_state(self):
        """
        MASTER VISUAL ROUTER: Dynamically maps configuration layouts out of memory.
        """
        if self.is_pressed:
            self.configure(
                fg_color=self._custom_pressed_map.get("fg_color"),
                border_color=self._custom_pressed_map.get("border_color"),
                hover_color=self._custom_pressed_map.get("hover_color", self._local_defaults.get("hover_color")),
                text_color=self._custom_pressed_map.get("text_color"),
                hover=False
            )
        else:
            self.configure(
                fg_color=self.final_kw.get("fg_color", self._local_defaults.get("fg_color")),
                border_color=self.final_kw.get("border_color", self._local_defaults.get("border_color")),
                hover_color=self.final_kw.get("hover_color", self._local_defaults.get("hover_color")),
                text_color=self.final_kw.get("text_color", self._local_defaults.get("text_color")),
                hover=True
            )


if __name__ == "__main__":
    # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x200")

    widget = sCTkButtonTertiary(root, text="Tertiary Action Option")
    widget1 = sCTkButtonTertiary(root, text="testpressed")
    widget1.configure(text="testpressed")

    widget.pack(expand=True, fill="none", padx=40, pady=40)
    widget1.pack(expand=True, fill="none", padx=40, pady=40)

    # Verify tracking sequences on your layout shell console
    widget.state("disabled")
    print("state =", widget.get_state())  # Output: disabled

    widget.state("normal")
    print("state =", widget.get_state())  # Output: normal

    widget1.set_pressed(True)
    print("state =", widget.get_state())

    root.mainloop()

