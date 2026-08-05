#!/usr/bin/python3
"""
sCTkButtonPrimary

subclass of CTkButton

UI source file: sCTkButtonPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkButtonPrimaryui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkButtonPrimary(baseui.sCTkButtonPrimaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            # 📐 Physical Geometry (Passed to lock layout boundaries natively)
            "width": 140,  # Standard compact horizontal width profile
            "height": 34,  # FIX: Natively sets a clean, balanced button height

            "font": ("Arial", 15, "normal"),
            "fg_color": ("#1A4375", "#2471A3"),
            "hover_color": ("#112A4B", "#1F618D"),
            "text_color": ("#FFFFFF", "#FFFFFF"),
            "corner_radius": 6,

            "disabled_map": {
                "fg_color": ("#E5E7EB", "#374151"),
                "hover_color": ("#E5E7EB", "#374151"),
                "text_color": ("#94A3B8", "#64748B")
            },

            # ⛔ FIX: Higher-contrast Blue-Slate pressed state for maximum background separation
            "pressed_map": {
                # Light Mode: Balanced deep slate blue (#3B5984) - clean contrast against white background
                # Dark Mode: Lighter Cobalt-Slate blue (#2E4A75) - pops sharply forward from #111827 background
                "fg_color": ("#3B5984", "#2E4A75"),
                "hover_color": ("#3B5984", "#2E4A75"),

                # High-contrast font pairing to keep text perfectly legible
                "text_color": ("#FFFFFF", "#FFFFFF")
            },

            "alarm_map": {
                "fg_color": ("#990000", "#E74C3C"),
                "hover_color": ("#990000", "#E74C3C"),
                "text_color": ("#FFFFFF", "#FFFFFF")
            }
        }

        # Store a reference to theme_defaults on the object instance
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})
        self._custom_pressed_map = theme_defaults.get("pressed_map", {})
        self._custom_alarm_map = theme_defaults.get("alarm_map", {})

        # Run our shared theme logic first to sanitize parameters
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array
        super().__init__(master, **self.final_kw)

        self.is_pressed = False
        self.is_alarm = False

    def state(self, mode: str):
        """Dedicated button state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            # 🔄 FIX: Re-bind core canvas event loops cleanly when coming back to active status
            try:
                self._canvas.bind("<Enter>", self._on_enter)
                self._canvas.bind("<Leave>", self._on_leave)
                self._canvas.bind("<Button-1>", self._on_clicked)
                self._canvas.bind("<ButtonRelease-1>", self._on_clicked)
            except Exception:
                pass

            # Restore standard look
            self.configure(state="normal", hover=True)
            self._update_current_visual_state()
            self._custom_current_state = "normal"

        elif mode == "disabled":
            # 🔄 FIX: Explicitly unbind cursor listeners to completely absorb hovering glitches
            try:
                self._canvas.unbind("<Enter>")
                self._canvas.unbind("<Leave>")
                self._canvas.unbind("<Button-1>")
                self._canvas.unbind("<ButtonRelease-1>")
            except Exception:
                pass

            # Lock interaction engine
            self.configure(state="disabled", hover=False)

            # Apply custom flat muted gray states
            for key in ("fg_color", "hover_color", "text_color"):
                if key in self._custom_disabled_map:
                    try:
                        self.configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"

    def set_pressed(self, pressed: bool):
        """Toggles the visual pressed state of the button cleanly."""
        if getattr(self, "_custom_current_state", "normal") == "disabled" or self.is_alarm:
            return

        self.is_pressed = pressed
        self._update_current_visual_state()

    def set_alarm_state(self, active: bool):
        """Forces the button into a high-visibility warning red state cleanly."""
        if getattr(self, "_custom_current_state", "normal") == "disabled":
            return

        self.is_alarm = active
        if self.is_alarm:
            self.is_pressed = False

        self._update_current_visual_state()

    def _update_current_visual_state(self):
        """
        MASTER VISUAL ROUTER: Dynamically maps configuration layouts out of memory.
        """
        # A. ALARM STATE TAKES IMMEDIATE PRIORITY
        if self.is_alarm:
            self.configure(
                fg_color=self._custom_alarm_map.get("fg_color"),
                hover_color=self._custom_alarm_map.get("hover_color"),
                text_color=self._custom_alarm_map.get("text_color"),
                hover=False
            )
        # B. PRESSED STATE TAKES SECONDARY PRIORITY
        elif self.is_pressed:
            self.configure(
                fg_color=self._custom_pressed_map.get("fg_color"),
                hover_color=self._custom_pressed_map.get("hover_color"),
                text_color=self._custom_pressed_map.get("text_color"),
                hover=False
            )
        # C. FALLBACK TO NORMAL THEME
        else:
            # Safely pulls runtime configurations straight from your clean keyword storage dictionary
            self.configure(
                fg_color=self.final_kw.get("fg_color", self._local_defaults.get("fg_color")),
                hover_color=self.final_kw.get("hover_color", self._local_defaults.get("hover_color")),
                text_color=self.final_kw.get("text_color", self._local_defaults.get("text_color")),
                hover=True
            )


if __name__ == "__main__":
    if __name__ == "__main__":
        ctk.set_appearance_mode("dark")
        root = ctk.CTk()
        root.geometry("400x400")

        widget = sCTkButtonPrimary(root, text="System Action Button")
        widget1 = sCTkButtonPrimary(root, text="testpressed")
        widget1.configure(text="testpressed")

        # 🔄 FIX: Remove expand=True and fill="both" so the button scales to its true width/height config!
        widget.pack(padx=40, pady=40)
        widget1.pack(padx=40, pady=40)

        # Test tracking loop sequences
        widget.state("normal")
        print(widget.get_state())

        # widget.set_alarm_state(True)
        widget1.set_pressed(True)

        # widget.state("normal")
        # print(widget.get_state())

        root.mainloop()

