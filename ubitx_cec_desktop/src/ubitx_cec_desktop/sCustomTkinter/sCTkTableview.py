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
        self._header_line_width = int(header_line_width) if header_line_width else 2
        self._outline_width = float(outline_width) if outline_width else 1.0
        self._outline_radius = int(outline_radius) if outline_radius else 4
        self._state = state

        self._num_columns = int(num_columns)
        self._num_rows = int(num_rows)

        clean_show = str(show_headers).replace("'", "").replace('"', "").strip().lower()
        self._show_headers = True if clean_show in ("true", "1", "yes") else False

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
            self.columns_list = columns
            self._num_columns = len(columns)
        else:
            self.columns_list = [f"Column {i + 1}" for i in range(self._num_columns)]

        self._column_widths = (120,) * self._num_columns
        self._column_anchors = ["center"] * self._num_columns
        self._click_callback, self._edit_callback, self._validation_callback = None, None, None

        self._create_header_bar()
        target_rows = self._num_rows if self._num_rows > 1 else 4
        blank_dataset = [["   ---   "] * self._num_columns for _ in range(target_rows)]
        self.load_dataset(blank_dataset)

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

        if not self._show_headers:
            return

        self.table_outline_frame.rowconfigure(0, minsize=28, weight=0)

        self.header_separator = ctk.CTkFrame(self.table_outline_frame, height=self._header_line_width,
                                             fg_color=self._grid_line_color, corner_radius=0)
        self.header_separator.grid(row=1, column=0, columnspan=len(self.columns_list), sticky="ew", padx=(2, 3),
                                   pady=(0, 2))
        try:
            self.header_separator.lift()
        except Exception:
            pass

        for col_idx, col_name in enumerate(self.columns_list):
            header_cell = sCTkLabelPrimary(self.table_outline_frame, text=col_name, font=self._header_font,
                                           text_color=self._header_fg, fg_color=self._header_bg, corner_radius=0,
                                           height=28, width=self._column_widths[col_idx])
            left_pad, right_pad = (2, 0) if col_idx == 0 else (
                (1, 2) if col_idx == len(self.columns_list) - 1 else (1, 0))
            header_cell.grid(row=0, column=col_idx, sticky="ew", padx=(left_pad, right_pad), pady=(2, 0))
            self.table_outline_frame.grid_columnconfigure(col_idx, weight=0)

            # 🚀 FIXED Z-INDEX MASKING:
            # Forcefully lift the header text label instances to the top of Tkinter's stacking deck.
            # This completely stops newly generated text rows from sliding over or hiding the labels!
            try:
                header_cell.lift()
            except Exception:
                pass

            self._header_widgets.append(header_cell)

    def load_dataset(self, dataset: List[List[Any]]):
        for cell in [c for row in self._cell_widgets for c in row]: cell.destroy()
        self._data_matrix, self._cell_widgets = [list(row) for row in dataset], []
        super().configure(width=0, height=0)
        row_offset = 2 if self._show_headers else 0

        for r_idx, r_data in enumerate(self._data_matrix):
            current_row_bg = self._cell_alt_bg if (self._grid_mode == "zebra" and r_idx % 2 != 0) else self._cell_bg
            r_cells = []
            for c_idx in range(self._num_columns):
                val = r_data[c_idx] if c_idx < len(r_data) else ""
                w_limit, h_limit = self._column_widths[c_idx], 26
                txt_anchor = self._column_anchors[c_idx]
                display_val = "    " + str(val) if txt_anchor == "w" else (
                    str(val) + "    " if txt_anchor == "e" else str(val))
                cell_label = sCTkLabelSecondary(self.table_outline_frame, text=display_val, font=self._cell_font,
                                                text_color=self._cell_fg, width=w_limit, height=h_limit,
                                                corner_radius=0, anchor=txt_anchor, fg_color="transparent")
                cell_label.configure(fg_color=current_row_bg)

                top_pad = 2 if r_idx == 0 else 1
                bot_pad = 2 if r_idx == len(self._data_matrix) - 1 else 0
                left_pad = 2 if c_idx == 0 else 1
                right_pad = 2 if c_idx == self._num_columns - 1 else 0
                cell_label.grid(row=r_idx + row_offset, column=c_idx, sticky="ew", padx=(left_pad, right_pad),
                                pady=(top_pad, bot_pad))
                r_cells.append(cell_label)
            self._cell_widgets.append(r_cells)

        # Firmly push the header bar elements to the absolute front layer of the Z-stack deck
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

    def configure(self, require_redraw=False, **kwargs):
        size_changed = False
        if "cell_bg_color" in kwargs:
            val = kwargs.pop("cell_bg_color")
            if isinstance(val, str) and val.startswith("(") and val.endswith(")"):
                try:
                    self._cell_bg = eval(val)
                except Exception:
                    pass
            elif val:
                self._cell_bg = val
            size_changed = True

        if "cell_alt_bg_color" in kwargs:
            val = kwargs.pop("cell_alt_bg_color")
            if isinstance(val, str) and val.startswith("(") and val.endswith(")"):
                try:
                    self._cell_alt_bg = eval(val)
                except Exception:
                    pass
            elif val:
                self._cell_alt_bg = val
            size_changed = True

        if "num_columns" in kwargs:
            self._num_columns = int(kwargs.pop("num_columns"))
            size_changed = True
        if "num_rows" in kwargs:
            self._num_rows = int(kwargs.pop("num_rows"))
            size_changed = True
        if "show_headers" in kwargs:
            val = kwargs.pop("show_headers")
            clean_show = str(val).replace("'", "").replace('"', "").strip().lower()
            self._show_headers = True if clean_show in ("true", "1", "yes") else False
            size_changed = True
        if "grid_mode" in kwargs:
            self._grid_mode = str(kwargs.pop("grid_mode") or "zebra").replace("'", "").replace('"', "").strip().lower()
            size_changed = True

        if "columns" in kwargs or "columns_list" in kwargs or size_changed:
            raw_cols = kwargs.pop("columns", kwargs.pop("columns_list", None))
            if isinstance(raw_cols, str):
                raw_cols = [c.strip() for c in raw_cols.split(',') if c.strip()]

            if raw_cols and len(raw_cols) > 0:
                self.columns_list = raw_cols
                self._num_columns = len(raw_cols)
            else:
                # 🚀 SMART RETENTION FIX:
                # Check if columns_list already has custom user text names inside it.
                # If it doesn't (or contains empty placeholder items), ONLY THEN generate defaults!
                is_currently_blank = not hasattr(self, "columns_list") or all(
                    str(c).strip() in ("", " ") for c in self.columns_list)
                if is_currently_blank or len(self.columns_list) != self._num_columns:
                    self.columns_list = [f"Column {i + 1}" for i in range(self._num_columns)]

            self._column_widths = (120,) * self._num_columns
            self._column_anchors = ["center"] * self._num_columns

            self._create_header_bar()
            target_rows = self._num_rows if self._num_rows > 1 else 4
            self.load_dataset([["   ---   "] * self._num_columns for _ in range(target_rows)])

            try:
                self.update()
            except Exception:
                pass

        if "header_line_width" in kwargs:
            val = kwargs.pop("header_line_width")
            self._header_line_width = int(val) if (val is not None and str(val).strip() != "") else 2
            if hasattr(self, "header_separator") and self._show_headers:
                self.header_separator.configure(height=self._header_line_width)

        if "outline_width" in kwargs:
            val = kwargs.pop("outline_width")
            self._outline_width = float(val) if (val is not None and str(val).strip() != "") else 1.0
            if hasattr(self, "table_outline_frame"):
                self.table_outline_frame.configure(border_width=self._outline_width)

        if "outline_radius" in kwargs:
            val = kwargs.pop("outline_radius")
            self._outline_radius = int(val) if (val is not None and str(val).strip() != "") else 4
            if hasattr(self, "table_outline_frame"):
                self.table_outline_frame.configure(corner_radius=self._outline_radius)

        if "state" in kwargs:
            self._state = kwargs.pop("state") or "normal"
            for row in self._cell_widgets:
                for cell in row:
                    if hasattr(cell, "configure"): cell.configure(state=self._state)
            require_redraw = True

        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str) -> Any:
        return self._state if attribute_name == "state" else super().cget(attribute_name)

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
