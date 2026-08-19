import customtkinter as ctk
from typing import List, Optional, Callable, Any, Literal
from sCTkThemes import THEME_DEFAULTS
from sCTkLabelPrimary import sCTkLabelPrimary
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkScrollableFrame import sCTkScrollableFrame
from ThemeableWidget import ThemeableWidget


class sCTkTableview(sCTkScrollableFrame):
    def __init__(self, master: any, columns: Optional[Any] = None, width: int = 500, height: int = 300,
                 grid_mode: Literal["zebra", "grid", "none"] = "zebra", header_line_width: int = 2,
                 outline_width: float = 1.0, outline_radius: int = 4, state: Literal["normal", "disabled"] = "normal",
                 num_columns: int = 3, num_rows: int = 1, show_headers: Any = True,
                 cell_bg_color: Optional[Any] = None, cell_alt_bg_color: Optional[Any] = None, *args, **kwargs):

        theme_config = THEME_DEFAULTS.get("sCTkTableview", THEME_DEFAULTS.get("sCTkTableView", {}))

        # 1. BIND OBJECT SCOPE EARLY
        self._local_defaults = theme_config
        self._custom_disabled_map = theme_config.get("disabled_map", {})

        # 2. RUN SHARED THEME LOGIC FIRST: Populates self.final_kw and strips disabled sub-dicts
        ThemeableWidget.__init__(self, theme_config, kwargs)

        # 3. LEAN PURGE: Remove unmapped behavioral tokens from self.final_kw
        # Shields the parent sCTkScrollableFrame class initialization layers
        self.final_kw.pop("state", None)
        self.final_kw.pop("grid_mode", None)
        self.final_kw.pop("show_headers", None)
        self.final_kw.pop("num_rows", None)
        self.final_kw.pop("num_columns", None)

        # 4. ASSIGN LOCAL THEME METRICS (Will strictly raise a KeyError hard stop if broken inside themes!)
        self._header_bg = self.final_kw["header_bg_color"]
        self._header_fg = self.final_kw["header_text_color"]
        self._header_font = self.final_kw["header_font"]

        self._cell_bg = cell_bg_color if cell_bg_color is not None else self.final_kw["cell_bg_color"]
        self._cell_alt_bg = cell_alt_bg_color if cell_alt_bg_color is not None else self.final_kw["cell_alt_bg_color"]
        self._cell_fg = self.final_kw["cell_text_color"]
        self._cell_font = self.final_kw["cell_font"]
        self._grid_line_color = self.final_kw["grid_line_color"]

        # 5. INITIALIZE TRACKING FIELDS
        self._grid_mode = str(grid_mode).replace("'", "").replace('"', "").strip().lower()
        self._header_line_width = int(header_line_width) if header_line_width is not None else 2
        self._outline_width = float(outline_width) if outline_width else 1.0
        self._outline_radius = int(outline_radius) if outline_radius else 4
        self._state = state

        self._num_columns = int(num_columns)
        self._num_rows = int(num_rows)
        self._show_headers = str(show_headers).replace("'", "").replace('"', "").strip().lower() in ("true", "1", "yes")

        self._data_matrix, self._cell_widgets, self._header_widgets = [], [], []
        kwargs["border_width"], kwargs["corner_radius"], kwargs["scrollbar_fg_color"] = 0, 0, self._cell_bg

        # 6. INITIALIZE NATIVE BASE LAYER (Passes pure remaining keyword keys down cleanly)
        super().__init__(master=master, width=width, height=height, *args, **kwargs)
        super().configure(border_width=0, corner_radius=0, fg_color=self._cell_bg)

        # ... (The rest of your widget packing and layout generation logic remains completely untouched below) ...
        self.table_outline_frame = ctk.CTkFrame(self, fg_color=self._grid_line_color, border_width=self._outline_width,
                                                border_color=self._grid_line_color, corner_radius=self._outline_radius)
        self.table_outline_frame.grid(row=0, column=0, sticky="nw", padx=1, pady=1)

        if isinstance(columns, str):
            clean_str = columns.replace("'", "").replace('"', "").strip()
            columns = [c.strip() for c in clean_str.split(',') if c.strip()]

        if columns and isinstance(columns, list) and len(columns) > 0:
            self.columns_list = list(columns)
        else:
            self.columns_list = [""] * self._num_columns

        self._column_widths = [120] * self._num_columns
        self._column_anchors = ["center"] * self._num_columns
        self._click_callback, self._edit_callback, self._validation_callback = None, None, None

        self._create_header_bar()
        self.load_dataset([[""] * self._num_columns for _ in range(self._num_rows)])

        # Defer initial state to your configure loop so it sets the grid components to 'disabled' on launch if requested
        self.configure(state=state)

    def _create_header_bar(self):
        for w in self._header_widgets:
            try:
                w.destroy()
            except Exception:
                pass
        self._header_widgets = []
        if hasattr(self, "header_separator") and self.header_separator:
            try:
                self.header_separator.destroy()
            except Exception:
                pass
        self.header_separator = None

        if not self._show_headers:
            return

        is_none_mode = (self._grid_mode == "none")
        gap_size = 0 if is_none_mode else 1
        edge_size = 0 if is_none_mode else 2

        if self._header_line_width > 0:
            self.header_separator = ctk.CTkFrame(self.table_outline_frame, height=self._header_line_width,
                                                 fg_color=self._grid_line_color, corner_radius=0)
            self.header_separator.grid(row=1, column=0, columnspan=self._num_columns, sticky="ew",
                                       padx=(edge_size, edge_size + gap_size), pady=(0, edge_size))

        render_labels = list(self.columns_list)
        if len(render_labels) < self._num_columns:
            render_labels += [""] * (self._num_columns - len(render_labels))
        elif len(render_labels) > self._num_columns:
            render_labels = render_labels[:self._num_columns]

        for col_idx, col_name in enumerate(render_labels):
            w_limit = self._column_widths[col_idx] if col_idx < len(self._column_widths) else 120
            header_cell = sCTkLabelPrimary(self.table_outline_frame, text=col_name, font=self._header_font,
                                           text_color=self._header_fg, fg_color=self._header_bg, corner_radius=0,
                                           height=28, width=w_limit)

            left_pad = edge_size if col_idx == 0 else gap_size
            right_pad = edge_size if col_idx == len(render_labels) - 1 else 0
            header_cell.grid(row=0, column=col_idx, sticky="ew", padx=(left_pad, right_pad), pady=(edge_size, 0))
            self.table_outline_frame.grid_columnconfigure(col_idx, weight=0)

            try:
                header_cell.lift()
            except Exception:
                pass
            self._header_widgets.append(header_cell)

    def load_dataset(self, dataset: List[List[Any]]):
        for cell in [c for row in self._cell_widgets for c in row]: cell.destroy()
        self._data_matrix, self._cell_widgets = [list(row) for row in dataset], []
        super().configure(width=0, height=0)

        # 🚀 SAFE SEAM ROW STITCHER:
        # If headers are visible but the divider line is 0, row 1 is completely empty.
        # If grid_mode is 'none', we dynamically push the cells up into row_offset = 1
        # to close the 1-pixel gap cleanly without using illegal negative padding values!
        if self._show_headers:
            row_offset = 1 if (self._grid_mode == "none" and self._header_line_width == 0) else 2
        else:
            row_offset = 0

        is_none_mode = (self._grid_mode == "none")
        gap_size = 0 if is_none_mode else 1
        edge_size = 0 if is_none_mode else 2

        for r_idx, r_data in enumerate(self._data_matrix):
            if len(r_data) < self._num_columns:
                r_data += [""] * (self._num_columns - len(r_data))
                self._data_matrix[r_idx] = r_data
            elif len(r_data) > self._num_columns:
                r_data = r_data[:self._num_columns]
                self._data_matrix[r_idx] = r_data

            current_row_bg = self._cell_alt_bg if (self._grid_mode == "zebra" and r_idx % 2 != 0) else self._cell_bg
            r_cells = []
            for c_idx in range(self._num_columns):
                val = r_data[c_idx]
                w_limit = self._column_widths[c_idx] if c_idx < len(self._column_widths) else 120
                h_limit = 26
                txt_anchor = self._column_anchors[c_idx] if c_idx < len(self._column_anchors) else "center"
                display_val = "    " + str(val) if txt_anchor == "w" else (
                    str(val) + "    " if txt_anchor == "e" else str(val))

                cell_label = sCTkLabelSecondary(self.table_outline_frame, text=display_val, font=self._cell_font,
                                                text_color=self._cell_fg, width=w_limit, height=h_limit,
                                                corner_radius=0, anchor=txt_anchor, fg_color="transparent")
                cell_label.configure(fg_color=current_row_bg)

                if self._state == "disabled":
                    cell_label.configure(state="disabled")

                # All grid padding integers remain explicitly positive or zero to prevent TclErrors
                top_pad = edge_size if r_idx == 0 else gap_size
                bot_pad = edge_size if r_idx == len(self._data_matrix) - 1 else 0
                left_pad = edge_size if c_idx == 0 else gap_size
                right_pad = edge_size if c_idx == self._num_columns - 1 else 0

                cell_label.grid(row=r_idx + row_offset, column=c_idx, sticky="ew", padx=(left_pad, right_pad),
                                pady=(top_pad, bot_pad))

                cell_label.bind("<Button-1>", lambda e, r=r_idx: self._click_callback(r, self._data_matrix[r]) if (
                            self._click_callback and self._state == "normal") else None)
                cell_label.bind("<Double-Button-1>", lambda e, r=r_idx, c=c_idx: self._spawn_editor(r,
                                                                                                    c) if self._state == "normal" else None)
                r_cells.append(cell_label)
            self._cell_widgets.append(r_cells)

        for hw in self._header_widgets:
            try:
                hw.lift()
            except Exception:
                pass
        if hasattr(self, "header_separator") and self.header_separator:
            try:
                self.header_separator.lift()
            except Exception:
                pass

        self.update_idletasks()
        super().configure(width=self.table_outline_frame.winfo_reqwidth() + 14,
                          height=self.table_outline_frame.winfo_reqheight() + 18)

    def _spawn_editor(self, r_idx: int, c_idx: int):
        if self._show_headers:
            row_offset = 1 if (self._grid_mode == "none" and self._header_line_width == 0) else 2
        else:
            row_offset = 0

        entry = ctk.CTkEntry(self.table_outline_frame, font=self._cell_font, width=self._column_widths[c_idx],
                             height=24, corner_radius=0)
        entry.insert(0, str(self._data_matrix[r_idx][c_idx]))
        entry.grid(row=r_idx + row_offset, column=c_idx, sticky="ew", padx=1, pady=1)
        entry.focus_set()
        entry.select_range(0, "end")
        entry.bind("<Return>", lambda e: self._save_edit(r_idx, c_idx, entry))
        entry.bind("<FocusOut>", lambda e: self._save_edit(r_idx, c_idx, entry))

    def _save_edit(self, r_idx: int, c_idx: int, entry: ctk.CTkEntry):
        if not entry.winfo_exists(): return
        val = entry.get()
        entry.destroy()
        if self._validation_callback and not self._validation_callback(c_idx, val): val = self._data_matrix[r_idx][
            c_idx]

        self._data_matrix[r_idx][c_idx] = val
        txt_anchor = self._column_anchors[c_idx]
        display_val = "    " + str(val) if txt_anchor == "w" else (str(val) + "    " if txt_anchor == "e" else str(val))

        self._cell_widgets[r_idx][c_idx].configure(text=display_val)
        if self._edit_callback and self._data_matrix[r_idx][c_idx] == val: self._edit_callback(r_idx, c_idx, val)

    def configure(self, require_redraw=False, **kwargs):
        """Processes Pygubu designer workspace queries and manages composite state updates."""

        # ZONE A: POSITION INTERCEPT (Pygubu Inspector compatibility check)
        if require_redraw is not None and not kwargs and isinstance(require_redraw, str):
            pname = require_redraw
            mapping = {
                "state": ("state", "state", "state", "normal", str(getattr(self, "_state", "normal"))),
                "grid_mode": ("grid_mode", "grid_mode", "grid_mode", "zebra",
                              str(getattr(self, "_grid_mode", "zebra"))),
                "show_headers": ("show_headers", "show_headers", "show_headers", "True",
                                 str(getattr(self, "_show_headers", True)))
            }
            if pname in mapping:
                return mapping[pname]
            if pname in ["num_columns", "num_rows", "header_line_width"]:
                return (pname, pname, pname, "0", str(getattr(self, f"_{pname}", 0)))

            return super().configure(require_redraw)

        if isinstance(require_redraw, dict):
            kwargs.update(require_redraw)
            require_redraw = False

        rebuild_layout = False

        # ZONE B: SANITIZATION & LAYOUT MODIFICATIONS
        if "cell_bg_color" in kwargs:
            self._cell_bg = kwargs.pop("cell_bg_color")
            rebuild_layout = True

        if "cell_alt_bg_color" in kwargs:
            self._cell_alt_bg = kwargs.pop("cell_alt_bg_color")
            rebuild_layout = True

        if "num_columns" in kwargs:
            self._num_columns = int(kwargs.pop("num_columns"))
            rebuild_layout = True

        if "num_rows" in kwargs:
            self._num_rows = int(kwargs.pop("num_rows"))
            rebuild_layout = True

        if "show_headers" in kwargs:
            val = kwargs.pop("show_headers")
            self._show_headers = val if isinstance(val, bool) else (str(val).lower() in ("true", "1", "yes"))
            rebuild_layout = True
        if "grid_mode" in kwargs:
            self._grid_mode = str(kwargs.pop("grid_mode") or "zebra").replace("'", "").replace('"', "").strip().lower()
            rebuild_layout = True
        if "header_line_width" in kwargs:
            self._header_line_width = int(kwargs.pop("header_line_width"))
            rebuild_layout = True

        if "outline_width" in kwargs:
            self._outline_width = float(kwargs.pop("outline_width"))
            if hasattr(self, "table_outline_frame"):
                self.table_outline_frame.configure(border_width=self._outline_width)
        if "outline_radius" in kwargs:
            self._outline_radius = int(kwargs.pop("outline_radius"))
            if hasattr(self, "table_outline_frame"):
                self.table_outline_frame.configure(corner_radius=self._outline_radius)

        if "columns" in kwargs or "columns_list" in kwargs or rebuild_layout:
            raw_cols = kwargs.pop("columns", kwargs.pop("columns_list", None))
            if isinstance(raw_cols, str):
                raw_cols = [c.strip() for c in raw_cols.split(',') if c.strip()]

            if raw_cols and len(raw_cols) > 0:
                self.columns_list = list(raw_cols)
            elif not hasattr(self, "columns_list") or not self.columns_list:
                self.columns_list = [""] * self._num_columns

            if len(self._column_widths) < self._num_columns:
                self._column_widths += [120] * (self._num_columns - len(self._column_widths))
                self._column_anchors += ["center"] * (self._num_columns - len(self._column_anchors))
            elif len(self._column_widths) > self._num_columns:
                self._column_widths = self._column_widths[:self._num_columns]
                self._column_anchors = self._column_anchors[:self._num_columns]

            self._create_header_bar()

            target_rows = len(self._data_matrix) if (
                    hasattr(self, "_data_matrix") and len(self._data_matrix) > 0) else self._num_rows
            if target_rows < self._num_rows:
                target_rows = self._num_rows

            self.load_dataset([[""] * self._num_columns for _ in range(target_rows)])

        # -----------------------------------------------------------------
        # ZONE C: STATE CONTROLLER MANAGEMENT (Cascades state to cells & parent layout)
        # -----------------------------------------------------------------
        if "state" in kwargs:
            # Safely capture state string variable continuously across all execution rings
            self._state = str(kwargs.get("state")).lower()

            # Pulls the master table dictionary block directly to preserve your hard-stops!
            table_theme = THEME_DEFAULTS.get("sCTkTableview", THEME_DEFAULTS.get("sCTkTableView", {}))
            theme_primary = THEME_DEFAULTS["sCTkLabelPrimary"]
            theme_secondary = THEME_DEFAULTS["sCTkLabelSecondary"]

            if self._state == "disabled":
                # Swap internal rendering flags to match your disabled styling profiles
                # Strictly references keys without soft defaults to force a hard stop if broken!
                self._header_bg = theme_primary.get("disabled_map", {}).get("fg_color") or table_theme[
                    "header_bg_color"]
                self._header_fg = theme_primary["disabled_map"]["text_color"]

                self._cell_bg = theme_secondary.get("disabled_map", {}).get("fg_color") or table_theme["cell_bg_color"]
                self._cell_alt_bg = theme_secondary.get("disabled_map", {}).get("fg_color") or table_theme[
                    "cell_alt_bg_color"]
                self._cell_fg = theme_secondary["disabled_map"]["text_color"]

                if "grid_line_color" in table_theme:
                    disabled_map = table_theme.get("disabled_map", {})
                    self._grid_line_color = disabled_map.get("grid_line_color") or table_theme["grid_line_color"]
            else:
                # Revert completely back to your pure operational table database values
                self._header_bg = table_theme["header_bg_color"]
                self._header_fg = table_theme["header_text_color"]
                self._cell_bg = table_theme["cell_bg_color"]
                self._cell_alt_bg = table_theme["cell_alt_bg_color"]
                self._cell_fg = table_theme["cell_text_color"]
                self._grid_line_color = table_theme["grid_line_color"]

            # 1. SAFE TIMING FILTER: Update outline and grid borders safely without rebuilding fonts
            if hasattr(self, "table_outline_frame") and self.table_outline_frame:
                self.table_outline_frame.configure(fg_color=self._grid_line_color, border_color=self._grid_line_color)

            # 2. FIXED: Cascade parameters to the separate header widgets array list!
            if hasattr(self, "_header_widgets") and self._header_widgets:
                for header_cell in self._header_widgets:
                    if hasattr(header_cell, "configure"):
                        if self._state == "disabled":
                            header_cell.configure(text_color=self._header_fg)
                        else:
                            header_cell.configure(text_color=table_theme["header_text_color"])

                        if hasattr(header_cell, "_update_appearance"):
                            header_cell._update_appearance()

            # 3. Cascade parameters to the EXISTING active rendered data row sub-cells
            if hasattr(self, "_cell_widgets") and self._cell_widgets:
                for row_idx, row in enumerate(self._cell_widgets):
                    for col_idx, cell in enumerate(row):
                        if hasattr(cell, "configure"):
                            # Select text colors using your verified class tracking attributes
                            if self._state == "disabled":
                                cell.configure(text_color=self._cell_fg)
                                # Freeze text input entry elements cleanly via 'readonly' rules to preserve text readability
                                if hasattr(cell, "_entry") or "entry" in str(type(cell)).lower():
                                    cell.configure(state="readonly")
                            else:
                                cell.configure(text_color=table_theme["cell_text_color"])
                                if hasattr(cell, "_entry") or "entry" in str(type(cell)).lower():
                                    cell.configure(state="normal")

                            # Force the text layout to refresh its graphics inside the canvas window context
                            if hasattr(cell, "_update_appearance"):
                                cell._update_appearance()

        # ZONE D: EXECUTE BASE CLASS INITIALIZATION (Preserves state key for parent scrollframe tracking)
        super().configure(require_redraw=require_redraw, **kwargs)

    def get_num_rows(self) -> int:
        if hasattr(self, "_cell_widgets") and self._cell_widgets:
            return len(self._cell_widgets)
        return self._num_rows

    def get_num_columns(self) -> int:
        if hasattr(self, "_cell_widgets") and self._cell_widgets and self._cell_widgets:
            return len(self._cell_widgets[0]) if self._cell_widgets and self._cell_widgets[0] else self._num_columns
        return self._num_columns

    def set_column_properties(self, column_index: int, width: int, anchor: Literal["w", "center", "e"] = "center"):
        if 0 <= column_index < len(self._column_widths):
            self._column_widths[column_index], self._column_anchors[column_index] = width, anchor
            if column_index < len(self._header_widgets) and self._show_headers:
                txt = self.columns_list[column_index] if column_index < len(self.columns_list) else ""
                display_text = "   " + txt if anchor == "w" else (txt + "   " if anchor == "e" else txt)
                self._header_widgets[column_index].configure(width=width, anchor=anchor, text=display_text)

    def bind_selection_callback(self, callback: Callable):
        self._click_callback = callback

    def bind_edit_callback(self, callback: Callable):
        self._edit_callback = callback

    def bind_validation_callback(self, callback: Callable):
        self._validation_callback = callback


