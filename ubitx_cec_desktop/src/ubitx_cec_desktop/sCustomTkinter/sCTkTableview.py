import customtkinter as ctk
from typing import List, Optional, Callable, Any, Literal
from sCTkThemes import THEME_DEFAULTS
from sCTkLabelPrimary import sCTkLabelPrimary
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkScrollableFrame import sCTkScrollableFrame


class sCTkTableview(sCTkScrollableFrame):
    def __init__(self, master: any, columns: Optional[Any] = None, width: int = 500, height: int = 300,
                 grid_mode: Literal["zebra", "grid", "none"] = "zebra", header_line_width: int = 2,
                 outline_width: float = 1.0, outline_radius: int = 4, state: Literal["normal", "disabled"] = "normal",
                 num_columns: int = 3, num_rows: int = 1, show_headers: Any = True,
                 cell_bg_color: Optional[Any] = None, cell_alt_bg_color: Optional[Any] = None, *args, **kwargs):
        self.final_kw = THEME_DEFAULTS.get("sCTkTableview", THEME_DEFAULTS.get("sCTkTableView", {}))
        self._header_bg = self.final_kw.get("header_bg_color", ("#E2E8F0", "#1E293B"))
        self._header_fg = self.final_kw.get("header_text_color", ("#0F172A", "#F8FAFC"))
        self._header_font = self.final_kw.get("header_font", ("Arial", 14, "bold"))

        self._cell_bg = cell_bg_color if cell_bg_color is not None else self.final_kw.get("cell_bg_color",
                                                                                          ("#FFFFFF", "#111827"))
        self._cell_alt_bg = cell_alt_bg_color if cell_alt_bg_color is not None else self.final_kw.get(
            "cell_alt_bg_color", ("#D1DCEE", "#222C3A"))
        self._cell_fg = self.final_kw.get("cell_text_color", ("#1E293B", "#E2E8F0"))
        self._cell_font = self.final_kw.get("cell_font", ("Arial", 13, "normal"))
        self._grid_line_color = self.final_kw.get("grid_line_color", ("#CBD5E1", "#334155"))

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

        super().__init__(master=master, width=width, height=height, *args, **kwargs)
        super().configure(border_width=0, corner_radius=0, fg_color=self._cell_bg)

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

        # ✅ FIXED CONSTRUCTOR LIST INITIALIZATION ARRAYS
        self._column_widths = [120] * self._num_columns
        self._column_anchors = ["center"] * self._num_columns
        self._click_callback, self._edit_callback, self._validation_callback = None, None, None

        self._create_header_bar()
        self.load_dataset([[""] * self._num_columns for _ in range(self._num_rows)])

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
        rebuild_layout = False

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
    table = sCTkTableview(border_capsule, columns=cols, grid_mode="grid", header_line_width=3, outline_width=1.5,
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

    root.mainloop()
