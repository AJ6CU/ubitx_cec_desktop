## sCTkEntryPrimary

Dominant form input lane widget variant designed for primary user data entry (e.g., core configuration inputs, direct numeric entries, or text queries). It implements a deep-copy keyword caching shield to protect the text field layout engine from validation failures.

*For alternative helper input fields or metadata input channels, see the companion component documentation page:* [sCTkEntrySecondary](sCTkEntrySecondary.md).

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkEntry(master)` | `sCTkEntryPrimary(master)` *(Primary form data field)* |
| **Maintenance** | Local style overrides duplicated across files manually. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Everything runs under one core native text pipeline. | Separated safely across `sCTkEntryPrimary.py`, `sCTkEntryPrimaryui.py`, and `ThemeableWidget.py`. |
| `state(mode)` | `self.configure(state=...)` | `Method (str)` handling layout tracking map transformations (`'normal'`, `'disabled'`). |
| `get_state()` | `self.cget("state")` | `Method -> str` explicit verification query matching system test assertions. |

---

### Constructor

Initialize a custom primary form data field instance. High-level configuration parameters like `textvariable` and `placeholder_text` are explicitly popped early inside `__init__` to protect the layout engine from keyword collisions.

```python
# Instantiate a primary user entry field
frequency_input = sCTkEntryPrimary(
    master=control_panel,
    placeholder_text="Enter Transceiver Frequency...",
    textvariable=vfo_string_var
)

# Render the widget inside your parent container coordinate tracker panel
frequency_input.pack(fill="x", padx=40, pady=10)
```

---

### Convenience Functions
```python
# Selectively manipulate the internal textual elements on the fly
frequency_input.insert(0, "14.032.000") # Populates text buffer indices with data strings
frequency_input.delete(0, "end")         # Wipes the entry line lane completely back to empty
active_buffer = frequency_input.get()    # Queries the live active text character arrays

# Evaluate current state configurations or apply absolute user interaction locks
current_mode = frequency_input.get_state() # Returns 'normal' or 'disabled'
frequency_input.state("disabled")          # Locks data entry tracks and applies muted gray fills
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkEntryPrimary": {
        "fg_color": ["#FFFFFF", "#111827"],
        "border_color": ["#1A4375", "#4B5563"],
        "text_color": ["#1F2937", "#FFFFFF"],
        "placeholder_text_color": ["#94A3B8", "#64748B"],
        "disabled_map": {
            "fg_color": ["#F3F4F6", "#1F2937"],
            "border_color": ["#E5E7EB", "#374151"],
            "text_color": ["#94A3B8", "#64748B"],
            "placeholder_text_color": ["#CBD5E1", "#475569"]
        }
    }
}
```

### Other notes
* **Deep-Copy Dictionary Isolation Shield:** Because CustomTkinter's native entry initialization code mutates, strips, and deletes keys directly out of raw dictionary data footprints during its boot phase, the constructor clones your configurations into `self._local_defaults = dict(self.final_kw)` beforehand. This prevents normal state restorations from crashing on missing keys.
* **Null Pointer Prevention Filters:** The internal visual loop is fortified to look up CustomTkinter's master `ThemeManager` variables if a specific color style (like `placeholder_text_color`) is completely skipped inside `themes.json`, blocking dangerous `None` keyword objects from halting application threads.


### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly map an `sCTkFrame` asset container.

```python
# !/usr/bin/python3
"""
sCTkEntryPrimary - Standalone Interactive Testing Harness
"""
import customtkinter as ctk
from sCTkFrame import sCTkFrame
from sCTkEntryPrimary import sCTkEntryPrimary
from sCTkLabelSecondary import sCTkLabelSecondary


def toggle_operational_state():
    """Toggles the input lane between normal active and dimmed disabled profiles."""
    current_mode = input_field.get_state()
    target = "disabled" if current_mode == "normal" else "normal"

    input_field.configure(state=target)
    btn_toggle.configure(text="Lock Input (Set 'disabled')" if target == "normal" else "Unlock Input (Set 'normal')")
    print(f"Logged Verification Hook -> input_field.get_state() = {input_field.get_state()}")


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("450x260")
    root.title("sCTkEntryPrimary Testing Deck")

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # Label notice layer to catch floating text changes
    lbl_monitor = sCTkLabelSecondary(base, text="Console monitor active...")
    lbl_monitor.pack(pady=10)

    # Instantiate your custom input widget field
    input_field = sCTkEntryPrimary(base, placeholder_text="Enter Transceiver Frequency...")
    input_field.pack(expand=False, fill="x", padx=40, pady=10)

    # Attach interactive keyboard binding tracker to dump text entries straight to terminal loop
    input_field.bind("<KeyRelease>", lambda e: lbl_monitor.configure(text=f"Live Buffer: {input_field.get()}"))

    btn_toggle = ctk.CTkButton(base, text="Lock Input (Set 'disabled')", command=toggle_operational_state)
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