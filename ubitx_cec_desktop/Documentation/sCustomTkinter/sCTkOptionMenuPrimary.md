## sCTkOptionMenuPrimary

### Table of Contents
* [API Property Reference](#api-property-reference)
* [Constructor](#constructor)
* [Convenience Functions](#convenience-functions)
* [Centralized Stylesheet Setup](#centralized-stylesheet-setup-themesjson)
* [Other Notes](#other-notes)
* [Implementation Example & Test Harness](#implementation-example--test-harness)

---

The dominant primary option menu selector drop-down widget component. It incorporates early parameter popping filters and an independent value-cloned deep copy caching layer to guarantee composite drop-down states remain permanently insulated against native CustomTkinter initialization dictionary data loss.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkOptionMenu(master)` | `sCTkOptionMenuPrimary(master)` *(Primary Drop-Down Menu)* |
| **File Mapping** | Direct layouts bundle under unconfig-managed files. | Separated safely across `sCTkOptionMenuPrimary.py` and `ThemeableWidget.py`. |
| **State Lock** | `self.configure(state="disabled")` | `menu_field.state("disabled")`<br>**OR**<br>`menu_field.configure(state="disabled")`<br><br>**Dual-Routing State Pipeline:** Natively intercepts state calls, unbinding drop-down trigger events while shifting background contrast rules safely out of `disabled_map` metrics. |
| `get_state()` | `self.cget("state")` | `Method -> str` explicit verification query matching system test assertions. |

---

### Constructor

Initialize a custom primary drop-down menu instance. High-level configuration parameters like `values`, `command`, and `variable` are explicitly popped early inside `__init__` to protect the layout engine from keyword collisions.

```python
# Instantiate a primary operational mode selection option menu
mode_dropdown = sCTkOptionMenuPrimary(
    master=control_panel,
    values=["Mode 1: Upper Sideband", "Mode 2: Lower Sideband", "Mode 3: Continuous Wave"],
    command=on_mode_selection_changed
)

# Render the widget inside your parent layout frame panel
mode_dropdown.pack(fill="x", padx=40, pady=10)
```

---

### Convenience Functions
```python
# Programmatically update menu item lists or query data frames
mode_dropdown.set("Mode 3: Continuous Wave")  # Forces the dropdown choice to display a specific value string
current_choice = mode_dropdown.get()           # Returns the active string item currently displayed
mode_dropdown.update_list(["Option A", "Option B"]) # Safely replaces the visible array and handles indexing boundaries

# Evaluate current state configurations or apply absolute user interaction locks via dual-routing syntax
current_mode = mode_dropdown.get_state()       # Returns 'normal' or 'disabled'
mode_dropdown.state("disabled")                # Locks dropdown triggers and applies muted gray fills
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkOptionMenuPrimary": {
        "fg_color": ["#1A4375", "#1F6AA5"],
        "button_color": ["#112A4B", "#194A7A"],
        "button_hover_color": ["#0F2542", "#134267"],
        "text_color": ["#FFFFFF", "#FFFFFF"],
        "dropdown_fg_color": ["#FFFFFF", "#1F2937"],
        "dropdown_text_color": ["#1F2937", "#FFFFFF"],
        "disabled_map": {
            "fg_color": ["#F3F4F6", "#1F2937"],
            "button_color": ["#E5E7EB", "#374151"],
            "button_hover_color": ["#E5E7EB", "#374151"],
            "text_color": ["#94A3B8", "#64748B"]
        }
    }
}
```

### Other notes
* **Deep-Copy Dictionary Isolation Shield:** Because CustomTkinter's native option menu initialization code mutates, strips, and deletes keys directly out of raw dictionary data footprints during its boot phase, the constructor clones your configurations into `self._local_defaults = dict(self.final_kw)` beforehand. This prevents normal state restorations from crashing on missing keys.
* **Bounded Dynamic Filter Loop:** The visual router is fortified to dynamically loop across active values inside your protected `_local_defaults` memory cache, dropping omitted parameters completely rather than passing raw `None` pointers. This allows CustomTkinter's built-in theme parameters to step forward natively, blocking dangerous type validation exceptions.

---

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed an `sCTkOptionMenuPrimary` option dropdown field along with an interactive status switch toggle.

```python
#!/usr/bin/python3
"""
sCTkOptionMenuPrimary - Standalone Interactive Testing Harness
"""
import customtkinter as ctk

# =====================================================================
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import sCTkThemes                    # 🔍 Duplicate import kept close for script scannability
from sCTkFrame import sCTkFrame      # Testing application wrapper container frame
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkOptionMenuPrimary import sCTkOptionMenuPrimary

if __name__ == "__main__":
    # Natively resolves your package assets and populates configurations cleanly
    sCTkThemes.apply_sCTkThemes()

    root = ctk.CTk()
    root.geometry("450x320")
    root.title("sCTkOptionMenuPrimary Testing Deck")

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # Label notice layer to monitor menu adjustments
    lbl_monitor = sCTkLabelSecondary(base, text="Active Selection: None")
    lbl_monitor.pack(pady=10)

    # Instantiate your custom drop-down menu element
    menu_field = sCTkOptionMenuPrimary(
        base,
        values=["Mode 1: USB", "Mode 2: LSB", "Mode 3: CW"],
        command=lambda choice: lbl_monitor.configure(text=f"Active Selection: {choice}")
    )
    menu_field.pack(expand=False, fill="x", padx=40, pady=10)
    menu_field.set("Mode 1: USB")

    def toggle_operational_state():
        """Toggles the option menu between normal active and dimmed disabled profiles."""
        current_mode = menu_field.get_state()
        target = "disabled" if current_mode == "normal" else "normal"

        # Explicitly testing the dual-routing capability via configure()
        menu_field.configure(state=target)
        btn_toggle.configure(text="Lock Dropdown (Set 'disabled')" if target == "normal" else "Unlock Dropdown (Set 'normal')")
        print(f"Logged Verification Hook -> menu_field.get_state() = {menu_field.get_state()}")

    btn_toggle = ctk.CTkButton(base, text="Lock Dropdown (Set 'disabled')", command=toggle_operational_state)
    btn_toggle.pack(side="bottom", pady=15)

    # Run the interactive boot tracking logs
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    menu_field.state("disabled")
    print("state (Disabled Pass) =", menu_field.get_state())  # Output: disabled

    menu_field.state("normal")
    print("state (Normal Pass)   =", menu_field.get_state())  # Output: normal
    print("========================================\n")

    root.mainloop()
```

[Return to Table of Contents](#contents)
