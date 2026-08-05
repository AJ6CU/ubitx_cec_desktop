#!/usr/bin/python3
"""
sCTkScrollbar

scrollbar

UI source file: sCTkScrollbar.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkScrollbarui as baseui
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#

class sCTkScrollbar(baseui.sCTkScrollbarUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # Safely parse orientation out of the incoming properties dictionary pass
        orientation = kw.get("orientation", "vertical").lower()
        is_horizontal = orientation == "horizontal"

        # Define the universal color system
        theme_defaults = {
            "corner_radius": 4,
            "fg_color": "transparent",
            "button_color": ("#64748B", "#4B5563"),
            "button_hover_color": ("#1A4375", "#2471A3"),

            # ⛔ Muted Disabled Overlay
            "disabled_map": {
                "button_color": ("#E5E7EB", "#1F2937")
            }
        }

        # Physical Geometry Injector: Lock down dimensions safely right inside the defaults mapping
        if is_horizontal:
            theme_defaults["height"] = 14
        else:
            theme_defaults["width"] = 14

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Aligned parameters to pass exactly TWO dictionary objects up to the base theme class
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Pop out "state" to protect the initial constructor pass
        initial_state = self.final_kw.pop("state", "normal")

        # Initialize CustomTkinter cleanly with the safe final kwargs array
        super().__init__(master, **self.final_kw)

        # Apply the initial state parameter via our tracker function post-creation safely
        if initial_state == "disabled":
            self.state("disabled")

    def state(self, mode: str):
        """
        Dedicated standalone scrollbar state controller.
        Bypasses native configuration blocks by unbinding/re-binding raw mouse event listeners.
        """
        mode = mode.lower()

        if mode in ("normal", "enabled", "active"):
            # 🔄 FIX: Re-bind CustomTkinter's native framework listener shortcuts to maintain scope!
            try:
                self._canvas.bind("<Enter>", self.enter)
                self._canvas.bind("<Leave>", self.leave)
                self._canvas.bind("<Button-1>", self.clicked)
                self._canvas.bind("<B1-Motion>", self.scrolled)
            except Exception:
                pass

            # Restore your original dynamic color states from our theme dictionary pass
            for key in ("fg_color", "button_color", "button_hover_color"):
                active_val = self.final_kw.get(key, self._local_defaults.get(key))
                try:
                    self.configure(**{key: active_val})
                except Exception:
                    pass

            self._custom_current_state = "normal"

        elif mode == "disabled":
            # Completely isolate mouse dragging interactions by stripping canvas listeners!
            try:
                self._canvas.unbind("<Enter>")
                self._canvas.unbind("<Leave>")
                self._canvas.unbind("<Button-1>")
                self._canvas.unbind("<B1-Motion>")
            except Exception:
                pass

            # Extract your customized muted configuration tuple safely
            target_disabled_color = self._custom_disabled_map.get("button_color", ("#E5E7EB", "#1F2937"))

            updates = {}
            if "button_color" in self._custom_disabled_map:
                updates["button_color"] = target_disabled_color
                # Force hover parameters to match to neutralize glowing animations
                updates["button_hover_color"] = target_disabled_color

            try:
                self.configure(**updates)
            except Exception:
                pass

            self._custom_current_state = "disabled"


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x250")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # Showcase standard vertical tracking handle operations
    widget = sCTkScrollbar(base, orientation="vertical")
    widget.pack(side="right", fill="y", padx=5, pady=5)

    # Test tracking loop sequences on your console window
    widget.state("disabled")
    print("state =", widget.get_state())  # Output: disabled

    widget.state("normal")
    print("state =", widget.get_state())  # Output: normal

    root.mainloop()
