## sCTkEntrySecondary

Minimalist form input lane widget variant designed for secondary or auxiliary data capture (e.g., configuration metadata, helper notations, or minor parameters). It replicates the exact deep-copy keyword caching shield and parameter-popping architecture utilized by the primary text fields to guarantee framework execution stability.

*For principal user input fields or primary numeric entry tracks, see the main component documentation page:* [sCTkEntryPrimary](sCTkEntryPrimary.md).

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkEntry(master)` | `sCTkEntrySecondary(master)` *(Secondary helper field)* |
| **Maintenance** | Local style overrides duplicated across files manually. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Everything runs under one core native text pipeline. | Separated safely across `sCTkEntrySecondary.py`, `sCTkEntrySecondaryui.py`, and `ThemeableWidget.py`. |
| `state(mode)` | `self.configure(state=...)` | `Method (str)` handling layout tracking map transformations (`'normal'`, `'disabled'`). |
| `get_state()` | `self.cget("state")` | `Method -> str` explicit verification query matching system test assertions. |

---

### Constructor

Initialize a custom secondary metadata entry lane instance. Sub-component parameters like `textvariable` and `placeholder_text` are explicitly popped early inside `__init__` to protect the layout engine from keyword collisions.

```python
# Instantiate a secondary helper input field
metadata_input = sCTkEntrySecondary(
    master=control_panel,
    placeholder_text="Enter configuration metadata..."
)

# Render the widget inside your parent container coordinate tracker panel
metadata_input.pack(fill="x", padx=40, pady=10)
```

---

### Convenience Functions
```python
# Selectively manipulate the internal textual elements on the fly
metadata_input.insert(0, "RIG_REV_C2")  # Populates text buffer indices with data strings
metadata_input.delete(0, "end")         # Wipes the entry line lane completely back to empty
active_buffer = metadata_input.get()    # Queries the live active text character arrays

# Evaluate current state configurations or apply absolute user interaction locks
current_mode = metadata_input.get_state() # Returns 'normal' or 'disabled'
metadata_input.state("disabled")          # Locks data entry tracks and applies muted gray fills
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkEntrySecondary": {
        "fg_color": ["#F8FAFC", "#1F2937"],
        "border_color": ["#94A3B8", "#4B5563"],
        "text_color": ["#334155", "#E2E8F0"],
        "placeholder_text_color": ["#94A3B8", "#4B5563"],
        "disabled_map": {
            "fg_color": ["#F1F5F9", "#111827"],
            "border_color": ["#E2E8F0", "#374151"],
            "text_color": ["#94A3B8", "#64748B"],
            "placeholder_text_color": ["#CBD5E1", "#475569"]
        }
    }
}
```

### Other notes
* **Deep-Copy Dictionary Isolation Shield:** Because CustomTkinter's native entry initialization code mutates, strips, and deletes keys directly out of raw dictionary data footprints during its boot phase, the constructor clones your configurations into `self._local_defaults = dict(self.final_kw)` beforehand. This prevents normal state restorations from crashing on missing keys.
* **Null Pointer Prevention Filters:** The internal visual loop is fortified to look up CustomTkinter's master `ThemeManager` variables if a specific color style (like `placeholder_text_color`) is completely skipped inside `themes.json`, blocking dangerous `None` keyword objects from halting application threads.

```python
# !/usr/bin/python3
"""
sCTkEntrySecondary - Standalone Interactive Testing Harness
"""
import customtkinter as ctk
from sCTkFrame import sCTkFrame
# from sCTkEntrySecondary import sCTkEntrySecondary
from sCTkLabelSecondary import sCTkLabelSecondary


def toggle_operational_state():
    """Toggles the helper input field between normal active and dimmed disabled profiles."""
    current_mode = input_field.get_state()
    target = "disabled" if current_mode == "normal" else "normal"

    input_field.configure(state=target)
    btn_toggle.configure(
        text="Lock Helper Input (Set 'disabled')" if target == "normal" else "Unlock Helper Input (Set 'normal')")
    print(f"Logged Verification Hook -> input_field.get_state() = {input_field.get_state()}")


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("450x260")
    root.title("sCTkEntrySecondary Testing Deck")

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # Label notice layer to monitor buffer array activity
    lbl_monitor = sCTkLabelSecondary(base, text="Console monitor active...")
    lbl_monitor.pack(pady=10)

    # Instantiate your custom secondary helper field
    input_field = sCTkEntrySecondary(base, placeholder_text="Enter configuration metadata...")
    input_field.pack(expand=False, fill="x", padx=40, pady=10)

    # Monitor keystrokes live
    input_field.bind("<KeyRelease>", lambda e: lbl_monitor.configure(text=f"Live Buffer: {input_field.get()}"))

    btn_toggle = ctk.CTkButton(base, text="Lock Helper Input (Set 'disabled')", command=toggle_operational_state)
    btn_toggle.pack(side="bottom", pady=15)

    # Run the interactive boot tracking logs
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    input_field.state("disabled")
    print("state (Disabled Pass) =", input_field.get_state())  # Output: disabled

    input_field.state("normal")
    print("state (Normal Pass)   =", input_field.get_state())  # Output: normal
    print("========================================\n")

    root.mainloop()
```