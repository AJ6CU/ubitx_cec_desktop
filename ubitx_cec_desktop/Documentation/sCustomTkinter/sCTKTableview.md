

## sCTkTableview

The `sCTkTableview` is a high-performance, theme-adaptive, and interactive data grid widget engineered specifically for the `sCustomTkinter` desktop amateur radio workspace architecture. It wraps a specialized scrollable container viewport to render structured, matrix-aligned logging rows, transceiver channels, or telemetry tracking data.

---

### 📐 Core Architecture & Environment Sync Rules

To operate seamlessly across both visual design suites and standalone Python initialization runners, the table implements a **Dual-Environment Priority Pass** constraint layout:

1. **Design Mode (`num_columns` Rules):** Within the Pygubu Designer layout studio pane, the explicit numeric sidebar options act as the source of truth. If you type more label names than `num_columns` dictates, the text is sliced down to prevent visual canvas breaking. If you type fewer labels, the trailing empty layout slots are preserved as blank spacer columns.
2. **Runtime Mode (`columns` Rules):** When executed natively in production code, the length of the list passed into the `columns=[...]` initializer constructor takes absolute authority, overriding any defaults to stretch or shrink the matrix widths dynamically.
3. **Alphabetical Optimization:** Pygubu Designer forcefully serializes configuration dictionary payloads alphabetically (causing `columns` to execute before `num_rows`). `sCTkTableview` utilizes an internal **Redraw Loop Debounce Gate** to capture all incoming parameters silently first, executing a single ordered draw pass right at the tail end to prevent layout collapse.

---

### 🛠️ Developer API Reference

### Constructor Signature

```python
table = sCTkTableview(
    master,
    columns=None,
    width=500,
    height=300,
    grid_mode="zebra",
    header_line_width=2,
    outline_width=1.0,
    outline_radius=4,
    state="normal",
    num_columns=3,
    num_rows=1,
    show_headers=True,
    cell_bg_color=None,
    cell_alt_bg_color=None,
    *args,
    **kwargs
)
```

### Public Methods

#### `load_dataset(dataset: List[List[Any]])`
Loads a 2D Python array into the active grid interface matrix canvas. 
* **Row Overflow:** If the number of incoming data rows exceeds the configured `num_rows`, the table dynamically stretches downward, scaling the scroll frame automatically.
* **Row Underflow:** If incoming data records are fewer than `num_rows`, the widget populates the cells and leaves the remaining rows blank (preserving layout proportions).

#### `get_num_rows() -> int`
Returns the true number of physical rows currently gridded on screen. This metric dynamically includes empty fallback slots and blank padding arrays.

#### `get_num_columns() -> int`
Returns the total number of structural columns currently managed inside the table, accurately counting un-labeled spacer cells.

#### `set_column_properties(column_index: int, width: int, anchor: Literal["w", "center", "e"] = "center")`
Adjusts the geometry constraints and text justification for a specific column index. Anchor tags smoothly recalculate text cell margins with tracking margin buffers.

#### `bind_selection_callback(callback: Callable[[int, List[Any]], None])`
Binds a mouse click tracking hook (`<Button-1>`) to all cell slots. Triggers the callback with the targeted row index and its matching data row list array.

#### `bind_edit_callback(callback: Callable[[int, int, str], None])`
Binds an operation interceptor hook triggered whenever an operator double-clicks a cell slot, modifies the inline `CTkEntry` field overlay, and commits changes via `<Return>` or focus loss.

#### `bind_validation_callback(callback: Callable[[int, str], bool] -> bool)`
Mounts a pre-save check gating hook before inline edits are saved to the core cell structure. Returning `False` rejects the user string and restores the original data cell text.

---

### 🎨 Visual Configuration & Style Sheet Tokens

`sCTkTableview` extracts default styling parameters directly from your centralized `THEME_DEFAULTS` dictionary, using the structural keyword token map `"sCTkTableview"`. It handles appearance changes natively, switching between dark and light modes cleanly.

| Property Keyword | Data Type | Permitted Values | Functional Output Behavior |
| :--- | :--- | :--- | :--- |
| `grid_mode` | `str` | `"grid"`, `"zebra"`, `"none"` | Changes row backgrounds. `"none"` collapses all padding to `0` for borderless flat screens. |
| `show_headers` | `bool` | `True`, `False` | Toggles the visibility of the primary header text labels. |
| `header_line_width` | `int` | `0` to `10` pixels | Size of the line divider under headers. Setting it to `0` joins rows seamlessly. |
| `state` | `str` | `"normal"`, `"disabled"` | Controls editing; `"disabled"` locks rows out from double-click cell edits. |
| `outline_width` | `float` | `0.0` to `5.0` pixels | Border line size bounding the frame layout. |
| `outline_radius` | `int` | `0` to `20` pixels | Corner roundness bounding the frame layout. |
| `cell_bg_color` | `str` / `tuple` | Color String / Hex Tuple | Primary row cell backing color override block. |
| `cell_alt_bg_color`| `str` / `tuple` | Color String / Hex Tuple | Alternating row color used to draw striping in `"zebra"` mode. |

---

### 🗃️ Complete Edge-Case Integration Sample

```python
import customtkinter as ctk
from sCTkTableview import sCTkTableview

app = ctk.CTk()
app.geometry("600x400")

# Setup 5 columns x 8 rows baseline
table = sCTkTableview(
    master=app,
    num_columns=5,
    num_rows=8,
    columns=["Callsign", "Frequency", "Mode", "Power", "Grid"],
    grid_mode="zebra"
)
table.pack(padx=20, pady=20, fill="both", expand=True)

# 🚀 Robust Overflow/Underflow Handling Sample Data Payload
# Row 3 underflows column settings (padded with blanks)
# Row 4 overflows column settings (safely truncated)
logging_payload = [
    ["W6EL", "14.074 MHz", "FT8", "50W", "DM14"],
    ["K6K7", "7.047 MHz", "CW", "100W", "CM87"],
    ["N6RE", "21.285 MHz"], 
    ["AI6IR", "144.200 MHz", "FM", "25W", "DM12", "EXTRA_FIELD_IGNORED"]
]

table.load_dataset(logging_payload)

# Execution Hook Callbacks Linkages
table.bind_selection_callback(lambda r, data: print(f"Selected Row {r}: {data}"))
table.bind_edit_callback(lambda r, c, val: print(f"Cell modified at ({r},{c}) -> New Value: {val}"))
table.bind_validation_callback(lambda c, val: len(val.strip()) > 0) # Reject empty updates

app.mainloop()
```


# Notes


[Return to Table of Contents](#contents)


