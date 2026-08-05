#!/usr/bin/python3
"""
sCTkFrameLabeledSecondary

Similar to ttk.labelframe built on ctkscrollableframe with scrollbars hidden

UI source file: sCTkFrameLabeledSecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
import os
import sCTkFrameLabeledSecondaryui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkFrameLabeledSecondary(baseui.sCTkFrameLabeledSecondaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        theme_defaults = THEME_DEFAULTS["sCTkFrameLabeledSecondary"]

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Pop out non-standard keys locally right here to prevent constructor crashes!
        lbl_font = self.final_kw.pop("label_font", theme_defaults.get("label_font"))
        lbl_color = self.final_kw.pop("label_text_color", theme_defaults.get("label_text_color"))

        # Safely capture the exact solid active color tuple from our dict pass
        current_bg = self.final_kw.get("fg_color", theme_defaults.get("fg_color"))

        # Initialize the underlying CustomTkinter scrollable frame constructor natively
        super().__init__(master, **self.final_kw)

        # Forward the captured typography configuration attributes down to the header label cleanly
        if hasattr(self, "_label") and self._label is not None:
            self._label.configure(font=lbl_font, text_color=lbl_color)

        # Safely camouflage the scrollbar tracking elements using your exact color matching rules!
        try:
            self.configure(
                scrollbar_fg_color=current_bg,
                scrollbar_button_color=current_bg,
                scrollbar_button_hover_color=current_bg
            )
        except Exception:
            pass

        # Completely collapse the remaining scrollbar handles out of view
        if hasattr(self, "_scrollbar") and self._scrollbar is not None:
            try:
                self._scrollbar.configure(width=0, border_width=0)
            except Exception:
                pass

    def state(self, mode: str):
        """Universal recursive container state controller."""
        mode = mode.lower()

        if mode in ("normal", "enabled", "active"):
            self.configure(border_color=self.final_kw.get("border_color", self._local_defaults.get("border_color")))
            if hasattr(self, "_label") and self._label is not None:
                self._label.configure(
                    text_color=self.final_kw.get("label_text_color", self._local_defaults.get("label_text_color")))

            self._custom_current_state = "normal"

        elif mode == "disabled":
            if "border_color" in self._custom_disabled_map:
                self.configure(border_color=self._custom_disabled_map["border_color"])
            if "label_text_color" in self._custom_disabled_map and hasattr(self, "_label") and self._label is not None:
                self._label.configure(text_color=self._custom_disabled_map["label_text_color"])

            self._custom_current_state = "disabled"

        # 🚀 CASCADING NODE DISCOVERY: Loop recursively over all children inside this container panel frame
        for child in self.winfo_children():
            if hasattr(child, "winfo_children"):
                for inner_child in child.winfo_children():
                    if hasattr(inner_child, "state") and callable(getattr(inner_child, "state")):
                        try:
                            inner_child.state(mode)
                        except Exception:
                            pass

            if hasattr(child, "state") and callable(getattr(child, "state")):
                try:
                    child.state(mode)
                except Exception:
                    pass

    def bind(self, sequence=None, command=None, add=None):
        if "PYGUBU_DESIGNER_RUNNING" in os.environ:
            pass
        else:
            return super().bind(sequence, command, add)


if __name__ == "__main__":
    # # ctk.set_appearance_mode("light")
    root = ctk.CTk()
    root.geometry("500x400")

    widget = sCTkFrameLabeledSecondary(root, label_text="Metadata Filter Attributes")
    widget.pack(expand=True, fill="both", padx=30, pady=30)

    # Injects multiple lines of sub-labels to trigger the camouflage limits beautifully
    from sCTkLabelTertiary import sCTkLabelTertiary

    for note_index in range(1, 16):
        meta_note = sCTkLabelTertiary(
            widget,
            text=f"* Parameter Trace Block {note_index:02d}: Squelch delta thresholds running calibration...",
            anchor="w"
        )
        meta_note.pack(fill="x", padx=15, pady=4)

    # Verify our custom cascading state system locks down the entire panel hierarchy instantly!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("Container Labeled Frame state =", widget.get_state())
    print("Nested log line entry state   =", meta_note.get_state())

    # Verify the cascade pipeline unlocks everything smoothly right back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("Container Labeled Frame state =", widget.get_state())
    print("Nested log line entry state   =", meta_note.get_state())

    root.mainloop()
