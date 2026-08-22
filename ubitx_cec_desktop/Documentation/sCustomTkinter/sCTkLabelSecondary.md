## sCTkLabelSecondary

### Table of Contents
* [API Property Reference](#api-property-reference)
* [Constructor](#constructor)
* [Centralized Stylesheet Setup](#centralized-stylesheet-setup-sctkthemesjson)
* [Other Notes](#other-notes)
* [Implementation Example & Test Harness](#implementation-example--test-harness)

---

The intermediate sub-section display typography label widget component. It features an independent deep-copy keyword caching shield and an advanced multi-state color-dimming interceptor to automatically shift text contrasts when subsystem components enter disabled sequences.

*For dominant main dashboard header components, see the companion component documentation page:* [sCTkLabelPrimary](sCTkLabelPrimary.md).

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkLabel(master)` | `sCTkLabelSecondary(master)` *(Intermediate Section Typography)* |
| **File Mapping** | Direct module definitions run without structured configuration. | Separated safely across `sCTkLabelSecondary.py` and `ThemeableWidget.py`. |
| **State Lock** | *Not Supported Natively* | `test_label.state("disabled")`<br>**OR**<br>`test_label.configure(state="disabled")`<br><br>**Framework-Wide State Support:** Natively supported across all label components (`Primary`, `Secondary`, `Tertiary`). It intercepts state configuration calls and dynamically dims typography layouts based on centralized `disabled_map` metrics. |
| `get_state()` | *Not Supported Natively* | `Method -> str` explicit verification query matching system test assertions. |

---

### Constructor

Initialize a custom secondary intermediate label instance. Configuration metrics map cleanly out of central stylesheet parameters.

```python
# Instantiate a secondary intermediate dashboard label element
panel_sub_label = sCTkLabelSecondary(
    master=control_panel,
    text="VFO STATUS PANEL: ACTIVE"
)

# Render the widget inside your layout panel using geometry managers
panel_sub_label.pack(expand=True, pady=10)
```

---

### Centralized Stylesheet Setup (`sCTkThemes.json`)
```json
{
    "sCTkLabelSecondary": {
        "fg_color": "transparent",
        "text_color": ["#475569", "#CBD5E1"],
        "font": ["Arial", 11, "bold"],
        "disabled_map": {
            "text_color": ["#94A3B8", "gray50"]
        }
    }
}
```

### Other notes
* **Deep-Copy Dictionary Isolation Shield:** Because CustomTkinter's native geometry constructor routines mutate and drop keys directly out of parsed configuration structures during early boot phases, the constructor clones your data configurations into `self._local_defaults = dict(self.final_kw)` beforehand. This prevents layout repaints from failing.
* **Dynamic Dark Mode Pass-Through:** When returning to an active state, the visual interceptor reads directly from your protected `_local_defaults` cache. If no hardcoded text color is explicitly discovered, it hands control back to CustomTkinter's master `ThemeManager` to natively paint high-contrast system fonts.

---

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed an `sCTkLabelSecondary` sub-section element along with an interactive status switch toggle.

```python
#!/usr/bin/python3
"""
sCTkLabelSecondary - Standalone Interactive Testing Harness
"""
import customtkinter as ctk

# =====================================================================
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import sCTkThemes                    # 🔍 Duplicate import kept close for script scannability
from sCTkFrame import sCTkFrame      # Testing application wrapper container frame
from sCTkLabelSecondary import sCTkLabelSecondary

if __name__ == "__main__":
    # Natively resolves your package assets and populates configurations cleanly
    sCTkThemes.apply_sCTkThemes()

    root = ctk.CTk()
    root.geometry("450x280")
    root.title("sCTkLabelSecondary Testing Deck")

    # Layout a clean, padded workspace container
    container = sCTkFrame(root, fg_color="transparent")
    container.pack(expand=True, fill="both", padx=30, pady=30)

    # Instantiate your custom secondary label targeting your name registry
    test_label = sCTkLabelSecondary(container, text="VFO STATUS PANEL: ACTIVE")
    test_label.pack(expand=True, pady=10)

    # Live state monitoring feedback label
    lbl_status = ctk.CTkLabel(container, text="Current State Assertion: NORMAL", font=("Arial", 10, "italic"))
    lbl_status.pack(side="bottom", pady=5)

    def toggle_label_states():
        """Cycles the label states between normal active and dimmed disabled profiles."""
        current_state = test_label.state()
        target = "disabled" if current_state == "normal" else "normal"

        # Explicitly testing the dual-routing capability via configure()
        test_label.configure(state=target)
        
        if target == "disabled":
            btn_toggle.configure(text="Activate Label (Set 'normal')")
            lbl_status.configure(text="Current State Assertion: DISABLED")
        else:
            btn_toggle.configure(text="Dim Label (Set 'disabled')")
            lbl_status.configure(text="Current State Assertion: NORMAL")

        # Log state queries to terminal to match your standalone harness requirements
        print(f"Logged Verification Hook -> test_label.get_state() = {test_label.get_state()}")

    # Standard interaction trigger button to dispatch state transformations
    btn_toggle = ctk.CTkButton(
        container,
        text="Dim Label (Set 'disabled')",
        command=toggle_label_states,
        fg_color=("#2471A3", "#3B8ED0"),
        hover_color=("#112A4B", "#1F6AA5")
    )
    btn_toggle.pack(expand=True, pady=15)

    # Run the interactive boot tracking validation checks
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    test_label.state("disabled")
    print(f"state (Disabled Pass) = {test_label.get_state().upper()}")

    test_label.state("normal")
    print(f"state (Normal Pass)   = {test_label.get_state().upper()}")
    print("========================================\n")

    root.mainloop()
```

[Return to Table of Contents](#contents)
