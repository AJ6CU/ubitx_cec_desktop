## sCTkFrame

Standardized, theme-compliant layout container frame acting as a clean wrapper panel layer protected against Pygubu Designer property interrogation resets.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkFrame(master)` | `sCTkFrame(master)` *(Functions as Layout Container Base)* |
| **Maintenance** | Localized styling properties duplicated manually. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Everything runs under one core native pipeline. | Separated safely across `sCTkFrame.py`, `sCTkFrameui.py`, and `ThemeableWidget.py`. |
| `state(mode)` | *Not Available Natively* | `Method (str)` acting as a safe operational pass-through tracker (`'normal'`). |
| `get_state()` | *Not Available Natively* | `Method -> str` explicit getter returning default active framework modes. |

---

### Constructor

Initialize a custom structural frame panel layer container instance. Keyword arguments layer cleanly over centralized file defaults.

```python
# Instantiate a clean theme-compliant container panel
workspace_card = sCTkFrame(
    master=root_window,
    corner_radius=8,
    border_width=1
)

# Pack container securely within your primary coordinate track grid layout
workspace_card.pack(fill="both", expand=True, padx=15, pady=15)
```

---

### Convenience Functions
```python
# Safe operational pass-through wrappers keep hierarchy calls from throwing AttributeError crashes
current_status = workspace_card.get_state()  # Returns 'normal'
workspace_card.state("disabled")             # Gracefully absorbs keyword without throwing frame bugs
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkFrame": {
        "fg_color": ["#FFFFFF", "#1E1E1E"],
        "border_color": ["#E2E8F0", "#2D2D2D"],
        "corner_radius": 6
    }
}
```

### Other notes
* **Pygubu Inspector Intercepts:** `Zone A` handles singular descriptive lookups natively to ensure designer layouts do not reject custom layout frames.
* **Pure Container Handoff:** Contains zero heavy state tracking loops or state tracking variables, preserving structural rendering performance.

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly map an `sCTkFrame` asset container.

```python
import customtkinter as ctk
from sCTkFrame import sCTkFrame

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("300x150")

    panel = sCTkFrame(root)
    panel.pack(expand=True, fill="both", padx=20, pady=20)

    print(f"Container Layout Operational Status: {panel.get_state().upper()}")
    root.mainloop()
```
