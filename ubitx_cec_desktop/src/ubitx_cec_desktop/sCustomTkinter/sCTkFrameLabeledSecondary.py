#!/usr/bin/python3
"""
sCTkFrameLabeledSecondary

Similer to ttk.labelframe built on ctkscrollableframe with scrollbars hidden

UI source file: sCTkFrameLabeledSecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import sCTkFrameLabeledSecondaryui as baseui


#
# Manual user code
#

class sCTkFrameLabeledSecondary(baseui.sCTkFrameLabeledSecondaryUI):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "border_color": ("#0f4d1e", "#00ff66"),
            "border_width": 1,
            "label_font": ("Arial", 12, "normal"),
            "label_text_color": ("#111827", "#F9FAFB"),
        }

        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)

        #
        #   The following gets the current background color and tries to hide the scrollbar by making it the same color
        #   This allows us to use the scrollerdlabelframe instead of creating one our selves from a frame to emulate
        #   a ttk.labelframe
        #
        current_bg = self.cget("fg_color")
        self.configure(
            scrollbar_button_color=current_bg,
            scrollbar_button_hover_color=current_bg,
            scrollbar_fg_color=current_bg
        )

        self._scrollbar.configure(height=0)


if __name__ == "__main__":
    root = tk.Tk()
    widget = sCTkFrameLabeledSecondary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
