## sCTkLabelTertiary

Minimalist description, status sub-text, and inline notice label widget variant. Natively intercepts state assignments to fade notation details into desaturated styling tracks when components lock down.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkLabel(master)` | `sCTkLabelTertiary(master)` *(Inline description notation)* |
| **Maintenance** | Local style overrides duplicated across files manually. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Everything runs under one core native text pipeline. | Separated safely across `sCTkLabelTertiary.py`, `sCTkLabelTertiaryui.py`, and `ThemeableWidget.py`. |
| `state(mode)` | *Not Available Natively* | `Method (str)` handling layout tracking map transformations (`'normal'`, `'disabled'`). |
| `get_state()` | *Not Available Natively* | `Method -> str` explicit verification query matching system test assertions. |

---

### Constructor

Initialize a custom description notice label instance. Direct initialization keywords take immediate preference over system JSON profiles.

```python
# Instantiate a clean theme-compliant informational description tag
notice_tag = sCTkLabelTertiary(
    master=footer_frame,
    text="Notice: VFO VFO boundary locked to licensed band spacing limits."
)

# Render the layout inside your parent container coordinate packer
notice_tag.pack(side="left", padx=10, pady=5)
```

---

### Convenience Functions
```python
# Evaluate active visual modes or clear interaction visibility tracks safely
current_look = notice_tag.get_state()   # Returns 'normal' or 'disabled'
notice_tag.state("disabled")            # Softens the typography line color completely
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkLabelTertiary": {
        "text_color": ["#4B5563", "#9CA3AF"],
        "font": ["Arial", 10, "italic"],
        "disabled_map": {
            "text_color": ["#CBD5E1", "#374151"]
        }
    }
}
```

### Other notes
* **Zero Boot Guessing Interference:** Completely bypasses runtime `_apply_appearance_mode()` loops during initialization, unblocking CustomTkinter's native tracker from capturing the operating system background preference seamlessly.
* **Fallback Cascade Handling:** If specific styling coordinates are omitted from `themes.json`, the class falls back onto primary metadata slots to prevent component rendering faults.

### Implementation Example & Test Harness

Below is a complete script demonstrating how to deploy an `sCTkLabelTertiary` instance within a standard panel wrapper.

```python
import customtkinter as ctk
from sCTkLabelTertiary import sCTkLabelTertiary

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("300x120")

    caption = sCTkLabelTertiary(root, text="Tracking step: 100Hz intervals")
    caption.pack(pady=20)
    
    caption.state("disabled")
    print(f"Caption Status Assert Loop: {caption.get_state().upper()}")
    root.mainloop()
```
