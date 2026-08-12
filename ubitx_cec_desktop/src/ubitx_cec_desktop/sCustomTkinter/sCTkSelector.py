# Derived from Selector class by Fastattack, 2024).
# https://github.com/fastattackv/MoreCustomTkinterWidgets
#
#
import customtkinter as ctk
from sCTkFrame import sCTkFrame
from sCTkCheckBox import sCTkCheckBox
from sCTkButtonPrimary import sCTkButtonPrimary
from sCTkScrollableFrame import sCTkScrollableFrame
from sCTkEntryPrimary import sCTkEntryPrimary

# Import your theme manager structures
from ThemeableWidget import ThemeableWidget
from sCTkThemes import THEME_DEFAULTS
from typing import Optional


class sCTkSelector(sCTkFrame, ThemeableWidget):
    def __init__(self, master, items: Optional[list[list[str]]] = None, multiple_choices=True, **kwargs):
        """Selector widgets to select options in a list of options.
        Includes a search bar to find different elements faster.
        """
        # 1. Initialize the ThemeableWidget mixin first to build self.final_kw
        # It scans THEME_DEFAULTS["Selector"] and runs corruption guards
        theme_config = THEME_DEFAULTS.get("sCTkSelector", {})
        ThemeableWidget.__init__(self, theme_config, kwargs)

        # 2. Extract configuration arguments intended for child components
        # so they do not contaminate the base CTkFrame constructor.
        # Example: fallback to transparent if no fg_color is defined in your theme
        fg_color = self.final_kw.get("fg_color", "transparent")

        # 3. Call the parent sCTkFrame constructor using the sanitized final_kw map
        super().__init__(master, **self.final_kw)

        self.search_var = ctk.StringVar(self)
        self.search_var.trace_add("write", self._search_modified)

        # 4. Pass down the theme settings to the composite parts
        self.search_bar = sCTkEntryPrimary(self, textvariable=self.search_var)

        # Ensure the scrollable sub-frame respects the primary widget color
        self.checkboxes_frame = sCTkScrollableFrame(self, fg_color=fg_color)

        self.search_bar.pack(anchor="n", fill="x")
        self.checkboxes_frame.pack(expand=True, fill="both", side="bottom")

        self.checkboxes = []
        self.selected_indexes = []
        self.multiple_choices = multiple_choices

        if items is None:
            items =[]

        if len(set(items)) == len(items):
            for index in range(len(items)):
                self.checkboxes.append(sCTkCheckBox(
                    self.checkboxes_frame,
                    text=items[index],
                    command=lambda a=index: self._selection(a)
                ))
            self._search_modified()
        else:
            raise ValueError("There is two times or more the same item in the given items list")

    def _selection(self, index: int):
        """ Internal method: selects / unselects the given index """
        if index in self.selected_indexes:
            self.selected_indexes.remove(index)
        else:
            if self.multiple_choices:
                self.selected_indexes.append(index)
            else:
                if self.selected_indexes:  # list not empty
                    for i in self.selected_indexes:
                        self.checkboxes[i].deselect()
                    self.selected_indexes.clear()
                    self.selected_indexes.append(index)
                else:
                    self.selected_indexes.append(index)

    def _reset_scroll(self):
        """ Internal method: scrolls back to the starting position """
        self.checkboxes_frame._parent_canvas.yview_moveto(0)

    def _search_modified(self, *args):
        """ Internal method: modifies the search """
        value = self.search_var.get()
        row = 0
        for x in range(len(self.checkboxes)):
            if self.checkboxes[x].cget("text").startswith(value):
                self.checkboxes[x].grid(row=row, column=0, padx=3, pady=3)
                row += 1
            else:
                self.checkboxes[x].grid_forget()
        self._reset_scroll()

    def get_all_items(self) -> list:
        """ Returns all the items in the selector """
        return [checkbox.cget("text") for checkbox in self.checkboxes]

    def configure(self, cnf=None, **kwargs):
        """
        Processes both custom widget collections and standard frame attributes
        simultaneously, resolving layout configuration ignore errors.
        """
        import ast

        # 1. Intercept and route list modifications cleanly
        if "items" in kwargs:
            items_val = kwargs.pop("items")
            # Safely handle string parsing if an unparsed literal leaks through
            if isinstance(items_val, str):
                try:
                    items_val = ast.literal_eval(items_val)
                except Exception:
                    items_val = []

            if items_val is not None:
                if len(set(items_val)) == len(items_val):
                    # Destroy old layout checkboxes
                    for checkbox in self.checkboxes:
                        checkbox.destroy()
                    self.checkboxes.clear()
                    self.selected_indexes.clear()

                    # Dynamically instantiate the updated checklist block
                    for index in range(len(items_val)):
                        self.checkboxes.append(sCTkCheckBox(
                            self.checkboxes_frame,
                            text=items_val[index],
                            command=lambda a=index: self._selection(a)
                        ))
                    self._search_modified()
                else:
                    raise ValueError("There is two times or more the same item in the given items list")

        # 2. Intercept and assign the multiple choices boolean flag
        if "multiple_choices" in kwargs:
            mult_val = kwargs.pop("multiple_choices")
            if isinstance(mult_val, str):
                mult_val = str(mult_val).lower() in ['true', '1', 'yes']
            self.multiple_choices = mult_val

        # 3. Synchronize your CustomTkinter theme layers against remaining variables
        theme_config = THEME_DEFAULTS.get("sCTkSelector", {})
        ThemeableWidget.__init__(self, theme_config, kwargs)

        # Keep background coloring synchronized across the sub-scroller canvas layer
        if "fg_color" in self.final_kw:
            new_fg = self.final_kw.get("fg_color")
            if hasattr(self, "checkboxes_frame"):
                self.checkboxes_frame.configure(fg_color=new_fg)

        # 4. Route remaining layout keys (width, height, etc.) safely down to the base Frame
        return super().configure(cnf, **self.final_kw)

    def clear_selections(self):
        """ Clears the selections """
        for index in self.selected_indexes:
            self.checkboxes[index].deselect()
        self.selected_indexes.clear()

    def get_selections(self) -> list:
        """Returns the selected items

        :return: selected items, empty list if none were selected
        """
        return [self.checkboxes[index].cget("text") for index in self.selected_indexes]

if __name__ == "__main__":

    def on_confirm():
        # Save selections before closing
        print(theSelector.get_selections())

    def on_close():
        # Save selections before closing
        print(theSelector.get_selections())
        root.destroy()

    root = ctk.CTk()
    root.geometry("400x350")
    root.title("sCTkSelector Test")
    root.protocol("WM_DELETE_WINDOW", on_close)

    result = []

    items=["vw", "porsche", "roadster", "tesla"]

    # 1. Embed the Selector frame
    theSelector = sCTkSelector(root, items=items, multiple_choices=True)
    theSelector.pack(expand=True, fill="both", padx=10, pady=10)

    # 2. Add a Confirm/OK button
    confirm_btn = sCTkButtonPrimary(root, text="Confirm", command=on_confirm)
    confirm_btn.pack(pady=(0, 10))

    root.mainloop()



