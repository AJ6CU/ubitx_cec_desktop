## sCTkEntrySecondary

### Table of Contents
* [API Property Reference](#api-property-reference)
* [Constructor](#constructor)
* [Convenience Functions](#convenience-functions)
* [Centralized Stylesheet Setup](#centralized-stylesheet-setup-themesjson)
* [Other Notes](#other-notes)
* [Implementation Example & Test Harness](#implementation-example--test-harness)

---

Auxiliary / secondary metadata input lane widget variant designed for secondary data capture (e.g., logging channels, station call signs, panel notes, or sub-metadata queries) [INDEX].

*For dominant form input fields or direct operational data entry channels, see the primary component documentation page:* [sCTkEntryPrimary](sCTkEntryPrimary.md).

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkEntry(master)` | `sCTkEntrySecondary(master)` *(Secondary metadata field)* |
| **Maintenance** | Local style overrides duplicated across files manually. | Clean updates across all layouts modified directly in the JSON file [INDEX]. |
| **File Mapping** | Everything runs under one core native text pipeline. | Separated safely across `sCTkEntrySecondary.py`, `sCTkEntrySecondaryui.py`, and `ThemeableWidget.py` [INDEX]. |
| **State Lock** | `self.configure(state="disabled")` | `input_field.state("disabled")`<br>**OR**<br>`input_field.configure(state="disabled")`<br><br>**Dual-Routing State Pipeline:** Natively handles both syntax paths [INDEX]. Freezes text interaction lanes, blocks keyboard event streams, and dynamically shifts colors out of `disabled_map` guidelines [INDEX]. |
| `get_state()` | `self.cget("state")` | `Method -> str` explicit verification query matching system test assertions [INDEX]. |

---

### Constructor

Initialize a custom secondary data field instance. High-level configuration parameters like `textvariable` and `placeholder_text` are explicitly popped early inside `__init__` to protect the layout engine from keyword collisions [INDEX].

```python
# Instantiate a secondary metadata user entry field
callsign_input = sCTkEntrySecondary(
    master=control_panel,
    placeholder_text="Enter Station Call Sign...",
    textvariable=callsign_string_var
)

# Render the widget inside your parent container coordinate tracker panel
callsign_input.pack(fill="x", padx=40, pady=10)
```

---

### Convenience Functions
```python
# Selectively manipulate the internal textual elements on the fly
callsign_input.insert(0, "W1AW")         # Populates text buffer indices with data strings [INDEX]
callsign_input.delete(0, "end")          # Wipes the entry line lane completely back to empty [INDEX]
active_buffer = callsign_input.get()     # Queries the live active text character arrays [INDEX]

# Evaluate current state configurations or apply absolute user interaction locks via dual-routing syntax
current_mode = callsign_input.get_state() # Returns 'normal' or 'disabled' [INDEX]
callsign_input.state("disabled")           # Locks data entry tracks and applies muted gray fills [INDEX]
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkEntrySecondary": {
        "fg_color": ["#F8FAFC", "#111827"],
        "border_color": ["#94A3B8", "#374151"],
        "text_color": ["#475569", "#94A3B8"],
        "placeholder_text_color": ["#94A3B8", "#475569"],
        "disabled_map": {
            "fg_color": ["#F1F5F9", "#171412"],
            "border_color": ["#E2E8F0", "#292524"],
            "text_color": ["#94A3B8", "#57534E"],
            "placeholder_text_color": ["#E5E7EB", "#1C1917"]
        }
    }
}
```

### Other notes
* **Deep-Copy Dictionary Isolation Shield:** Because CustomTkinter's native entry initialization code mutates, strips, and deletes keys directly out of raw dictionary data footprints during its boot phase, the constructor clones your configurations into `self._local_defaults = dict(self.final_kw)` beforehand. This prevents normal state restorations from crashing on missing keys [INDEX].
* **Bounded Dynamic Filter Loop:** The visual router is fortified to dynamically loop across active values inside your protected `_local_defaults` memory cache, dropping omitted parameters completely rather than passing raw `None` pointers. This allows CustomTkinter's built-in theme parameters to step forward natively, blocking dangerous type validation exceptions [INDEX].

---

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed an `sCTkEntrySecondary` input lane field along with an interactive status switch toggle [INDEX].

```python
#!/usr/bin/python3
"""
sCTkEntrySecondary - Standalone Interactive Testing Harness
"""
import customtkinter as ctk

# =====================================================================
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import sCTkThemes                # 🔍 Duplicate import kept close for script scannability
from sCTkFrame import sCTkFrame  # Testing application wrapper container frame
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkEntrySecondary import sCTkEntrySecondary

if __name__ == "__main__":
    # Natively resolves your package assets and populates configurations cleanly [INDEX]
    sCTkThemes.apply_sCTkThemes()

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

    def toggle_operational_state():
        """Toggles the helper input field between normal active and dimmed disabled profiles [INDEX]."""
        current_mode = input_field.get_state()
        target = "disabled" if current_mode == "normal" else "normal"

        # Explicitly testing the dual-routing capability via configure()
        input_field.configure(state=target)
        btn_toggle.configure(
            text="Lock Helper Input (Set 'disabled')" if target == "normal" else "Unlock Helper Input (Set 'normal')")
        print(f"Logged Verification Hook -> input_field.get_state() = {input_field.get_state()}")

    btn_toggle = ctk.CTkButton(base, text="Lock Helper Input (Set 'disabled')", command=toggle_operational_state)
    btn_toggle.pack(side="bottom", pady=15)

    # Run the interactive boot tracking logs [INDEX]
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    input_field.state("disabled")
    print("state (Disabled Pass) =", input_field.get_state())  # Output: disabled [INDEX]

    input_field.state("normal")
    print("state (Normal Pass)   =", input_field.get_state())  # Output: normal [INDEX]
    print("========================================\n")

    root.mainloop()
```

[Return to Table of Contents](#contents)
