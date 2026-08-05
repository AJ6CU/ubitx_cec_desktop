#!/usr/bin/python3
"""
sCTkTabview

subclass of CTkTabview (Multi-Page Dashboard Deck Layout Container)

UI source file: sCTkTabview.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
import sCTkTabviewui as baseui
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#

class sCTkTabview(baseui.sCTkTabviewUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        theme_defaults = THEME_DEFAULTS["sCTkTabview"]

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run standard shared dict parsing code
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Intercept the non-standard key locally just for this specific constructor signature pass
        target_font = self.final_kw.pop("font", theme_defaults.get("font"))

        # Initialize CustomTkinter with the clean final kwargs array securely
        super().__init__(master, **self.final_kw)

        # Forward the extracted font parameter down to the navigation bar layer safely
        if hasattr(self, "_segmented_button"):
            self._segmented_button.configure(font=target_font)

    def state(self, mode: str):
        """Dedicated Tabview composite state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            if hasattr(self, "_segmented_button"):
                self._segmented_button.configure(state="normal")

                # Restore original dynamic color states from our theme dictionary pass
                for key in ("fg_color", "selected_color", "unselected_color", "selected_hover_color",
                            "unselected_hover_color"):
                    mapped_key = f"segmented_button_{key}"
                    active_val = self.final_kw.get(mapped_key, self._local_defaults.get(mapped_key))
                    try:
                        self._segmented_button.configure(**{key: active_val})
                    except Exception:
                        pass

                # Re-apply sharp text color settings to the internal navigation label buttons
                if hasattr(self._segmented_button, "_buttons_dict"):
                    active_txt = self.final_kw.get("text_color", self._local_defaults.get("text_color"))
                    for button in self._segmented_button._buttons_dict.values():
                        button.configure(text_color=active_txt)

            self._custom_current_state = "normal"

        elif mode == "disabled":
            if hasattr(self, "_segmented_button"):
                self._segmented_button.configure(state="disabled")

                # Flatten the background track tabs and the master backing row block frame cleanly
                updates = {}
                if "segmented_button_fg_color" in self._custom_disabled_map:
                    updates["fg_color"] = self._custom_disabled_map["segmented_button_fg_color"]
                if "segmented_button_selected_color" in self._custom_disabled_map:
                    updates["selected_color"] = self._custom_disabled_map["segmented_button_selected_color"]
                    updates["selected_hover_color"] = self._custom_disabled_map["segmented_button_selected_color"]
                if "segmented_button_unselected_color" in self._custom_disabled_map:
                    updates["unselected_color"] = self._custom_disabled_map["segmented_button_unselected_color"]
                    updates["unselected_hover_color"] = self._custom_disabled_map["segmented_button_unselected_color"]

                try:
                    self._segmented_button.configure(**updates)
                except Exception:
                    pass

                # Override and drop internal button label text contrast
                if hasattr(self._segmented_button, "_buttons_dict"):
                    disabled_txt = self._custom_disabled_map.get("text_color", ("#94A3B8", "#64748B"))
                    for button in self._segmented_button._buttons_dict.values():
                        button.configure(text_color=disabled_txt)

            self._custom_current_state = "disabled"


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")

    root = ctk.CTk()
    root.geometry("500x350")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkTabview(base)
    widget.pack(expand=True, fill="both", padx=10, pady=10)

    widget.add("Transceiver Settings")
    widget.add("Audio Filters")
    widget.add("System Logs")

    # Verify our custom cascading state system locks down the multi-page deck layout container!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("state (Disabled Pass) =", widget.get_state())  # Output: disabled

    # FIX: Re-activated to verify fluid return-to-normal parameters tracking flows flawlessly
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("state (Normal Pass)   =", widget.get_state())  # Output: normal

    root.mainloop()
