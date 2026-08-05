
#!/usr/bin/python3
"""
sCTkButtonTertiary

subclass of CTkButton (Universal Platform Border-Driven Outline Latching Toggle Variant)

UI source file: sCTkButtonTertiary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import platform
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
import sCTkButtonTertiaryui as baseui
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#

class sCTkButtonTertiary(baseui.sCTkButtonTertiaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        theme_defaults = THEME_DEFAULTS["sCTkButtonTertiary"]

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
                self._canvas.bind("<ButtonRelease>", self._on_clicked)
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
                self._canvas.unbind("<ButtonRelease>")
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
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x200")

    from sCTkFrame import sCTkFrame
    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkButtonTertiary(base)
    widget.configure(text="push me", command=lambda: widget.set_pressed(True))
    widget1 = sCTkButtonTertiary(base, text="normal button")

    widget.pack(expand=False, fill="none", padx=40, pady=15)
    widget1.pack(expand=False, fill="none", padx=40, pady=15)

    # Verify our custom cascading state system locks down the entire panel hierarchy instantly!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("Widget 0 state =", widget.get_state())
    print("Widget 1 state =", widget1.get_state())

    # Verify the cascade pipeline unlocks everything smoothly right back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("Widget 0 state =", widget.get_state())
    print("Widget 1 state =", widget1.get_state())

    root.mainloop()


