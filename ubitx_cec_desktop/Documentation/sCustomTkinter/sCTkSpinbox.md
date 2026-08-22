

## sCTkSpinbox

The `sCTkSpinbox` is a highly configurable, theme-compliant custom spinbox wrapper widget. It extends `ctk.CTkFrame` and aggregates an internal `sCTkEntryPrimary` alongside two stacked or flanking directional button controls. The component dynamically supports two operational tracking tracks: standard numerical incrementation step ranges, and discrete string text array index navigation. Like all sCTk widgets, it is theme-adaptive.

---

### 📋 API Constructor Reference

```python
sCTkSpinbox(master=None, from_=0.0, to=100.0, step_size=1.0, command=None, state="normal", wrap=False, justify="left", show=None, placeholder_text=None, exportselection=True, width=140, height=32, **kw)
```

| Parameter Name | Data Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `master` | `any` | `None` | Reference pointer tracking your root window or parent layout layer capsule container. |
| `from_` | `float` | `0.0` | The lower numerical limit boundary representing the floor of your adjustment range. |
| `to` | `float` | `100.0` | The upper numerical limit boundary representing the ceiling of your adjustment range. |
| `step_size` | `float` | `1.0` | The exact mathematical offset added or subtracted from your tracking float on every button click. |
| `command` | `callable` | `None` | Optional event logging callback function executed instantly on text shifts, passing the active value. |
| `state` | `str` | `"normal"` | Execution state controller. Toggling to `"disabled"` dampens and locks out all inputs and arrows. |
| `wrap` | `bool` | `False` | Mechanical boundary iteration loop flag. When `True`, stepping past limits wraps around to alternative poles. |
| `justify` | `str` | `"left"` | Content text arrangement alignment tracking mask within the entry area. Options: `"left"`, `"center"`, `"right"`. |
| `show` | `str` | `None` | Character masking input indicator string sequence (e.g. `show="*"` for password entries). |
| `placeholder_text` | `str` | `None` | Faded background prompt text block displayed natively whenever the input cell field is completely empty. |
| `exportselection` | `bool` | `True` | Standard Tkinter selection clipboard persistence state identifier switch. |
| `width` | `int` | `140` | Manual hardware panel horizontal width layout footprint dimension measured in pixels. |
| `height` | `int` | `32` | Manual hardware panel vertical height layout footprint dimension measured in pixels. |

### 🛠️ Custom Keyword Extensions (`**kw`)
These exclusive configuration parameters override default geometry behaviors, resolve theme definitions, and style proportions dynamically:

| Extension Parameter | Data Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `button_width` | `int` | `22` | The horizontal width tracking measurement assigned to increment/decrement button frames in pixels. |
| `button_height` | `int` | `None` | The vertical button height. If `None`, scales automatically based on active grid parameters. |
| `button_side` | `str` | `"right"` | Hardware control grid positioning side anchor layout. Options: `"right"`, `"left"`, `"split"`. |
| `orientation` | `str` | `"vertical"` | Structural grid layout arrangement axis profile track. Options: `"vertical"`, `"horizontal"`. |
| `arrow_font` | `tuple` / `str` | `None` | Typography tuple passed directly to the arrows/glyphs. Ensures runtime theme compatibility. |
| `arrow_font_size` | `int` | `8` | Typography scaling rule explicitly defining point sizes for the raw directional glyph markings inside Pygubu. |
| `format` | `str` | `""` | Numerical formatting mask specifier string rule (supports C percent styles `%.3f` or bracket masks `{:.3f}`). |
| `values` | `str` / `list` | `None` | Literal input values array string loader. Setting choices converts your widget into Discrete Text List Mode. |

---

### ⚡ Global Object Instance Methods

#### Programmatically Set Value Elements
```python
# Insert a distinct float, integer, or matching list mode text option string natively
spinbox.set(12.5)
```

#### Fetch Active Value Strings
```python
# Reaches into the data entry track, pulling back the active string layout contents
current_selection = spinbox.get()
```

#### Discrete Values Array Loader Shortcut
```python
# Programmatically inject custom space-separated lines or list records on the fly
spinbox.set_values('Low Medium High "Extreme Alert" Max')
```

#### Layout Parameter Configuration Modifier
```python
# Updates interactive structural layouts or boundaries cleanly without layout recreation overhead
spinbox.configure(orientation="horizontal", button_side="split", arrow_font_size=14, wrap=True)
```

#### Advanced Sub-Component Style Targeting
If an explicit overrides requirement arises at runtime that bypasses the compiled stylesheet definitions, you can directly interact with the isolated increment/decrement components safely without initialization crashes:
```python
# Manually altering internal button typography fonts at runtime
spinbox._sub_button_1.configure(font=("Arial", 8, "normal")) # Increment button
spinbox._sub_button_2.configure(font=("Arial", 8, "normal")) # Decrement button
```

---

### 🎨 Centralized Stylesheet Integration (`sCTkThemes.py`)

The widget relies heavily on direct index key lookups within your central styling map profile matrix. The theme mapping profile utilizes explicit arrow definitions, glyph direction markers, formatting masks, and soft contrast palettes to eliminate runtime fallback drops.

```python
THEME_DEFAULTS = {
    "sCTkSpinbox": {
        # Font family and dimensions applied natively into the tracking sCTkEntryPrimary field area
        "font": ("Arial", 15, "normal"),
        
        # Font configuration specifically assigned to resolve button arrows/glyphs
        "arrow_font": ("Arial", 8, "normal"),
        
        # Explicit directional string characters assigned to step button graphics 
        "arrow_up_char": "▲",
        "arrow_down_char": "▼",
        "arrow_right_char": "▶",
        "arrow_left_char": "◀",

        # String rendering format controller (C percent-style or python bracket mapping rules)
        "format": "%.2f",

        # Geometry footprints matching baseline sCTkEntryPrimary boundaries
        "border_width": 1.5,
        "corner_radius": 6,
        
        # Active Layout Palette Look Parameters
        "entry_color": ("#FFFFFF", "#111827"),
        "border_color": ("#1A4375", "#64748B"),
        "text_color": ("#1F2937", "#F9FAFB"),
        
        # 🎨 UPDATED SOFT CONTRAST:
        # Light Mode: Comfortable Slate Blue-Grey (#5A6E7F)
        # Dark Mode: Muted Technical Steel Blue-Grey (#526071) - Soft, readable, non-distracting
        "placeholder_text_color": ("#5A6E7F", "#526071"),
        
        "button_color": ("#9E9E9E", "#2A2F3D"),
        "button_hover_color": ("#7D7D7D", "#374151"),

        # Direct cascading mapping dictionary nested cleanly for the locked disabled state machine
        "disabled_map": {
            "entry_color": ("#F3F4F6", "#1F2937"),
            "border_color": ("#CBD5E1", "#475569"),
            "text_color": ("#94A3B8", "#64748B"),
            "button_color": ("#CBD5E1", "#334155")
        }
    }

```


[Return to Table of Contents](#contents)


