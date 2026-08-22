


## sCTkSeparator

(Derived from Selector class by Fastattack, 2024. This widget was made available to the community via the MIT License.  Source Repository: [MoreCustomTkinterWidgets](https://github.com/fastattackv/MoreCustomTkinterWidgets) )


The *sCTkSeparator* is an advanced, themeable divider widget for CustomTkinter. It provides dynamic scaling via layout managers, vector-drawn customizable corner radiuses, dashed/dotted line styles, and automated line-splitting centered section text headers with bounding capsule brackets.

--- 
### Widget Preview
![sCTkSeparator.png](images/sCTkSeparator.png)

### API Property Reference

| Property Name | Data Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `master` | `any` | *Required* | Parent container instance (e.g., `sCTkFrame` or `ctk.CTk`). |
| `length` | `int` | `100` | The total span length of the line track in pixels (corresponds to widget height if vertical, width if horizontal). |
| `width` | `float` | `4` | The visual thickness profile of the divider line in pixels. |
| `corner_radius` | `int` or `None` | `6` (from theme) | Defines roundness sharpness of divider line endpoints (defaults to stylesheet configuration). |
| `orientation` | `str` | `"vertical"` | Sets spatial directional positioning alignment. Accepts `"vertical"` or `"horizontal"`. |
| `text` | `str` | `""` | Appends a centered section header label text directly inside a computed line split zone. |
| `font` | `tuple` or `CTkFont` | `("Arial", 11, "bold")` | Text font profile style parameters for the embedded header tag. |
| `text_color` | `str` or `Tuple[str, str]` | Central theme default | Font hex palette token string mapping. Supports appearance mode tuples. |
| `dash` | `tuple` or `None` | `None` | Integer stroke sequence array tuple mapping out dashed/dotted rendering rules (e.g., `(5, 5)`). |

---

### Centralized Stylesheet Setup (`sCTkThemes.py`)
As of the writing of this document, the current Themes for the sCTkSeparator is included below. However, the governing theme is always stored in sCTkThemes.py in your installation directory.

```python
    "sCTkSeparator": {
            # Format: (Light Mode Hex, Dark Mode Hex)
            # Softer mid-tones changed to robust crisp outlines for sharp visual separation
            "fg_color": ("#808080", "#8A9296"),
            "bg_color": "transparent",
            "corner_radius": 6,
            "font": ("Arial", 11, "bold"),
            "text_color": ("#1A1A1A", "#FFFFFF")  # Crisp high-contrast header text labels
        },
```

---

### Layout Manager Integration

Mixing layout manager tracking loops within the same immediate frame layer is completely blocked. When handling automated expansion parameters across scaling monitor resolutions, enforce the following geometry behaviors:

#### Grid Configurations (`.grid()`)
* **Horizontal Mode Line**: Must use **`sticky="ew"`** to allow the vector path to grow horizontally.
* **Vertical Mode Line**: Must use **`sticky="ns"`** to stretch the line across rows.
* **Parent Frame Setup**: The container frame track columns/rows **must** have their weights configured to let the engine allocate expanding window real estate:
  ```python
  # Column 0 and Column 2 hold widgets and expand; Column 1 isolates the separator line track
  grid_Frame.grid_columnconfigure(0, weight=1)
  grid_Frame.grid_columnconfigure(1, weight=0)
  grid_Frame.grid_columnconfigure(2, weight=1)
  ```

#### Pack Configurations (`.pack()`)
* **Horizontal Mode Line**: Must use **`fill="x"`** alongside `expand=False` so it hugs adjacent frames tightly instead of expanding into empty background rows.
* **Vertical Mode Line**: Must use **`fill="y"`** inside layout columns.

---

### Pygubu Designer Properties Guide

When configuring layouts visually within the Pygubu Designer editing workspace panel strip, observe these property formatting rules:

1. **`orientation`**: Select `vertical` or `horizontal` from the choice dropdown list pane. The preview canvas will immediately adjust orientations without flattening.
2. **`text`**: Type any section title banner sequence string directly into the entry field (e.g., `AUDIO CONTROLS`). The line will cleanly break around the text boundaries.
3. **`dash`**: Enter raw comma-separated lists of numerical values directly into the input strip **without using quote symbols or brackets**.
   * Type `5,5` for standard clean dash blocks.
   * Type `2,6` for clean dotted layout maps.
   * Leave blank or type `None` to restore solid rounded vector shapes.
4. **Dimensions with Headers**: When utilizing `text` headers on a `vertical` orientation alignment track line, remember to increase the designer **`width`** attribute setting from `4` to a larger size (e.g., `20` or `24`) to give the vertical top and bottom capsule framing lines physical canvas clearance to draw.

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed the `sCTkFileExplorer` inside a root window workspace panel layout using the strict two-argument callback structure.

```python
#!/usr/bin/python3
import customtkinter as ctk
from ThemeableWidget import ThemeableWidget

import customtkinter as ctk
from sCTkSeparator import sCTkSeparator
# ==========================================
#   MAIN TESTING RUNNER CODE BLOCK
# ==========================================
if __name__ == "__main__":
    if "sCTkSeparator" not in THEME_DEFAULTS:
        THEME_DEFAULTS["sCTkSeparator"] = {
            "fg_color": ("#BABABA", "#565B5E"),
            "bg_color": "transparent",
            "corner_radius": 6
        }

    root = ctk.CTk()
    root.title("sCTkSeparator Feature Test Environment")
    root.geometry("600x450")

    grid_Frame = ctk.CTkFrame(root)
    grid_Frame.pack(side="top", fill="both", expand=True, padx=20, pady=15)

    grid_Frame.grid_columnconfigure(0, weight=1)
    grid_Frame.grid_columnconfigure(1, weight=0)
    grid_Frame.grid_columnconfigure(2, weight=1)
    grid_Frame.grid_rowconfigure(0, weight=1)

    lbl_left = ctk.CTkLabel(grid_Frame, text="Left Sub-Panel Group Data")
    lbl_left.grid(row=0, column=0, sticky="nswe")

    sep_vertical_text = sCTkSeparator(grid_Frame, orientation="vertical", text="CORE API", width=4)
    sep_vertical_text.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

    lbl_right = ctk.CTkLabel(grid_Frame, text="Right Sub-Panel Group Data")
    lbl_right.grid(row=0, column=2, sticky="nswe")

    sep_horizontal_text = sCTkSeparator(root, orientation="horizontal", text="SYSTEM DASH SEPARATOR SECTION", width=4)
    sep_horizontal_text.pack(side="top", fill="x", padx=20, pady=10)

    pack_frame = ctk.CTkFrame(root)
    pack_frame.pack(side="bottom", fill="both", expand=True, padx=20, pady=(5, 20))

    panel_a = ctk.CTkLabel(pack_frame, text="System Input Options")
    panel_a.pack(side="left", fill="both", expand=True)

    sep_dashed = sCTkSeparator(pack_frame, orientation="vertical", width=4, dash=(4, 4))
    sep_dashed.pack(side="left", fill="y", padx=10, pady=15)

    panel_b = ctk.CTkLabel(pack_frame, text="System Output Channels")
    panel_b.pack(side="right", fill="both", expand=True)

    root.mainloop()
```


[Return to Table of Contents](#contents)


