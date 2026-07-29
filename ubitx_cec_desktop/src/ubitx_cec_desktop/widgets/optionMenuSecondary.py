#!/usr/bin/python3
"""
optionMenuSecondary

Tailored version of the standard ctkOptionMenu for secondary

UI source file: optionMenuSecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import optionMenuSecondaryui as baseui


#
# Manual user code
#

class optionMenuSecondary(baseui.optionMenuSecondaryUI):
    def __init__(self, master=None, **kw):

        #
        #   Defaults for this widget
        #
        theme_defaults = {
            # The resting surface color (Light: soft off-white gray, Dark: charcoal slate)
            "fg_color": ("#F3F4F6", "#374151"),
            'button_color': ("#F3F4F6", "#374151"),

            # Active text color
            "text_color": ("#1F2937", "#F9FAFB"),

            # THE FIX: Shifting the light mode hover much darker (to a crisp slate gray)
            # and the dark mode hover slightly brighter to clearly show state changes.
            "button_hover_color": ("#94A3B8", "#4B5563"),

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
    widget = optionMenuSecondary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
