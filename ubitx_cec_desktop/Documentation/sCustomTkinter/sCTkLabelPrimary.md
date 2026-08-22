## sCTkLabelPrimary

Dominant headline and section header label widget variant. Natively intercepts state assignments to swap active high-contrast header colors with desaturated disabled configurations cleanly.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkLabel(master)` | `sCTkLabelPrimary(master)` *(Dominant layout header title)* |
| **Maintenance** | Local style overrides duplicated across files manually. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Everything runs under one core native text pipeline. | Separated safely across `sCTkLabelPrimary.py`, `sCTkLabelPrimaryui.py`, and `ThemeableWidget.py`. |
| `state(mode)` | *Not Available Natively* | `Method (str)` handling layout tracking map transformations (`'normal'`, `'disabled'`). |
| `get_state()` | *Not Available Natively* | `Method -> str` explicit verification query matching system test assertions. |

---

### Constructor

Initialize a custom prominent header instance. Inline layout styling parameters passed here layer natively over centralized JSON stylesheet presets.

```python
# Instantiate a clean theme-compliant application master header
header_title = sCTkLabelPrimary(
    master=top_banner_frame,
    text="MAIN HF TRANSMITTER PANEL"
)

# Render the layout inside your parent container geometry packer grid
header_title.pack(pady=(15, 5))
```

---

### Convenience Functions
```python
# Query current operational status or swap header text contrast levels cleanly
current_state = header_title.get_state()   # Returns 'normal' or 'disabled'
header_title.state("disabled")             # Drops title text focus down to flat muted styles
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkLabelPrimary": {
        "text_color": ["#111827", "#F9FAFB"],
        "font": ["Arial", 18, "bold"],
        "disabled_map": {
            "text_color": ["#94A3B8", "#4B5563"]
        }
    }
}
```

### Other notes
* **OS-Native Default Resolution:** When your style dictionary configuration is unmapped, the class automatically tracks CustomTkinter's baseline theme list, allowing the operating system to paint crisp high-visibility white characters in Dark Mode out of the box.
* **Pygubu Inspector Intercepts:** `Zone A` handles descriptive single-string inspector lookups securely to prevent designer previews from breaking.

### Implementation Example & Test Harness

Below is a complete script demonstrating how to deploy an `sCTkLabelPrimary` instance within a standard grid wrapper block.

```python
import customtkinter as ctk
from sCTkLabelPrimary import sCTkLabelPrimary

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("300x120")

    header = sCTkLabelPrimary(root, text="CONTROL CONTROL ACTIVE")
    header.pack(pady=20)
    
    print(f"Header Initialization Pass: {header.get_state().upper()}")
    root.mainloop()
```
