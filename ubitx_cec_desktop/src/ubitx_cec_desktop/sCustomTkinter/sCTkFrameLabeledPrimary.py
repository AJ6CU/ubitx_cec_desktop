#!/usr/bin/python3
"""
sCTkFrameLabeledPrimary

Similer to ttk.labelframe built on ctkscrollableframe with scrollbars hidden

UI source file: sCTkFrameLabeledPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import os
import sCTkFrameLabeledPrimaryui as baseui


#
# Manual user code
#

class sCTkFrameLabeledPrimary(baseui.sCTkFrameLabeledPrimaryUI):
    def __init__(self, master=None, **kw):

        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "border_color": ("#2ed158", "#11802b"),
            "border_width": 2,
            "label_font": ("Arial", 15, "bold"),
            "label_text_color": ("#111827", "#F9FAFB"),
        }
        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)

        #
        #   This allows us to hide the scrollbar by making it the same color as the background. We are doing
        #   this to provide the equivalent to ttk.labelframe without having to create it from scratch
        #
        current_bg = self.cget("fg_color")
        self.configure(
            scrollbar_button_color=current_bg,
            scrollbar_button_hover_color=current_bg,
            scrollbar_fg_color=current_bg,
        )

        self._scrollbar.configure(height=0)

    def bind(self, sequence=None, command=None, add=None):
        if "PYGUBU_DESIGNER_RUNNING" in os.environ:
            # Avoid error, do nothing.
            pass
        else:
            # Send request to parent class
            return super().bind(sequence, command, add)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkFrameLabeledPrimary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
