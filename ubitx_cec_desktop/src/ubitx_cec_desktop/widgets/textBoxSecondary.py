#!/usr/bin/python3
"""
textBoxSecondary

Similer to ttk.labelframe built on ctkscrollableframe with scrollbars hidden. This textBox is typically used for user information or explanations as there is no border and the font is smaller.

UI source file: textBoxSecondary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import re
import customtkinter as ctk
import textBoxSecondaryui as baseui


#
# Manual user code
#

class textBoxSecondary(baseui.textBoxSecondaryUI):
    def __init__(self, master=None, **kw):
        #
        #   Defaults for this widget
        #
        theme_defaults = {
            "border_width": 0,
            "border_color": ("#b5beb6", "#3d5242"),  # Matches frame outlines
            "fg_color": ("#cbcfcb", "#1a1a1a"),  # Recessed input surface
            "text_color": ("#1c1d1c", "#e3ece4"),  # High legibility text pairing
            "scrollbar_button_color": ("#2ed158", "#11802b"),  # Brand green handles
            "scrollbar_button_hover_color": ("#1f9c40", "#0b541c"),  # Interactive hover green
            "font": ("Arial", 11, "normal"),
            "wrap": "word"
        }
        #
        #   Merge them into the kw
        #
        kw = theme_defaults | kw

        super().__init__(master, **kw)

    def configure(self, *args, **kw):
        if "text" in kw:
            new_text = kw.pop("text")
            self.delete(0.0, "end")
            self.insert(0.0, new_text)

        # Handle font configuration conversion
        if "font" in kw:
            font_val = kw["font"]

            if isinstance(font_val, str):
                # Remove a leading "font " prefix if it exists
                if font_val.lower().startswith("font "):
                    font_val = font_val[5:].strip()

                # Extract tokens inside curly braces, quotes, or standalone words
                tokens = re.findall(r'\{([^}]+)\}|"([^"]+)"|\'([^\']+)\'|(\S+)', font_val)
                # Flatten the regex tuple groups and remove empty matches
                tokens = [next(t for t in g if t) for g in tokens if any(g)]

                if tokens:
                    # Parameter 1: Family
                    family = tokens[0]

                    # Parameter 2: Size
                    size = int(tokens[1]) if len(tokens) > 1 and tokens[1].replace('-', '').isdigit() else 12

                    # Remaining tokens are styles. If styles were grouped like {bold italic}, split them.
                    styles = []
                    for t in tokens[2:]:
                        styles.extend(t.lower().split())

                    weight = "bold" if "bold" in styles else "normal"
                    slant = "italic" if "italic" in styles else "roman"
                    underline = True if "underline" in styles or "true" in styles else False
                    overstrike = True if "overstrike" in styles or "true" in styles else False

                    # Convert string format to a full native CTkFont object
                    kw["font"] = ctk.CTkFont(
                        family=family,
                        size=size,
                        weight=weight,
                        slant=slant,
                        underline=underline,
                        overstrike=overstrike
                    )

        # Pass remaining keyword arguments to parent class
        return super().configure(*args, **kw)


if __name__ == "__main__":
    root = tk.Tk()
    widget = textBoxSecondary(root)
    widget.pack(expand=True, fill="both")
    root.mainloop()
