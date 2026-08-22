## sCTkLabelSecondary

Intermediate sub-section label widget variant that natively intercepts state assignments to swap active vs desaturated text color matrices seamlessly across system appearance mode switches.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkLabel(master)` | `sCTkLabelSecondary(master)` *(Secondary metadata readout)* |
| **Maintenance** | Local style configurations duplicated manually across widgets. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Runs natively via a single core text pipeline tracker. | Separated safely across `sCTkLabelSecondary.py`, `sCTkLabelSecondaryui.py`, and `ThemeableWidget.py`. |
| `state(mode)` | *Not Available Natively* | `Method (str)` handling layout tracking map transformations (`'normal'`, `'disabled'`). |
| `get_state()` | *Not Available Natively* | `Method -> str` explicit verification query matching system test assertions. |

---

### Constructor

Initialize an intermediate informational tracking text widget instance. Inline styling overrides take total preference over your central style files.

```python
# Instantiate a clean theme-compliant informational readout tag
telemetry_label = sCTkLabelSecondary(
    master=workspace_frame,
    text="SYSTEM READY: VFO TRACKING DISPATCHED"
)

# Render the layout inside your parent container geometry packer grid
telemetry_label.pack(pady=10)
```

---

### Convenience Functions
```python
# Query current operational status or swap text contrast layouts cleanly
current_look = telemetry_label.get_state()   # Returns 'normal' or 'disabled'
telemetry_label.state("disabled")            # Intercepts the key and drops text contrast to muted tones
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkLabelSecondary": {
        "text_color": ["#1A4375", "#FFFFFF"],
        "font": ["Arial", 11, "bold"],
        "disabled_map": {
            "text_color": ["#94A3B8", "#64748B"]
        }
    }
}
```

### Other notes
* **System Mode Alignment:** If layout color tracking dictionaries are empty, the component falls back to CustomTkinter's master `ThemeManager` lookup block, allowing the OS to automatically change text to high-contrast white in Dark Mode.
* **Boot Cascade Protection:** Strips out early boot-time guessing loops entirely, allowing operating system appearance choices to flow through without hardcoding.

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to verify the text contrast transformations.

```python
import customtkinter as ctk
from sCTkLabelSecondary import sCTkLabelSecondary

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("300x150")

    lbl = sCTkLabelSecondary(root, text="MONITOR READING ACTIVE")
    lbl.pack(pady=20)

    # Transition straight into a dimmed disabled style profile state
    lbl.state("disabled")
    print(f"Logged Verification Assert Token = {lbl.get_state()}")
    
    root.mainloop()
```
