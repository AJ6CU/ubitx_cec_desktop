#!/usr/bin/python3
"""
optionMenuSecondary

Tailored version of the standard ctkOptionMenu for secondary

UI source file: sCTkOptionMenuSecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkOptionMenuSecondaryui as baseui


#
# Manual user code
#

class sCTkOptionMenuSecondary(baseui.sCTkOptionMenuSecondaryUI):
    def __init__(self, master=None, **kw):

        #
        #   Defaults for this widget
        #
        theme_defaults = {
            # 🔤 Font scaled down to 13 for secondary hierarchy
            "font": ("Arial", 13, "normal"),
            "dropdown_font": ("Arial", 13, "normal"),

            # 🎨 FIX: Max dark mode contrast. Uses deep charcoal (#111827) to match entry field backgrounds
            "fg_color": ("#F3F4F6", "#111827"),
            "button_color": ("#F3F4F6", "#111827"),

            # 📝 High-contrast neutral text (Dark text in Light Mode, Light text in Dark Mode)
            "text_color": ("#1F2937", "#F9FAFB"),

            # 🖱️ Responsive Hover states (Dark mode now jumps significantly to #374151)
            "button_hover_color": ("#94A3B8", "#374151"),

            # 📋 Dropdown options
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
    widget = sCTkOptionMenuSecondary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
