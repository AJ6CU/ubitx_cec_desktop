# `sCustomTkinter` File Browser Technical Documentation

This document contains the complete developer reference for the **`sCTkPathChooser`** compound widget row and the standalone **`sCTkFileExplorer`** directory panel. 

Both components are built natively using CustomTkinter vector elements, ensuring complete theme compliance (Light/Dark mode) and eliminating standard Tcl/Tk native focus loops and multi-click window bugs on macOS. Unselectable file formats are gracefully dimmed, disabled, and locked from clicks in real time.

---

## 🎨 Theme & Style Integration

Both components inherit natively from `ThemeableWidget` and automatically map styling configurations from the global dictionary registry **`THEME_DEFAULTS`** inside **`sCTkThemes.py`**.

### Centralized Integrity Guard Lockout
The widgets utilize an aggressive validation loop on startup inside `ThemeableWidget`. If `sCTkThemes.py` is entirely missing, or if any layout parameters resolve to `None`, the application halts immediately and outputs a highly descriptive error on the terminal tracking exactly which widget class configuration broke.

---

## 📥 1. `sCTkPathChooser` (Compound Widget)

The `sCTkPathChooser` is an advanced entry-based path selection row designed for settings forms and parameter configuration panels. It pairs a fluid layout text entry field with a stylized browse button. 

The text entry acts like an accordion: it automatically stretches or contracts to occupy whatever layout room is left over after accounting for the browse button's fixed metrics. By using a single vector character character token (such as `"▶"` or `">"`) combined with a narrow button width constraint, you can maximize the horizontal space available for viewing deep system directory text paths.

### Constructor Signature
```python
sCTkPathChooser(master=None, width=350, height=32, type="directory", justify="left", title="Select Path", initialdir=None, initialfile=None, filetypes=None, btn_width=110, btn_height=32, btn_text=None, entry_height=32, browser_width=500, browser_height=450, command=None, **kwargs)
```

### Available Arguments

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`master`** | `Widget` | `None` | The parent container context (e.g., `CTk`, `CTkFrame`, or `sCTkFrame`). |
| **`width`** | `int` | `350` | Total horizontal width in pixels of file entry and button combined. File path width = total width - button width. |
| **`height`** | `int` | `32` | Total vertical space allocated to the file path and button frame container. Children heights are set separately. |
| **`type`** | `Literal["file", "directory"]` | `"directory"` | Determines whether lookups target specific file extension targets or structural system directory folder locations. (Case-insensitive) |
| **`justify`** | `Literal["left", "right", "center"]` | `"left"` | Aligns path string text. Set to `"right"` to anchor long system paths on the trailing file/folder component names. |
| **`title`** | `str` | `"Select Path"` | Base title text printed at the top of the browser popup window modal. For files, allowed tracking suffixes are generated and appended automatically. |
| **`initialdir`** | `str` | `None` | The default directory path folder to focus on when opening the explorer. Resolves system home directories (`~`) natively. |
| **`initialfile`** | `str` | `None` | A seed absolute path string to a file or directory that populates the entry field bar natively on startup. Forces a directory fallback if `type="directory"`. |
| **`filetypes`** | `list[str]` | `None` | A list array of string extension masks (e.g., `[".py", ".txt"]`). Non-matching elements are dimmed out and locked from clicks. Ignored if `type="directory"`. |
| **`entry_height`** | `int` | `32` | Explicit thickness height in pixels assigned directly to the text entry field sub-widget. |
| **`btn_width`** | `int` | `110` | Explicit width in pixels assigned directly to the browse button element. |
| **`btn_height`** | `int` | `32` | Explicit thickness height in pixels assigned directly to the browse button element. |
| **`btn_text`** | `str` | `None` | Custom character text string mapped directly to the browse button face. If left as `None`, it automatically falls back to wide desktop-style phrases like `"Browse Folders..."`. Supports Unicode strings natively (e.g. `"▶"`). |
| **`browser_width`** | `int` | `500` | Target pop-up file browser window horizontal frame size in pixels. |
| **`browser_height`** | `int` | `450` | Target pop-up file browser window vertical frame size in pixels. |
| **`command`** | `Callable` | `None` | Callback method triggered instantly upon confirming and selecting a path location string. Forwards the path as its first positional parameter. |

### Public API Methods

*   **`set(path_string: str) -> None`**  
    Rewrites the location text printed inside the widget entry canvas box, running system normalization strings automatically. Dispatches your registered `command` callback.
*   **`get() -> str`**  
    Extracts the absolute normalized string path currently written inside the input field canvas box.

---

## 🛠️ 2. `sCTkFileExplorer` (Embedded Panel View)

The `sCTkFileExplorer` is the underlying modular viewport layout engine. It is isolated into its own Python file and class, meaning it can be instantiated as a **permanent, open, scrollable panel grid** right inside your dashboards, sidebar frames, or wide administrative tabs without spawning popup top-level screens. 

Because it operates inside modal conditions or distinct dashboard views, it does not manage its own recursive disabled state layer, letting parent forms manage container freezes cleanly instead.

### Constructor Signature
```python
sCTkFileExplorer(master, type="directory", filetypes=None, initialdir=None, initialfile=None, command=None, double_click_command=None, width=400, height=300, **kwargs)
```

---

## 🔬 3. Pure Python Implementation Examples

### Configuration A: Wide Descriptive Desktop Layout
```python
# Wide envelope with high-visibility descriptive text instructions
chooser_desktop = sCTkPathChooser(
    master=app,
    type="directory",
    width=550,
    height=45,
    btn_width=130,
    btn_text=None # Defaults to "Browse Folders..." phrase based on type variable
)
chooser_desktop.pack(pady=10)
```

### Configuration B: Compact Accordion Vector Layout (Pygubu/Native Style)
```python
# Minimal footprint maximize data viewing row space for nested system folders
chooser_compact = sCTkPathChooser(
    master=app,
    type="file",
    justify="right",
    filetypes=[".json", ".txt"],
    width=550,
    height=45,
    entry_height=36,
    btn_width=36,       # Square geometry dimensions
    btn_height=36,      # Square geometry dimensions
    btn_text="▶"        # Standard right arrow vector text character code mapping
)
chooser_compact.pack(pady=10)
```
