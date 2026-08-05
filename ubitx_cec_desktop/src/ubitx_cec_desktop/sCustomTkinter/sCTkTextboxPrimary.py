#!/usr/bin/python3
"""
sCTkTextboxPrimary

update to ctktextbox

UI source file: sCTkTextboxPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkTextboxPrimaryui as baseui
from ThemeableWidget import ThemeableWidget
from sCTkFrame import sCTkFrame


#
# Manual user code
#

class sCTkTextboxPrimary(baseui.sCTkTextboxPrimaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            # 📐 Physical Sizing & Typography
            "font": ("Arial", 13, "normal"),
            "border_width": 1,
            "corner_radius": 6,

            # 🎨 Canvas Base Layers (Sage/Charcoal Palette Profile)
            "border_color": ("#b5beb6", "#3d5242"),
            "fg_color": ("#cbcfcb", "#1a1a1a"),
            "text_color": ("#1c1d1c", "#e3ece4"),

            # 🟢 Internal Native Scrollbar Map
            "scrollbar_button_color": ("#64748B", "#4B5563"),
            "scrollbar_button_hover_color": ("#1A4375", "#2471A3"),

            # ⛔ Muted Disabled Overlay
            "disabled_map": {
                "fg_color": ("#E5E7EB", "#111827"),  # Lock container canvas back completely
                "border_color": ("#CBD5E1", "#1F2937"),
                "text_color": ("#94A3B8", "#64748B"),
                "scrollbar_button_color": ("#E5E7EB", "#1F2937"),  # Mutes the inner handle tracking rails
                "scrollbar_button_hover_color": ("#E5E7EB", "#1F2937")
            }
        }

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries safely
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array securely
        super().__init__(master, **self.final_kw)

        # 🔄 FIX: Self-correcting transparency workaround!
        # If the text box lands on top of a transparent container panel, it dynamically
        # climbs up the layout tree to fetch the window's true underlying background colors,
        # perfectly matching your camouflage look without triggering a transparency error!
        try:
            current_fg = self.cget("fg_color")
            if current_fg == "transparent" or current_fg == "":
                # Fallback to the master's true background asset tuple
                parent_bg = self.master.cget("fg_color")
                if parent_bg != "transparent" and parent_bg != "":
                    self.configure(fg_color=parent_bg)
        except Exception:
            pass

    def state(self, mode: str):
        """Dedicated text field state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            self.configure(state="normal")

            # Dynamically restore all active properties out of final_kw
            for key in ("fg_color", "border_color", "text_color", "scrollbar_button_color",
                        "scrollbar_button_hover_color"):
                active_val = self.final_kw.get(key, self._local_defaults.get(key))
                try:
                    self.configure(**{key: active_val})
                except Exception:
                    pass

            self._custom_current_state = "normal"

        elif mode == "disabled":
            self.configure(state="disabled")

            # Dynamically apply your complete high-contrast disabled muted configurations out of your map!
            for key in ("fg_color", "border_color", "text_color", "scrollbar_button_color",
                        "scrollbar_button_hover_color"):
                if key in self._custom_disabled_map:
                    try:
                        self.configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("500x400")

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkTextboxPrimary(base)
    widget.pack(expand=True, fill="both", padx=10, pady=10)

    # Pre-populate sample message streams to check text visibility metrics
    widget.insert("0.0", "System Telemetry Buffer Active...\nListening on COM-04 trace line...\n")

    # Verify our custom cascading state system locks down the canvas and text elements instantly!
    widget.state("disabled")
    print("state (Disabled Sequence) =", widget.get_state())  # Output: disabled

    # widget.state("normal")
    # print("state (Normal Sequence)   =", widget.get_state())  # Output: normal

    root.mainloop()
