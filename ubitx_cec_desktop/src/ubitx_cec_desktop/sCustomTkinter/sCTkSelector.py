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
    def __init__(self, master, items: Optional[list[str]] = None, multiple_choices=True, **kwargs):
        """Selector widgets to select options in a list of options.
        Includes a search bar to find different elements faster.
        """
        # 1. SANITIZE RUNTIME ARGUMENTS: Strip unmanaged properties out of kwargs immediately
        # This completely shields the parent CTkFrame from invalid keyword errors on startup
        state_init = kwargs.pop("state", "normal")
        pack_prop_init = kwargs.pop("pack_propagate", None)
        grid_prop_init = kwargs.pop("grid_propagate", None)

        # 2. MERGE THEMES: Initialize ThemeableWidget safely using the cleaned kwargs dictionary
        theme_config = THEME_DEFAULTS.get("sCTkSelector", {})

        # FIXED: Store dictionary references safely onto instance memory BEFORE configure runs
        self._local_defaults = theme_config
        self._custom_disabled_map = theme_config.get("disabled_map", {})

        ThemeableWidget.__init__(self, theme_config, kwargs)

        fg_color = self.final_kw.get("fg_color", "transparent")

        # # 3. LEAN PURGE: Remove only custom behavioral parameters from self.final_kw
        # # just in case they were pulled out of the THEME_DEFAULTS config dictionary.
        # # (No need to pop items or multiple_choices here since they were never in the theme files!)
        # self.final_kw.pop("state", None)
        # self.final_kw.pop("pack_propagate", None)
        # self.final_kw.pop("grid_propagate", None)

        # 4. Call the parent sCTkFrame constructor safely
        super().__init__(master, **self.final_kw)

        self.search_var = ctk.StringVar(self)
        self.search_var.trace_add("write", self._search_modified)

        self.search_bar = sCTkEntryPrimary(self, textvariable=self.search_var)
        self.checkboxes_frame = sCTkScrollableFrame(self, fg_color=fg_color)

        self.search_bar.pack(anchor="n", fill="x")
        self.checkboxes_frame.pack(expand=True, fill="both", side="bottom")

        # LAYER 1 PROPAGATION GUARD: Target the private native frame inside the scrollable container
        self.checkboxes_frame._parent_frame.pack_propagate(False)
        self.checkboxes_frame._parent_frame.grid_propagate(False)

        self.checkboxes = []
        self.selected_indexes = []
        self.multiple_choices = multiple_choices
        self.state = "normal"

        if items is None:
            items = []

        # 5. Route variables into the configure parser loop for execution mapping
        self.configure(
            items=items,
            multiple_choices=multiple_choices,
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

        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Satisfies Pygubu Inspector panel queries)
        # -----------------------------------------------------------------
        # If Pygubu passes a single positional string, intercept and return the meta-tuple
        if cnf is not None and not kwargs and isinstance(cnf, str):
            pname = cnf
            if pname == "state":
                return ("state", "state", "state", "normal", str(getattr(self, "state", "normal")))
            if pname == "multiple_choices":
                return ("multiple_choices", "multiple_choices", "multiple_choices", "True", str(self.multiple_choices))
            if pname == "items":
                # Returns the current checklist text elements as a string format
                current_items = [cb.cget("text") for cb in self.checkboxes] if hasattr(self, "checkboxes") else []
                return ("items", "items", "items", "[]", str(current_items))
            if pname in ["pack_propagate", "grid_propagate"]:
                return (pname, pname, pname, "None", str(getattr(self, f"_{pname}_val", None)))
            if pname in ["fg_color", "border_color", "text_color"]:
                current_state = str(getattr(self, "state", "normal")).lower()
                if current_state == "disabled" and self._widget_disabled_map:
                    val = self._widget_disabled_map.get(pname)
                else:
                    val = self._local_defaults.get(pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            return super().configure(cnf)

        # Handle Pygubu dictionary-style passes or unify arguments into standard kwargs
        if isinstance(cnf, dict):
            kwargs.update(cnf)

        # -----------------------------------------------------------------
        # ZONE B: SANITIZATION INTERCEPTOR (Your Precise Checkbox & Option Physics)
        # -----------------------------------------------------------------
        # 1. Intercept and route list modifications cleanly
        if "items" in kwargs:
            items_val = kwargs.pop("items")

            # Handle empty/cleared field erasures from Pygubu gracefully
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

        if "multiple_choices" in kwargs:
            mult_val = kwargs.pop("multiple_choices")
            if mult_val == "" or mult_val is None:
                mult_val = True
            elif isinstance(mult_val, str):
                mult_val = str(mult_val).lower() in ['true', '1', 'yes']
            self.multiple_choices = mult_val

        # 2. Intercept and apply the state configuration property with your disabled_map theme settings
        if "state" in kwargs:
            target_state = kwargs.pop("state")
            if target_state == "" or target_state is None:
                target_state = "normal"
            else:
                target_state = str(target_state).lower()

            if target_state in ("normal", "disabled"):
                self.state = target_state
                disabled_text_color = self._widget_disabled_map.get("text_color", None)

                if hasattr(self, "search_bar"):
                    self.search_bar.configure(state=self.state)
                    if self.state == "disabled" and disabled_text_color:
                        self.search_bar.configure(text_color=disabled_text_color)
                    elif self.state == "normal":
                        # FIXED: Extract text color parameters directly from the inner
                        # text component's local defaults instead of the parent composite frame!
                        # This enforces a hard stop crash if the theme file configuration is broken.
                        entry_defaults = THEME_DEFAULTS.get("sCTkEntryPrimary", {})
                        self.search_bar.configure(text_color=entry_defaults["text_color"])

                if hasattr(self, "checkboxes"):
                    for checkbox in self.checkboxes:
                        checkbox.configure(state=self.state)
                        if self.state == "disabled" and disabled_text_color:
                            checkbox.configure(text_color=disabled_text_color)
                        elif self.state == "normal":
                            # FIXED: Pull text parameters directly out of the core checkbox configuration
                            cb_defaults = THEME_DEFAULTS.get("sCTkCheckBox", {})
                            checkbox.configure(text_color=cb_defaults["text_color"])

        # 3. Safely pop custom propagation fields out before they hit ThemeableWidget parsing
        pack_prop_val = kwargs.pop("pack_propagate", None)
        grid_prop_val = kwargs.pop("grid_propagate", None)

        # Save structural tracking configurations for Pygubu queries
        if pack_prop_val is not None and pack_prop_val != "":
            setattr(self, "_pack_propagate_val", str(pack_prop_val).lower() in ['true', '1', 'yes'])
        if grid_prop_val is not None and grid_prop_val != "":
            setattr(self, "_grid_propagate_val", str(grid_prop_val).lower() in ['true', '1', 'yes'])

        # 4. FIXED: Instead of re-running ThemeableWidget.__init__ (which clears out your theme maps),
        # selectively update the existing local final_kw configuration dictionary!
        for k, v in list(kwargs.items()):
            if k in self._local_defaults:
                self.final_kw[k] = kwargs.pop(k)

        if "fg_color" in self.final_kw:
            new_fg = self.final_kw.get("fg_color")
            if hasattr(self, "checkboxes_frame"):
                self.checkboxes_frame.configure(fg_color=new_fg)


        # 5. Resolve layout sizing and fallback default constraints dynamically
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

        # 6. ✅ CRITICAL LEAN CLEANUP STEP:
        # Scrub unmapped layout tokens entirely before passing remaining standard dictionary elements downstream
        self.final_kw.pop("pack_propagate", None)
        self.final_kw.pop("grid_propagate", None)
        self.final_kw.pop("state", None)

        # Route standard remaining layout tokens safely to the frame constructor pass
        # Clean out any leftover empty string keyword values to prevent Tkinter validation crashes
        for k, v in list(kwargs.items()):
            if v == "":
                kwargs.pop(k)

        return super().configure(**kwargs)

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
        print(theSelector.get_selections())

    def on_close():
        print(theSelector.get_selections())
        root.destroy()

    root = ctk.CTk()
    root.geometry("400x350")
    root.title("sCTkSelector Test")
    root.protocol("WM_DELETE_WINDOW", on_close)

    result = []
    items = ["vw", "porsche", "roadster", "tesla"]

    theSelector = sCTkSelector(root, items=items, multiple_choices=True)
    theSelector.pack(expand=True, fill="both", padx=10, pady=10)

    confirm_btn = sCTkButtonPrimary(root, text="Confirm", command=on_confirm)
    confirm_btn.pack(pady=(0, 10))

    root.mainloop()
