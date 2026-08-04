#!/usr/bin/python3
"""
sCTkOptionMenuPrimary

Tailored version of the standard ctkOptionMenu

UI source file: sCTkOptionMenuPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkOptionMenuPrimaryui as baseui


#
# Manual user code
#

class sCTkOptionMenuPrimary(baseui.sCTkOptionMenuPrimaryUI):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "font": ("Arial", 15, "normal"),
            "dropdown_font": ("Arial", 15, "normal"),
            # Match fg_color to  button color so the whole menu is cohesive
            "fg_color": ("#1A4375", "#2471A3"),
            'button_color': ("#1F538D", "#2471A3"),

            # Clean, high-contrast text
            "text_color": ("#FFFFFF", "#FFFFFF"),

            # The entire widget now visually shifts deep navy (light) or rich slate blue (dark) on hover
            "button_hover_color": ("#112A4B", "#1F618D"),

            # Dropdown menu canvas and styling
            "dropdown_fg_color": ("#FFFFFF", "#1F2937"),
            "dropdown_text_color": ("#1F2937", "#F9FAFB"),
            "dropdown_hover_color": ("#E5E7EB", "#374151")
        }
        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)

    def update_list(self, new_values: list, default_index: int = 0):
        """Safely updates the items list and resets the visible value."""
        if not new_values:
            self.configure(values=[""])
            self.set("")
            return

        self.configure(values=new_values)

        # Guard against index out of bounds errors
        if default_index < len(new_values):
            self.set(new_values[default_index])
        else:
            self.set(new_values[0])


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkOptionMenuPrimary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
