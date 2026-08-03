#!/usr/bin/python3
"""
sCTkButtonPrimary

sublass of CTkButton

UI source file: sCTkButtonPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkButtonPrimaryui as baseui


#
# Manual user code
#

class sCTkButtonPrimary(baseui.sCTkButtonPrimaryUI):
    def __init__(self, *args, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
        }
        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(*args, **kw)

        self.is_pressed = False
        self.is_alarm = False  # Track alarm state separately
        self.orig_fg_color = self.cget("fg_color")
        self.orig_hover_color = self.cget("hover_color")
        self.orig_text_color = self.cget("text_color")

    def set_pressed(self, pressed: bool):
        """Toggles the visual pressed state of the button."""
        self.is_pressed = pressed
        if self.is_pressed:
            # save current values
            # Configure 'pressed' visuals: darker color, disable hover
            self.configure(
                # High-contrast pressed colors: (Light Mode Hex, Dark Mode Hex)
                fg_color=("#1F4E79", "#2E86C1"),
                hover_color=("#1F4E79", "#2E86C1"),
                text_color=("#FFFFFF", "#E5E7EB"),  # Brighten text for clarity
                hover=False
            )
        else:
            # Restore normal visuals
            self.restore_defaults()

    def set_alarm_state(self, active: bool):
        """Forces the button into a high-visibility warning red state."""
        self.is_alarm = active
        self.is_pressed = False  # Turn off normal press if alarm is triggered

        if self.is_alarm:
            self.configure(
                # High-contrast alarm reds: (Dark Crimson for Light Mode, Vibrant Red for Dark Mode)
                fg_color=("#990000", "#E74C3C"),
                hover_color=("#990000", "#E74C3C"),
                text_color=("#FFFFFF", "#FFFFFF"),  # Keep text pure white for maximum legibility
                hover=False
            )
        else:
            self.restore_defaults()

    def restore_defaults(self):
        """Helper method to reset the button back to its standard styling."""
        self.configure(
            fg_color=self.orig_fg_color,
            hover_color=self.orig_hover_color,
            text_color=self.orig_text_color,
            hover=True
        )


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkButtonPrimary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
