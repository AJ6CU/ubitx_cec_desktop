#!/usr/bin/python3
"""
secondaryButton

secondary ctk button

UI source file: buttonSecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import buttonSecondaryui as baseui


#
# Manual user code
#
# Global theme sync
# ctk.set_appearance_mode("System")

class buttonSecondary(baseui.buttonSecondaryUI):
    def __init__(self, master=None, **kw):

        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "fg_color": ("#E5E7EB", "#374151"),
            "hover_color": ("#D1D5DB", "#4B5563"),
            "text_color": ("#1F2937", "#F9FAFB"),
            "border_width": 2,  # Ensure border renders
            "border_color": ("#9CA3AF", "#4B5563")  # Add distinct border colors
        }
        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = buttonSecondary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
