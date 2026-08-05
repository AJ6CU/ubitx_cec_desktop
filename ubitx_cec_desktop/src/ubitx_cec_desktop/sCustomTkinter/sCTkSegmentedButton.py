#!/usr/bin/python3
"""
sCTkSegmentedButton

segmentedButton

UI source file: sCTkSegmentedButton.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import os
import sCTkSegmentedButtonui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkSegmentedButton(baseui.sCTkSegmentedButtonUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        theme_defaults = {
            # 🔤 Typography matching your core form controls
            "font": ("Arial", 15, "normal"),

            # 🎨 Base Track Background (Pure neutral medium gray / dark container)
            "fg_color": ("#9E9E9E", "#111827"),

            # 📝 Active selected text remains crisp white over the brand blue
            "text_color": ("#FFFFFF", "#FFFFFF"),

            # 📈 Selected / Active Segment (Your primary OptionMenu/ComboBox brand navy blues)
            "selected_color": ("#1A4375", "#2471A3"),
            "selected_hover_color": ("#112A4B", "#1F618D"),

            # 🖱️ The perfect mid-dark neutral gray tone
            "unselected_color": ("#9E9E9E", "#1F2937"),
            "unselected_hover_color": ("#7D7D7D", "#374151"),  # Smoothly deepens on hover

            # ⛔ Muted Disabled Overlay
            "disabled_map": {
                # 🔄 FIX: Lightened the track background BEHIND the buttons completely to match your frame panels!
                "fg_color": ("#FFFFFF", "#111827"),

                # The individual button segments preserve their crisp, solid inactive looks
                "selected_color": ("#64748B", "#4B5563"),
                "unselected_color": ("#64748B", "#4B5563"),

                # Hover states completely lock to the background color to mask cursor movements
                "selected_hover_color": ("#64748B", "#4B5563"),
                "unselected_hover_color": ("#64748B", "#4B5563"),

                # Text turns into a light silver font in light mode, and a soft gray font in dark mode
                "text_color": ("#CBD5E1", "#94A3B8")
            }

        }

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # 🔄 FIX: Pass exactly TWO dictionary arguments to stay synchronized with your master engine class
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array securely
        super().__init__(master, **self.final_kw)

    def state(self, mode: str):
        """Dedicated segmented button row state controller."""
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            # Natively unlock mouse tracking click streams safely
            self.configure(state="normal")

            # Dynamically pull the exact active colors without hardwired strings
            for key in ("selected_color", "selected_hover_color", "unselected_color", "unselected_hover_color"):
                active_val = self.final_kw.get(key, self._local_defaults.get(key))
                try:
                    self.configure(**{key: active_val})
                except Exception:
                    pass

            # Re-apply crisp active text color settings to the internal navigation label buttons
            if hasattr(self, "_buttons_dict"):
                active_txt = self.final_kw.get("text_color", self._local_defaults.get("text_color"))
                for button in self._buttons_dict.values():
                    button.configure(text_color=active_txt)

            self._custom_current_state = "normal"

        elif mode == "disabled":
            # Natively freeze segment selections entirely
            self.configure(state="disabled")

            # Flatten the background track tabs into an identical muted look layout box
            updates = {}
            for key in ("selected_color", "selected_hover_color", "unselected_color", "unselected_hover_color"):
                if key in self._custom_disabled_map:
                    updates[key] = self._custom_disabled_map[key]

            try:
                self.configure(**updates)
            except Exception:
                pass

            # 🔄 FIX: Reach deep into the internal button dictionary to override text color configurations!
            # This completely fixes CustomTkinter's native font coloring bug when disabled.
            if hasattr(self, "_buttons_dict"):
                disabled_txt = self._custom_disabled_map.get("text_color", ("#CBD5E1", "#94A3B8"))
                for button in self._buttons_dict.values():
                    button.configure(text_color=disabled_txt)

            self._custom_current_state = "disabled"

    def bind(self, sequence=None, command=None, add=None):
        if "PYGUBU_DESIGNER_RUNNING" in os.environ:
            pass
        else:
            return super().bind(sequence, command, add)


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("500x200")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # Instantiate with a sample parameter selector array
    widget = sCTkSegmentedButton(base, values=["VFO-A", "VFO-B", "MEM-BANK", "SPLIT"])
    widget.pack(expand=False, fill="none", padx=10, pady=10)
    widget.set("VFO-A")

    # Verify our custom state loop handles double-pass transitions flawlessly on the console
    widget.state("disabled")
    print("state (Disabled Pass) =", widget.get_state())  # Output: disabled

    # widget.state("normal")
    # print("state (Normal Pass)   =", widget.get_state())  # Output: normal

    root.mainloop()
