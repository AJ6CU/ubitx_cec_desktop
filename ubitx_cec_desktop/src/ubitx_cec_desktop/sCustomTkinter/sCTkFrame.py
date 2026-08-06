#!/usr/bin/python3
"""
sCTkFrame

subclass of Frame tuned for this ux

UI source file: sCTkFrame.ui
"""
import tkinter as tk
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
import tkinter.ttk as ttk
import sCTkFrameui as baseui
from ThemeableWidget import ThemeableWidget


#
# Manual user code
#

class sCTkFrame(baseui.sCTkFrameUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        theme_defaults = THEME_DEFAULTS["sCTkFrame"]

        # Run our shared theme logic first to sanitize parameters and build self.final_kw
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # Initialize CustomTkinter with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x300")

    # This frame drops on your window completely invisible as a layout placeholder panel container!
    widget = sCTkFrame(root)
    widget.pack(expand=True, fill="both", padx=30, pady=30)

    # Let's drop a themeable input child inside to verify the invisible cascade routing
    from sCTkEntryPrimary import sCTkEntryPrimary

    test_input = sCTkEntryPrimary(widget)
    test_input.pack(padx=20, pady=20, fill="x")


    # Verify our custom cascading state system locks down the container block!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("Outlined Card panel tracker =", widget.get_state())
    print("Nested child Entry tracker  =", test_input.get_state())

    # Verify the cascade pipeline unlocks everything smoothly right back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("Outlined Card panel tracker =", widget.get_state())
    print("Nested child Entry tracker  =", test_input.get_state())

    root.mainloop()
