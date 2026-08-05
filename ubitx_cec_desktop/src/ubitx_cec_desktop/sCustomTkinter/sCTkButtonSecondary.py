#!/usr/bin/python3
"""
buttonSecondary

secondary ctk button

UI source file: sCTkButtonSecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkButtonSecondaryui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkButtonSecondary(baseui.sCTkButtonSecondaryUI,ThemeableWidget):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "font": ("Arial", 15, "normal"),
            "fg_color": ("#E5E7EB", "#374151"),
            "hover_color": ("#D1D5DB", "#4B5563"),
            "text_color": ("#1F2937", "#F9FAFB"),
            "border_width": 2,  # Ensure border renders
            "border_color": ("#9CA3AF", "#4B5563"),  # Add distinct border colors
            "corner_radius": 6,

            "disabled_map": {
                "fg_color": ("#F3F4F6", "#1F2937"),
                "hover_color": ("#F3F4F6", "#1F2937"),  # FIX: Absorbs hover glow
                "border_color": ("#E5E7EB", "#374151"),
                "text_color": ("#94A3B8", "#64748B")
            },
            # 🔄 MOD A: Add your custom secondary pressed configuration!
            "pressed_map": {
                "fg_color": ("#CBD5E1", "#1F2937"),  # Significantly darkens layout frame layer
                "hover_color": ("#CBD5E1", "#1F2937"),
                "border_color": ("#475569", "#94A3B8"),  # Sharpens edge lines for compressed feedback
                "text_color": ("#0F172A", "#FFFFFF")
            }
        }
        # 🔄 MOD B: Store your custom pressed data map reference safely
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})
        self._custom_pressed_map = theme_defaults.get("pressed_map", {})

        # Run our shared theme logic first to sanitize parameters
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter natively
        super().__init__(master, **self.final_kw)

        # 🔄 MOD C: Set up your local press tracking boolean state flag
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

            # 🔄 MOD F: Force re-evaluation of flags to maintain persistent looks!
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
            for key in ("fg_color", "hover_color", "border_color", "text_color"):
                if key in self._custom_disabled_map:
                    try:
                        self.configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"

    # 🔄 MOD D: Add the toggle mechanism block
    def set_pressed(self, pressed: bool):
        """Toggles the visual pressed state of the secondary button cleanly."""
        # Block interaction states immediately if the button is disabled
        if getattr(self, "_custom_current_state", "normal") == "disabled":
            return

        self.is_pressed = pressed
        self._update_current_visual_state()

    # 🔄 MOD E: Build your clean, alarm-free visual router loop!
    def _update_current_visual_state(self):
        """
        MASTER VISUAL ROUTER: Evaluates the secondary button's press status variable
        and dynamically maps configuration layouts out of memory.
        """
        # A. PRESSED STATE TAKES PRIMARY LOCAL PRIORITY
        if self.is_pressed:
            self.configure(
                fg_color=self._custom_pressed_map.get("fg_color"),
                hover_color=self._custom_pressed_map.get("hover_color"),
                border_color=self._custom_pressed_map.get("border_color"),
                text_color=self._custom_pressed_map.get("text_color"),
                hover=False
            )
        # B. FALLBACK TO STANDARD ACTIVE THEME CONFIGURATION
        else:
            self.configure(
                fg_color=self.final_kw.get("fg_color", self._local_defaults.get("fg_color")),
                hover_color=self.final_kw.get("hover_color", self._local_defaults.get("hover_color")),
                border_color=self.final_kw.get("border_color", self._local_defaults.get("border_color")),
                text_color=self.final_kw.get("text_color", self._local_defaults.get("text_color")),
                hover=True
            )



if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x400")

    widget = sCTkButtonSecondary(root, text="System Action Button")
    widget1 = sCTkButtonSecondary(root, text="testpressed")
    widget1.configure(text="testpressed")

    # 🔄 FIX: Remove expand=True and fill="both" so the button scales to its true width/height config!
    widget.pack(padx=40, pady=40)
    widget1.pack(padx=40, pady=40)

    # Test tracking loop sequences
    widget.state("normal")
    print(widget.get_state())

    # widget.set_alarm_state(True)
    widget1.set_pressed(True)

    widget.state("disabled")
    print(widget.get_state())

    root.mainloop()

