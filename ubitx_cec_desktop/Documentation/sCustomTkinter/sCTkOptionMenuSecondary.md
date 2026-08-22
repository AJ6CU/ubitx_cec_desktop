## sCTkOptionMenuSecondary

A cleanly bordered, composite layout option menu component widget variant designed for secondary, auxiliary, or helper data slot selections (e.g., bandwidth filters, squelch limits, or offset increments). 

It inherits directly from a native `ctk.CTkFrame` chassis on the exterior while embedding a highly customized `ctk.CTkOptionMenu` on the interior. It applies a dynamic attribute lookup loop and a structural constructor default floor to guarantee total Pygubu Designer layout inspection stability and prevent `NoneType` math scaling crashes.

*For primary system control selectors or dominant operating mode drop-downs, see the main component documentation page:* [sCTkOptionMenuPrimary](sCTkOptionMenuPrimary.md).

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkOptionMenu(master)` | `sCTkOptionMenuSecondary(master)` *(Bordered composite dropdown)* |
| **Maintenance** | Local style overrides duplicated across files manually. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Component logic nested inside single tracking arrays. | Separated safely across `sCTkOptionMenuSecondary.py` and `ThemeableWidget.py`. |
| `state(mode)` | `self.configure(state=...)` | `Method (str)` handling layout tracking map transformations (`'normal'`, `'disabled'`). |
| `get_state()` | `self.cget("state")` | `Method -> str` explicit verification query matching system test assertions. |
| `update_list(list, idx)` | *Not Available Natively* | **Helper Pass:** Dynamically updates items and sets default indices safely. |

---

### Constructor

Initialize a custom secondary composite option selection dropdown instance. Sub-component parameters like `values`, `command`, and `variable` are explicitly popped early inside `__init__` to protect the layout engine from keyword collisions. Signature defaults are explicitly declared to shield standalone automated test runs.

```python
# Instantiate a secondary bordered option selection dropdown (Ghost style alignment)
filter_options = ["Filter: 2.4KHz", "Filter: 1.8KHz", "Filter: 500Hz", "Filter: 250Hz"]

bandwidth_selector = sCTkOptionMenuSecondary(
    master=control_panel,
    values=filter_options,
    command=on_bandwidth_filter_selected
)

# Render the widget inside your parent container coordinate tracker panel
bandwidth_selector.pack(fill="x", padx=40, pady=10)
```

---

### Convenience Functions
```python
# Query current selections or force alternative text positions on the fly
active_filter = bandwidth_selector.get() # Queries the active text string visible on the button face
bandwidth_selector.set("Filter: 500Hz")   # Manually updates the displayed text choice selection target

# Dynamically re-populate option menu arrays without throwing layout bugs
new_steps = ["Step: 10Hz", "Step: 50Hz", "Step: 100Hz"]
bandwidth_selector.update_list(new_steps, default_index=2) # Re-populates list and selects "Step: 100Hz"

# Evaluate current state configurations or apply absolute user interaction locks
current_mode = bandwidth_selector.get_state() # Returns 'normal' or 'disabled'
bandwidth_selector.state("disabled")           # Locks down the menu dropdown arrow and applies muted gray fills
```

### Centralized Stylesheet Setup (`sCTkThemes.json`)

To synchronize its outline styles flawlessly with your standard Ghost buttons, ensure the configuration hex codes are matched perfectly:

```json
{
    "sCTkOptionMenuSecondary": {
        "fg_color": "transparent",
        "border_color": ["#CBD5E1", "#44403C"],
        "text_color": ["#334155", "#E7E5E4"],
        "border_width": 1,
        "corner_radius": 4,
        "disabled_map": {
            "fg_color": ["#F1F5F9", "#171412"],
            "border_color": ["#E2E8F0", "#292524"],
            "text_color": ["#94A3B8", "#57534E"]
        }
    }
}
```

### Other notes
* **Open-Closed Extensibility Loop:** The visual router contains zero hardcoded widget property name lookups. It maps styles by looping directly over the active keys defined inside `sCTkThemes.json`, allowing you to append new future configurations seamlessly without editing the class file.
* **Pygubu Designer Integration:** Overrides standard positional configuration intercepts (`Zone A`) to report accurate single-string metrics directly back to Pygubu's workspace preview manager, keeping properties cleanly queryable.

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed an `sCTkOptionMenuSecondary` alongside a live telemetry monitor.

```python
#!/usr/bin/python3
import customtkinter as ctk
from sCTkFrame import sCTkFrame
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkOptionMenuSecondary import sCTkOptionMenuSecondary
import sCTkThemes
# =====================================================================
# 🛠️ INTEGRATED REPOSITORY COMPLIANT INLINE TESTING HARNESS
# =====================================================================


if __name__ == "__main__":
    
    sCTkThemes.apply_sCTkThemes()
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
    option_menu = sCTkOptionMenuSecondary(
        base, 
        values=["Initial Data Track A", "Initial Data Track B"],
        command=lambda choice: lbl_data.configure(text=f"Selection Captured: {choice}")
    )
    option_menu.pack(fill="x", padx=40, pady=10)

    # 4. Dynamically update options and set default tracking location
    option_menu.update_list(["Filter: Narrow", "Filter: Medium", "Filter: Wide"], default_index=0)

    root.mainloop()
```
