## sCTkCheckBox

Uniform application checkbox toggle component equipped with state tracking machines, centralized theme file injection, and multi-zone Pygubu Inspector design-time stability.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkCheckBox(master)` | `sCTkCheckBox(master)` *(Functions as Core Toggle Selection)* |
| **Maintenance** | Manual styling assignments across localized setups. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Everything runs under one core native pipeline. | Separated safely across `sCTkCheckBox.py`, `sCTkCheckBoxui.py`, and `ThemeableWidget.py`. |
| `state(mode)` | `self.configure(state=...)` | `Method (str)` handling layout tracking map transformations (`'normal'`, `'disabled'`). |
| `get_state()` | `self.cget("state")` | `Method -> str` explicit verification query matching system test assertions. |

---

### Constructor

Initialize a custom checkbox interaction instance. Any direct property configuration passed here will safely layer over your centralized `themes.json` asset settings at runtime.

```python
# Instantiate the themed checkbox element
logging_toggle = sCTkCheckBox(
    master=control_panel,
    text="Enable Logging Framework",
    border_width=3,                 # Override baseline json rim track dimensions on the fly
    command=framework_state_changed # Attach your interactive selection loop callback function
)

# Render the layout inside your parent container geometry panel
logging_toggle.pack(padx=20, pady=10)
```

---

### Callback Signature & Usage

Executes standard callback logic blocks on selection changes, cleanly interogating the instance value natively via core retrieval keys.

#### Command 

```python
# Fires on button selection state changes
def framework_state_changed():
    # Evaluates to 1 when active (checked), 0 when empty (unchecked)
    print("Checked" if logging_toggle.get() == 1 else "Unchecked")
```

### Dynamic Property Modifiers Live
```python
# Select or deselect the tracking node values directly on the fly
logging_toggle.select()   # Forces checkmark rendering active
logging_toggle.deselect() # Wipes the checkbox state back to empty
```

### Convenience Functions
```python
# Query current state value string or toggle operational availability cleanly
current_mode = logging_toggle.get_state() # Returns 'normal' or 'disabled'
logging_toggle.state("disabled")          # Locks interaction tracks and applies muted styles
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkCheckBox": {
        "font": ["Arial", 15, "normal"],
        "border_width": 3,
        "border_color": ["#64748B", "#94A3B8"],
        "fg_color": ["#1A4375", "#2471A3"],
        "hover_color": ["#112A4B", "#1F618D"],
        "text_color": ["#1F2937", "#D1D5DB"],
        "disabled_map": {
            "text_color": ["#94A3B8", "#64748B"],
            "fg_color": ["#E5E7EB", "#374151"],
            "border_color": ["#CBD5E1", "#475569"]
        }
    }
}
```

### Other notes
* **Volatile Canvas Preservation:** Modifying states via `state()` completely bypasses manual canvas `.unbind()` scripts, ensuring CustomTkinter's native internal window tracking loops stay perfectly functional.
* **Pygubu Zone-A Interception:** The widget safely responds to single positional property queries coming from design-time editor tools without crashing or locking execution tracks.

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed the `sCTkCheckBox` inside a root window workspace panel layout using the strict interactive test configuration loops.

```python
import customtkinter as ctk
from sCTkCheckBox import sCTkCheckBox
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x200")

    widget = sCTkCheckBox(root, text="Enable Logging Framework")
    widget.configure(command=lambda: print("Checked" if widget.get() == 1 else "Unchecked"))
    widget.pack(expand=True, fill="none", padx=10, pady=10)

    widget.state("disabled")
    print("state (Disabled Pass) =", widget.get_state())
    
    widget.state("normal")
    print("state (Normal Pass)   =", widget.get_state())

    root.mainloop()
```


[Return to Table of Contents](#contents)


