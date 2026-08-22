## sCTkFileExplorer

The `sCTkFileExplorer` is a highly configurable, theme-compliant custom file and folder navigation panel. Designed as an embedded, nested component layout rather than a separate popup dialog frame, it maps absolute directory environments onto a scannable canvas area. Valid files and subfolders render with custom graphical glyphs, while invalid or filtered file records are dynamically dimmed and locked out from interactions. 

This component supports a strict runtime `disabled` state configuration, dynamically desaturating typography elements, freezing scrollbar navigation, and locking out item selection events globally when running inside embedded container tabs.

---
![FileExplorer.png](images/FileExplorer.png)

### 📋 API Constructor Reference

```python
sCTkFileExplorer(master, type="directory", filetypes=None, initialdir=None, initialfile=None, command=None, double_click_command=None, width=400, height=300, corner_radius=None, border_width=None, bg_color="transparent", fg_color=None, border_color=None, background_corner_colors=None, overwrite_preferred_drawing_method=None, **kwargs)
```

| Parameter Name | Data Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `master` | `any` | *Required* | Reference pointer tracking your root window, parent layout layer, or container frame capsule. |
| `type` | `str` | `"directory"` | Structural layout operation mode. Options: `"directory"` (renders folders only) or `"file"` (renders folders and compatible files). |
| `filetypes` | `list` / `str` | `None` | Filter array masking permitted file extensions. Formatted as an explicit python list or bracketed string array (e.g., `['.py', '.txt']`). Defers to unfiltered mode when `None`. |
| `initialdir` | `str` | `None` | Starting navigation folder pathway string. Supports tilde user expansion (`~`) and forces normalization to absolute paths at instantiation. Defaults to `os.getcwd()` if omitted. |
| `initialfile` | `str` | `None` | Default starting highlight target file path string. Highlights and selects the specified file asset row automatically on boot. |
| `command` | `callable` | `None` | Single-click method event callback triggered instantly whenever a valid, active list row is highlighted. Requires a strict **two-argument footprint**. |
| `double_click_command` | `callable` | `None` | Double-click selection method callback executed when an active row file is confirmed or executed. Requires a strict **two-argument footprint**. |
| `width` | `int` | `400` | Manual horizontal width constraint boundary dimension allocated to the explorer component measured in pixels. |
| `height` | `int` | `300` | Manual vertical height constraint boundary dimension allocated to the explorer component measured in pixels. |

---

### ⚡ Execution Event Callbacks (`command` & `double_click_command`)

Both callback functions execute dynamically when rows are manipulated by the user. To prevent application layer traceback drops, **any method mapped to these commands must accept exactly two mandatory arguments**:

```python
def my_explorer_callback(widget_instance, selected_path):
    """
    Mandatory Callback Signature Requirement
    
    1. widget_instance: The sCTkFileExplorer object triggering the method loop.
    2. selected_path:   The absolute string file path matching the row just clicked.
    """
    print(f"Action detected from {widget_instance}: Processing path -> {selected_path}")
```

* **`command`**: Triggers when a folder or file row is highlighted on a single click. Passes the updated absolute string path of the row item as the second parameter.
* **`double_click_command`**: Triggers when an active row item is double-clicked. If the targeted row is a subdirectory, the explorer automatically expands and steps *into* that directory. If the item is a valid file asset, it hands structural control back to the callback method, passing the absolute file location path.

---

### 🎨 Centralized Stylesheet Integration (`sCTkThemes.py`)

The file explorer queries your repository styling map profile matrix using `ThemeableWidget._resolve_color()` lookup routines. This decoupling ensures that layout shapes, font styles, and path row aesthetics repaint smoothly during real-time theme profile adjustments.

To satisfy the framework configuration guidelines, ensure your theme matrix includes this structured asset block:

```python
THEME_DEFAULTS = {
    "sCTkFileExplorer": {
        # Typography configurations assigned to management controls and row labels
        "btn_font": ("Arial", 11, "bold"),
        "entry_font": ("Arial", 12, "normal"),
        
        # Upper navigational button styling variables
        "btn_fg": ("#3B82F6", "#1D4ED8"),
        "btn_hover": ("#2563EB", "#1E40AF"),
        "btn_text_color": ("#FFFFFF", "#F9FAFB"),
        "btn_border_color": ("#1E3A8A", "#1E3A8A"),

        # Path display address input cell field colors
        "entry_fg": ("#FFFFFF", "#111827"),
        "entry_text_color": ("#1F2937", "#F9FAFB"),
        "entry_border_color": ("#CBD5E1", "#475569"),

        # Live File Row Rendering Palette Look Parameters
        "row_active_text": ("#1F2937", "#F9FAFB"),       # Color applied to valid choices
        "row_dimmed_text": ("#94A3B8", "#64748B"),      # Soft contrast color applied to filtered elements

        # Cascading State Lockdown Controllers
        "disabled_map": {
            "btn_fg": ("#CBD5E1", "#334155"),
            "btn_border_color": ("#CBD5E1", "#334155"),
            "btn_text_color": ("#94A3B8", "#64748B"),
            "entry_fg": ("#F3F4F6", "#1F2937"),
            "entry_border_color": ("#CBD5E1", "#475569"),
            "entry_text_color": ("#94A3B8", "#64748B"),
            "row_active_text": ("#94A3B8", "#64748B")
        }
    },
    # ... your other widget entries
}
```

---

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed the `sCTkFileExplorer` inside a root window workspace panel layout using the strict two-argument callback structure.

```python
#!/usr/bin/python3
import os
import customtkinter as ctk
from sCTkFileExplorer import sCTkFileExplorer


class FileExplorerTesterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Standalone Embedded sCTkFileExplorer Test Panel")
        self.geometry("600x500")
        
        # Configure root layout grid weighting
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Upper descriptive text label block
        self.header_lbl = ctk.CTkLabel(
            self, 
            text="sCTkFileExplorer Interactive Panel (Filtered to .py and .txt files)",
            font=("Arial", 14, "bold")
        )
        self.header_lbl.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        # Initialize and mount the custom layout file explorer
        self.explorer = sCTkFileExplorer(
            self,
            type="file",
            filetypes=[".py", ".txt"],
            initialdir="~",  # Gracefully handles tilde user space expansions
            command=self.track_single_click_highlight,
            double_click_command=self.execute_double_click_selection,
            width=570,
            height=400
        )
        self.explorer.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")

    def track_single_click_highlight(self, widget_instance, selected_path):
        """Fires instantly whenever an active directory list item is focused."""
        print(f"SINGLE-CLICK FOCUS -> Triggered by: {widget_instance}")
        print(f"                       Selected Path: {selected_path}\n")

    def execute_double_click_selection(self, widget_instance, selected_path):
        """Fires when an item row is successfully double-clicked or confirmed."""
        print(f"🚀 DOUBLE-CLICK CONFIRMED! Target: {selected_path}")
        if os.path.isfile(selected_path):
            print(f"Executing explicit business logic handler rules on target asset file.")


if __name__ == "__main__":
    # Initialize the main loop wrapper
    app = FileExplorerTesterApp()
    app.mainloop()
```


[Return to Table of Contents](#contents)



