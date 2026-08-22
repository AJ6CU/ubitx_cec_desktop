
## sCTkComboBox

Multi-layered dropdown option selection widget equipped with custom composite state controllers, parameter-popping architecture initialization tracks, and Pygubu Inspector design-time stability.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkComboBox(master)` | `sCTkComboBox(master)` *(Functions as Composite Select Menu)* |
| **Maintenance** | Local style overrides duplicated across widgets. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Everything runs under one core native pipeline. | Separated safely across `sCTkComboBox.py`, `sCTkComboBoxui.py`, and `ThemeableWidget.py`. |
| `state(mode)` | `self.configure(state=...)` | `Method (str)` handling layout tracking map transformations (`'normal'`, `'disabled'`). |
| `get_state()` | `self.cget("state")` | `Method -> str` explicit verification query matching system test assertions. |

---

### Constructor

Initialize a custom option tracking menu instance. Composite parameters like `values`, `command`, and `variable` are explicitly popped early inside `__init__` to protect the layout engine from keyword collisions.

```python
# Instantiate the themed option selection element
frequency_selector = sCTkComboBox(
    master=control_panel,
    values=["Channel A (VHF)", "Channel B (UHF)", "Direct Audio Feed"],
    command=frequency_index_latched  # Attach your option change loop callback function
)

# Render the layout inside your parent container geometry tracker path
frequency_selector.pack(padx=20, pady=10)
```

---

### Callback Signature & Usage

Dispatches selected option value text strings down to runtime logging terminals directly upon mouse selection changes inside the floating popup card window.

#### Command 

```python
# Fires on dropdown menu option selection loops
def frequency_index_latched(selected_choice: str):
    print(f"ComboBox Option Latched: {selected_choice}")
```

### Dynamic Property Modifiers Live
```python
# Force alter the active option string selection array on the fly
frequency_selector.configure(values=["HF Band Feed", "Satellite Link (SHF)"])
```

### Convenience Functions
```python
# Manually inject a default tracking option string directly into the entry field
frequency_selector.set("Direct Audio Feed")

# Query current state value string or toggle operational availability cleanly
current_mode = frequency_selector.get_state()  # Returns 'normal' or 'disabled'
frequency_selector.state("disabled")            # Locks interaction layers and dims inner buttons
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkComboBox": {
        "font": ["Arial", 15, "normal"],
        "dropdown_font": ["Arial", 15, "normal"],
        "border_width": 1.5,
        "border_color": ["#1A4375", "#64748B"],
        "fg_color": ["#FFFFFF", "#111827"],
        "text_color": ["#1F2937", "#FFFFFF"],
        "button_color": ["#2471A3", "#64748B"],
        "button_hover_color": ["#112A4B", "#1F618D"],
        "dropdown_fg_color": ["#FFFFFF", "#1F2937"],
        "dropdown_text_color": ["#1F2937", "#F9FAFB"],
        "dropdown_hover_color": ["#E5E7EB", "#374151"],
        "disabled_map": {
            "fg_color": ["#F3F4F6", "#1F2937"],
            "border_color": ["#E5E7EB", "#374151"],
            "text_color": ["#94A3B8", "#64748B"],
            "button_color": ["#94A3B8", "#4B5563"]
        }
    }
}
```

### Other notes
* **Composite State Cascading:** Transitioning to `disabled` cleanly applies dimming array variables across the text fields, structural bounding rims, and arrow dropdown boxes simultaneously.
* **Pygubu Zone-A Interception:** The widget safely responds to single positional property queries coming from design-time editor tools without crashing or locking execution tracks.

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed the `sCTkComboBox` inside a root window workspace panel layout using the strict interactive test configuration loops.

```python
import customtkinter as ctk
from sCTkComboBox import sCTkComboBox

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x200")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # Instantiate with dummy options test list array values and click reporter logs
    widget = sCTkComboBox(
        base,
        values=["Channel A (VHF)", "Channel B (UHF)", "Direct Audio Feed"],
        command=lambda choice: print(f"ComboBox Option Latched: {choice}")
    )
    widget.pack(expand=True, fill="none", padx=10, pady=10)

    # Test tracking loop sequences on your console window
    widget.state("disabled")
    print("state (Disabled Pass) =", widget.get_state())  # Output: disabled

    widget.state("normal")
    print("state (Normal Pass)   =", widget.get_state())  # Output: normal

    root.mainloop()
```


[Return to Table of Contents](#contents)


