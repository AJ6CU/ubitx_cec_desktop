import customtkinter as ctk
from sCTkFrame import sCTkFrame
from sCTkCheckBox import sCTkCheckBox
from sCTkButtonPrimary import sCTkButtonPrimary
from sCTkScrollableFrame import sCTkScrollableFrame
from sCTkEntryPrimary import sCTkEntryPrimary


class Selector(sCTkFrame):
    def __init__(self, master, items: list[str], multiple_choices=True, *args, **kwargs):
        """Selector widgets to select options in a list of options. Includes a search bar to find different elements faster.

        :param master: master window for the widget
        :param items: list of the possible options, they should all be different
        :param multiple_choices: Optional: if set to False, the user will be allowed to select only one item (default=True)
        :param args: args for the CTkFrame widget
        :param kwargs: kwargs for the CTkFrame widget
        """
        super().__init__(master, *args, **kwargs)

        self.search_var = ctk.StringVar(self)
        self.search_var.trace_add("write", self._search_modified)
        self.search_bar = sCTkEntryPrimary(self, textvariable=self.search_var)
        color = kwargs.pop("fg_color") if "fg_color" in kwargs else "transparent"
        self.checkboxes_frame = sCTkScrollableFrame(self, fg_color=color, *args, **kwargs)
        self.search_bar.pack(anchor="n", fill="x")
        self.checkboxes_frame.pack(expand=True, fill="both", side="bottom")

        self.checkboxes = []
        self.selected_indexes = []
        self.multiple_choices = multiple_choices
        if len(set(items)) == len(items):  # not 2 times the same item
            for index in range(len(items)):
                self.checkboxes.append(sCTkCheckBox(self.checkboxes_frame, text=items[index], command=lambda a=index: self._selection(a)))
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

    def configure_selector(self, items: list = None, multiple_choices: bool = None):
        """Changes the given arguments

        :param items: new items to show, if [] is given: deletes all old items
        :param multiple_choices: if set to False, the user will be allowed to select only one item
        """
        if items is not None:
            if len(set(items)) == len(items):  # not 2 times the same item
                # destroy old widgets
                for checkbox in self.checkboxes:
                    checkbox.destroy()
                self.checkboxes.clear()
                self.selected_indexes.clear()

                # create new ones
                for index in range(len(items)):
                    self.checkboxes.append(sCTkCheckBox(self.checkboxes_frame, text=items[index], command=lambda a=index: self._selection(a)))
                self._search_modified()
            else:
                raise ValueError("There is two times or more the same item in the given items list")

        if multiple_choices is not None:
            self.multiple_choices = multiple_choices

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
    root.geometry("400x300")
    root.title("sCTkSelector Test")
    root.protocol("WM_DELETE_WINDOW", on_close)

    result = []

    items=["vw", "porsche", "roadster", "tesla"]

    # 1. Embed the Selector frame
    theSelector = Selector(root, items=items, multiple_choices=True)
    theSelector.pack(expand=True, fill="both", padx=10, pady=10)

    # 2. Add a Confirm/OK button
    confirm_btn = sCTkButtonPrimary(root, text="Confirm", command=on_confirm)
    confirm_btn.pack(pady=(0, 10))

    root.mainloop()



