#!/usr/bin/python3
"""
sCTkScrollbar

scrollbar

UI source file: sCTkScrollbar.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkScrollbarui as baseui


#
# Manual user code
#

class sCTkScrollbar(baseui.sCTkScrollbarUI):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)

        # 2. Query the object directly to check its true orientation state
        is_horizontal = self.cget("orientation") == "horizontal"

        # 3. Define the universal color system
        theme_defaults = {
            "corner_radius": 4,
            "fg_color": "transparent",
            "button_color": ("#64748B", "#4B5563"),
            "button_hover_color": ("#1A4375", "#2471A3")
        }

        # 4. Inject only the non-conflicting dimension key
        if is_horizontal:
            theme_defaults["height"] = 14
        else:
            theme_defaults["width"] = 14

        # 5. Safely lock in the theme configurations on the active widget
        self.configure(**theme_defaults)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkScrollbar(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
