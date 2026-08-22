## sCTkOptionMenuPrimary

A theme-compliant, prominent selection drop-down option menu widget variant. It integrates early parameter-popping initialization filters alongside a deep-copy keyword caching shield. This configuration permanently protects your active color selections and list trackers from experiencing native CustomTkinter validation failures.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkOptionMenu(master)` | `sCTkOptionMenuPrimary(master)` *(Primary selection drop-down)* |
| **Maintenance** | Local style overrides duplicated across files manually. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Everything runs under one core native composite track. | Separated safely across `sCTkOptionMenuPrimary.py` and `ThemeableWidget.py`. |
| `state(mode)` | `self.configure(state=...)` | `Method (str)` handling layout tracking map transformations (`'normal'`, `'disabled'`). |
| `get_state()` | `self.cget("state")` | `Method -> str` explicit verification query matching system test assertions. |
| `update_list(list, idx)` | *Not Available Natively* | **Helper Pass:** Dynamically updates items and sets default indices safely. |

---

### Constructor

Initialize a custom primary option selection drop-down instance. Menu trackers like `values`, `command`, and `variable` are explicitly popped early inside `__init__` to protect the layout engine from keyword collisions.

```python
# Instantiate a primary option selection dropdown
operating_modes = ["Mode: USB", "Mode: LSB", "Mode: AM", "Mode: CW"]

mode_selector = sCTkOptionMenuPrimary(
    master=control_panel,
    values=operating_modes,
    command=on_radio_mode_selected
)

# Render the widget inside your parent container coordinate tracker panel
mode_selector.pack(fill="x", padx=40, pady=10)
```

---

### Callback Signature & Usage

Dispatches the selected string value directly to interface listeners natively upon item dropdown changes.

#### Command 

```python
# Fires instantly upon receiving a new drop-down selection selection click
def on_radio_mode_selected(chosen_value: str):
    print(f"Radio Selection Telemetry: {chosen_value}")
```

### Dynamic Property Modifiers Live
```python
# Query current selections or force alternative text positions on the fly
active_choice = mode_selector.get()     # Queries the active text string visible on the button face
mode_selector.set("Mode: USB")          # Manually updates the displayed text choice selection target
```

### Convenience Functions
```python
# Dynamically re-populate option menu arrays without throwing layout bugs
new_bands = ["160M Band", "80M Band", "40M Band", "20M Band"]
mode_selector.update_list(new_bands, default_index=2) # Re-populates list and selects "40M Band"

# Evaluate current state configurations or apply absolute user interaction locks
current_mode = mode_selector.get_state()   # Returns 'normal' or 'disabled'
mode_selector.state("disabled")             # Locks down the menu dropdown arrow and applies muted gray fills
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkOptionMenuPrimary": {
        "fg_color": ["#1A4375", "#1F6AA5"],
        "button_color": ["#112A4B", "#194A7A"],
        "button_hover_color": ["#0B1B30", "#143C63"],
        "text_color": ["#FFFFFF", "#FFFFFF"],
        "disabled_map": {
            "fg_color": ["#F3F4F6", "#1F2937"],
            "button_color": ["#E5E7EB", "#374151"],
            "button_hover_color": ["#E5E7EB", "#374151"],
            "text_color": ["#94A3B8", "#64748B"]
        }
    }
}
```

### Other notes
* **Deep-Copy Dictionary Isolation Shield:** Because CustomTkinter's native option menu initialization code mutates, strips, and deletes keys directly out of raw dictionary data footprints during its boot phase, the constructor clones your configurations into `self._local_defaults = dict(self.final_kw)` beforehand. This prevents normal state restorations from crashing on missing keys.
* **Null Pointer Prevention Filters:** The internal visual loop is fortified to look up CustomTkinter's master `ThemeManager` variables if a specific color style (like `button_hover_color`) is completely skipped inside `themes.json`, blocking dangerous `None` keyword objects from halting application threads.


### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed an `sCTkSOptionMenutPrimary` alongside a live telemetry monitor.

```python
#!/usr/bin/python3
import customtkinter as ctk
from sCTkFrame import sCTkFrame
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkOptionMenuPrimary import sCTkOptionMenuPrimary

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("450x260")
    root.title("Option Menu Telemetry Bench")

    # 1. Mount standard application workspace container
    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # 2. Attach live data feedback monitor readout
    lbl_data = sCTkLabelSecondary(base, text="Active choice telemetry pending...")
    lbl_data.pack(pady=10)

    # 3. Instantiate your custom option menu widget selector element
    option_menu = sCTkOptionMenuPrimary(
        base, 
        values=["Initial Mode A", "Initial Mode B"],
        command=lambda choice: lbl_data.configure(text=f"Selection Captured: {choice}")
    )
    option_menu.pack(fill="x", padx=40, pady=10)

    # 4. Dynamically update options and set default tracking location
    option_menu.update_list(["Mode: USB", "Mode: LSB", "Mode: AM", "Mode: CW"], default_index=1)

    root.mainloop()
```