# ==========================================
#   MAIN RUNNER TESTING ENVIRONMENT
# ==========================================
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("sCTkTableview Full Validation & State Showcase")

    border_capsule = ctk.CTkFrame(root, fg_color="transparent", border_width=2, border_color=("#64748B", "#94A3B8"),
                                  corner_radius=12)
    border_capsule.pack(padx=20, pady=20, fill="both", expand=True)

    cols = ["Channel Label", "Frequency (MHz)", "Mode", "Station Name"]

    # Initialize your table view module cleanly (Pass state="normal" or state="disabled" to test lock modes)
    table = sCTkTableview(border_capsule, columns=cols, grid_mode="zebra", header_line_width=3, outline_width=1.5,
                          outline_radius=6, state="normal")
    table.pack(padx=10, pady=(10, 10), fill="both", expand=True)

    table.set_column_properties(0, width=110, anchor="w")
    table.set_column_properties(1, width=120, anchor="center")
    table.set_column_properties(2, width=70, anchor="center")
    table.set_column_properties(3, width=250, anchor="w")

    ham_stations = [
        ["160M-VOX", "1.8400", "LSB", "160m - Voice / Calling"],
        ["40M-LSB", "7.2000", "LSB", "40m - LSB Voice Calling"],
        ["40M-FT8", "7.0740", "USB", "40m - FT8 Digital Mode"],
        ["20M-FT8", "14.0740", "USB", "20m - FT8 Digital Mode"],
        ["17M-USB", "18.1300", "USB", "17m - USB Voice Calling"],
        ["15M-USB", "21.3000", "USB", "15m - USB Voice Calling"],
        ["12M-USB", "24.9500", "USB", "12m - USB Voice Calling"],
        ["10M-USB", "28.4000", "USB", "10m - Tech / General Voice"]
    ]
    table.load_dataset(ham_stations)


    def validate_table_cell_changes(column_index: int, raw_input_string: str) -> bool:
        cleaned_input = str(raw_input_string).strip()
        if column_index == 1:
            try:
                float(cleaned_input); return True
            except ValueError:
                return False
        if column_index == 2: return cleaned_input.upper() in ["LSB", "USB", "AM", "FM", "CW"]
        return len(cleaned_input) > 0


    table.bind_validation_callback(validate_table_cell_changes)
    table.bind_selection_callback(lambda r, vals: print(f"📡 Clicked Row: {r} -> {vals}"))
    table.bind_edit_callback(lambda r, c, val: print(f"📝 Persistent Data Saved ({r}, {c}) -> '{val}'"))
    table.configure(state="disabled")

    root.mainloop()
