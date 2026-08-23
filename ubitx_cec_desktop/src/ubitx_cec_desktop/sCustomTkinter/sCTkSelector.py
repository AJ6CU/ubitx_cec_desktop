#!/usr/bin/python3
"""
sCTkSelector - Part 1: Core Initialization & Item Filtering

An advanced theme-compliant, scrollable option tree selector widget.
Pairs an optional high-contrast search field lane with a dynamic listing frame card
to manage multi-state checkbox row configurations natively.

Derived from Selector class by Fastattack, 2024.
Source Repository: MoreCustomTkinterWidgets
"""
import customtkinter as ctk
import ast
from typing import Optional, Union, Tuple
from ThemeableWidget import ThemeableWidget

# Framework-compliant component imports
from sCTkFrame import sCTkFrame
from sCTkCheckBox import sCTkCheckBox
from sCTkEntryPrimary import sCTkEntryPrimary
from sCTkScrollableFrame import sCTkScrollableFrame


class sCTkSelector(sCTkFrame, ThemeableWidget):
    def __init__(self, master, items: Optional[list[str]] = None, multiple_choices=True, searchBox=True, **kwargs):
        """Selector widgets to select options in a list of options.
        Includes an optional search bar to find different elements faster.
        """
        # 1. SANITIZE RUNTIME ARGUMENTS: Strip unmanaged properties out immediately
        state_init = kwargs.pop("state", "normal")
        pack_prop_init = kwargs.pop("pack_propagate", None)
        grid_prop_init = kwargs.pop("grid_propagate", None)

        # 2. ENFORCE SYSTEM REGISTRY INTERACTION:
        # Pass kwargs cleanly to the theme mixin to engage the name-introspection pipeline natively.
        ThemeableWidget.__init__(self, kwargs)

        # 🛠️ THE MUTATION SAFEGUARD DEEP COPY SHIELD:
        self._local_defaults = dict(self.final_kw)
        self._custom_disabled_map = dict(self._widget_disabled_map)

        fg_color = self._local_defaults.get("fg_color", "transparent")

        # 3. Call the parent sCTkFrame constructor safely
        super().__init__(master, **self.final_kw)

        self._state = "normal"
        self.search_var = ctk.StringVar(self)
        self.search_var.trace_add("write", self._search_modified)

        # Initialize internal reference variables early to support configuration tracking
        self.search_bar = None
        self._search_box_visible = bool(searchBox)

        # Construct the scroll backplane chassis frame first
        self.checkboxes_frame = sCTkScrollableFrame(self, fg_color=fg_color)
        self.checkboxes_frame.pack(expand=True, fill="both", side="bottom")

        # LAYER 1 PROPAGATION GUARD: Target the private native frame inside the scrollable container
        if hasattr(self.checkboxes_frame, "_parent_frame") and self.checkboxes_frame._parent_frame is not None:
            self.checkboxes_frame._parent_frame.pack_propagate(False)
            self.checkboxes_frame._parent_frame.grid_propagate(False)

        self.checkboxes = []
        self.selected_indexes = []
        self.multiple_choices = multiple_choices

        if items is None:
            items = []

        # 4. Route variables into the configure parser loop for execution mapping
        self.configure(
            items=items,
            multiple_choices=multiple_choices,
            searchBox=self._search_box_visible,
            pack_propagate=pack_prop_init,
            grid_propagate=grid_prop_init,
            state=state_init
        )

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
                        if i < len(self.checkboxes):
                            self.checkboxes[i].deselect()
                    self.selected_indexes.clear()
                    self.selected_indexes.append(index)
                else:
                    self.selected_indexes.append(index)

    def _reset_scroll(self):
        """ Internal method: scrolls back to the starting position """
        if hasattr(self.checkboxes_frame, "_parent_canvas") and self.checkboxes_frame._parent_canvas is not None:
            self.checkboxes_frame._parent_canvas.yview_moveto(0)

    def _search_modified(self, *args):
        """ Internal method: modifies the search based on prefix constraints """
        value = self.search_var.get()
        row = 0
        for x in range(len(self.checkboxes)):
            if self.checkboxes[x].cget("text").startswith(value):
                self.checkboxes[x].grid(row=row, column=0, padx=3, pady=3, sticky="w")
                row += 1
            else:
                self.checkboxes[x].grid_forget()
        self._reset_scroll()

    def get_all_items(self) -> list:
        """ Returns all the items in the selector """
        return [checkbox.cget("text") for checkbox in self.checkboxes]

    def configure(self, cnf=None, **kwargs):
        """Processes both custom widget collections and standard frame attributes safely."""
        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Feeds values to Pygubu Inspector)
        # -----------------------------------------------------------------
        if cnf is not None and not kwargs and isinstance(cnf, str):
            pname = cnf
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))
            if pname == "multiple_choices":
                return ("multiple_choices", "multiple_choices", "multiple_choices", "True", str(self.multiple_choices))
            if pname == "searchBox":
                return ("searchBox", "searchBox", "searchBox", "True", str(self._search_box_visible))
            if pname == "items":
                current_items = [cb.cget("text") for cb in self.checkboxes] if hasattr(self, "checkboxes") else []
                return ("items", "items", "items", "[]", str(current_items))
            if pname in ["pack_propagate", "grid_propagate"]:
                return (pname, pname, pname, "None", str(getattr(self, f"_{pname}_val", None)))
            if pname in ["fg_color", "border_color", "text_color"]:
                current_state = str(self.state()).lower()
                val = self._custom_disabled_map.get(pname) if current_state == "disabled" else self._local_defaults.get(
                    pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))
            return super().configure(cnf)

        if isinstance(cnf, dict):
            kwargs = cnf | kwargs

        # -----------------------------------------------------------------
        # ZONE B: SANITIZATION INTERCEPTOR
        # -----------------------------------------------------------------
        if "items" in kwargs:
            items_val = kwargs.pop("items")
            if items_val == "" or items_val is None:
                items_val = []
            elif isinstance(items_val, str):
                try:
                    items_val = ast.literal_eval(items_val)
                except Exception:
                    items_val = []

            if items_val is not None:
                if len(set(items_val)) == len(items_val):
                    for checkbox in self.checkboxes:
                        checkbox.destroy()
                    self.checkboxes.clear()
                    self.selected_indexes.clear()

                    for index in range(len(items_val)):
                        self.checkboxes.append(sCTkCheckBox(
                            self.checkboxes_frame,
                            text=items_val[index],
                            command=lambda a=index: self._selection(a)
                        ))
                    self._search_modified()
                else:
                    raise ValueError("There is two times or more the same item in the given items list")

        if "searchBox" in kwargs:
            sb_val = kwargs.pop("searchBox")
            if sb_val == "" or sb_val is None:
                sb_val = True
            elif isinstance(sb_val, str):
                sb_val = str(sb_val).lower() in ['true', '1', 'yes']

            self._search_box_visible = sb_val
            if self._search_box_visible:
                if not hasattr(self, "search_bar") or self.search_bar is None:
                    self.search_bar = sCTkEntryPrimary(self, textvariable=self.search_var)

                # 🛠️ THE REVERSED PACKING STACK MATRIX RESOLUTION:
                # We strip 'before=' entirely to eliminate TclError exceptions.
                # We mount the search bar cleanly, then cycle the scroll frame to the bottom index!
                self.search_bar.pack(anchor="n", fill="x")

                if hasattr(self, "checkboxes_frame") and self.checkboxes_frame is not None:
                    self.checkboxes_frame.pack_forget()
                    self.checkboxes_frame.pack(expand=True, fill="both", side="bottom")

                if self._state == "disabled" and self.search_bar is not None:
                    self.search_bar.configure(state="disabled")
            else:
                if hasattr(self, "search_bar") and self.search_bar is not None:
                    self.search_bar.pack_forget()

        if "multiple_choices" in kwargs:
            mult_val = kwargs.pop("multiple_choices")
            if mult_val == "" or mult_val is None:
                mult_val = True
            elif isinstance(mult_val, str):
                mult_val = str(mult_val).lower() in ['true', '1', 'yes']
            self.multiple_choices = mult_val

        if "state" in kwargs:
            self.state(kwargs.pop("state"))

        pack_prop_val = kwargs.pop("pack_propagate", None)
        grid_prop_val = kwargs.pop("grid_propagate", None)

        if pack_prop_val is not None and pack_prop_val != "":
            setattr(self, "_pack_propagate_val", str(pack_prop_val).lower() in ['true', '1', 'yes'])
        if grid_prop_val is not None and grid_prop_val != "":
            setattr(self, "_grid_propagate_val", str(grid_prop_val).lower() in ['true', '1', 'yes'])

        for k, v in list(kwargs.items()):
            if k in self._local_defaults:
                self.final_kw[k] = kwargs.pop(k)

        if "fg_color" in self.final_kw:
            new_fg = self.final_kw.get("fg_color")
            if hasattr(self, "checkboxes_frame"):
                self.checkboxes_frame.configure(fg_color=new_fg)

        w_val = int(self.final_kw.get("width", 0))
        h_val = int(self.final_kw.get("height", 0))

        if w_val > 0 or h_val > 0:
            use_pack_p = pack_prop_val if pack_prop_val is not None else getattr(self, "_pack_propagate_val", False)
            use_grid_p = grid_prop_val if grid_prop_val is not None else getattr(self, "_grid_propagate_val", False)
        else:
            self.final_kw["width"] = 200
            self.final_kw["height"] = 150
            use_pack_p = pack_prop_val if pack_prop_val is not None else getattr(self, "_pack_propagate_val", True)
            use_grid_p = grid_prop_val if grid_prop_val is not None else getattr(self, "_grid_propagate_val", True)

        if isinstance(use_pack_p, str): use_pack_p = use_pack_p.lower() in ['true', '1', 'yes']
        if isinstance(use_grid_p, str): use_grid_p = use_grid_p.lower() in ['true', '1', 'yes']

        if use_pack_p is not None: self.pack_propagate(use_pack_p)
        if use_grid_p is not None: self.grid_propagate(use_grid_p)

        if hasattr(self, "checkboxes_frame") and hasattr(self.checkboxes_frame, "_parent_frame"):
            if use_pack_p is not None: self.checkboxes_frame._parent_frame.pack_propagate(use_pack_p)
            if use_grid_p is not None: self.checkboxes_frame._parent_frame.grid_propagate(use_grid_p)

        self.final_kw.pop("pack_propagate", None)
        self.final_kw.pop("grid_propagate", None)
        self.final_kw.pop("state", None)

        for k, v in list(kwargs.items()):
            if v == "":
                kwargs.pop(k)

        if kwargs:
            return super().configure(**kwargs)
        return None

    config = configure

    def clear_selections(self):
        """ Clears the selections """
        for index in self.selected_indexes:
            if index < len(self.checkboxes):
                self.checkboxes[index].deselect()
        self.selected_indexes.clear()

    def get_selections(self) -> list:
        """Returns the selected items"""
        return [self.checkboxes[index].cget("text") for index in self.selected_indexes if index < len(self.checkboxes)]

    def get_state(self) -> str:
        """Explicit getter returning the current operational state safely."""
        return self.state()

    def state(self, mode: str = None) -> str:
        """Dedicated polymorphic state manager syncing search input fields and checklist grids."""
        if mode is None:
            return str(getattr(self, "_state", "normal")).lower()

        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            self._state = "normal"
            if hasattr(self, "search_bar") and self.search_bar is not None:
                self.search_bar.configure(state="normal")
            if hasattr(self, "checkboxes_frame") and self.checkboxes_frame is not None:
                self.checkboxes_frame.configure(state="normal")
            if hasattr(self, "checkboxes"):
                for cb in self.checkboxes: cb.configure(state="normal")
        elif mode == "disabled":
            self._state = "disabled"
            if hasattr(self, "search_bar") and self.search_bar is not None:
                self.search_bar.configure(state="disabled")
            if hasattr(self, "checkboxes_frame") and self.checkboxes_frame is not None:
                self.checkboxes_frame.configure(state="disabled")
            if hasattr(self, "checkboxes"):
                for cb in self.checkboxes: cb.configure(state="disabled")
        return self._state

# =====================================================================
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import sCTkThemes
from sCTkButtonPrimary import sCTkButtonPrimary

if __name__ == "__main__":
    def on_confirm():
        print(f"Active Selection Telemetry Array: {theSelector.get_selections()}")


    root = ctk.CTk()
    root.geometry("200x380")
    root.title("sCTkSelector Validation Bench")

    sCTkThemes.apply_sCTkThemes()

    items = ["vw", "porsche", "roadster", "tesla", "ferrari", "mclaren"]

    #
    # Test of adding search field after creation
    #
    # theSelector = sCTkSelector(root, items=items, multiple_choices=True, searchBox=False)
    # theSelector.configure(searchBox=True)

    #
    #   Test of deletion of search box after creation
    #

    # theSelector = sCTkSelector(root, items=items, multiple_choices=True, searchBox=True)
    # theSelector.configure(searchBox=False)

    #
    #   Normal case
    #
    theSelector = sCTkSelector(root, items=items, multiple_choices=True)

    theSelector.pack(expand=True, fill="both", padx=15, pady=15)

    confirm_btn = sCTkButtonPrimary(root, text="Confirm Selections", command=on_confirm)
    confirm_btn.pack(pady=(0, 15))

    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    theSelector.state("disabled")
    print("state (Disabled Pass) =", theSelector.get_state())  # Output: disabled
    theSelector.state("normal")
    print("state (Normal Pass)   =", theSelector.get_state())  # Output: normal
    print("========================================\n")

    # theSelector.configure(searchBox=True)

    root.mainloop()
