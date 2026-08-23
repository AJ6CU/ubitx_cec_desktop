## sCTkSelector

### Table of Contents
* [API Property Reference](#api-property-reference)
* [Constructor](#constructor)
* [Convenience Functions](#convenience-functions)
* [Centralized Stylesheet Setup](#centralized-stylesheet-setup-sctkthemesjson)
* [Other Notes](#other-notes)
* [Implementation Example & Test Harness](#implementation-example--test-harness)

---

An advanced theme-compliant option list selector widget [INDEX]. It pairs an optional high-contrast string prefix search lane with a dynamic checklist scrollback chassis to safely manage multi-state checkbox row configurations natively [INDEX].

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | *Not Available Natively* | `sCTkSelector(master)` *(Scrollable Options Selector)* |
| **File Mapping** | Array elements bundle manually without centralized theme hooks. | Separated safely across `sCTkSelector.py` and `ThemeableWidget.py`. |
| **State Lock** | *Not Supported Natively* | `theSelector.state("disabled")`<br>**OR**<br>`theSelector.configure(state="disabled")`<br><br>**Polymorphic State Controller:** Simultaneously locks the top search bar entry field and freezes all child selection checkbox tracks natively. |
| `searchBox` | *Not Supported Natively* | `Property -> bool`. Controls visibility of the dynamic search bar lane. |

---

### Constructor

Initialize a custom themed selector option array tree layout.

```python
items = ["vw", "porsche", "roadster", "tesla", "ferrari", "mclaren"]

# Instantiate with multi-selection active but search functionality turned off
theSelector = sCTkSelector(
    master=root, 
    items=items, 
    multiple_choices=True, 
    searchBox=False
)

# Render the widget inside your container panel
theSelector.pack(expand=True, fill="both", padx=15, pady=15)
```

---

### Convenience Functions
```python
# Unpack current active choices dynamically
active_items = theSelector.get_selections()  # Returns list of strings e.g. ['porsche', 'tesla']

# Return all mapped string names managed by the element index
all_options = theSelector.get_all_items()     # Returns list of all items

# Wipe selection arrays clean uniformly
theSelector.clear_selections()

# Adjust layout properties or component visibilities on the fly
theSelector.configure(searchBox=True)        # Dynamically mounts and renders search bar lane
```

### Centralized Stylesheet Setup (`sCTkThemes.json`)
```json
{
    "sCTkSelector": {
        "fg_color": ["#FAFAFA", "#11141A"],
        "border_color": ["#CBD5E1", "#222933"],
        "text_color": ["#1F2937", "#FFFFFF"],
        "disabled_map": {
            "fg_color": ["#F1F5F9", "#0A0D14"],
            "border_color": ["#E2E8F0", "#171C24"]
        }
    }
}
```

### Other Notes
* **Isolated Checklist Tracking:** To optimize bulk interface operations, this component tracks its row nodes through its own localized memory list array (`self.checkboxes`) [INDEX]. Standard window inspection crawlers on dashboard trees bypass its internals cleanly, protecting checkboxes from global style conflicts.
* **Stack Re-Ordering Execution:** Toggling `searchBox=True` dynamically at runtime triggers a pack index safety cycle [INDEX]. The canvas content chassis forgets and remounts its bottom alignment to prevent native packing sequence layout exceptions [INDEX].

---

### Implementation Example & Test Harness

Below is a complete, self-contained testing suite containing block-commented execution routes to safely evaluate option configurations [INDEX].

```python
#!/usr/bin/python3
"""
sCTkSelector - Standalone Interactive Testing Harness
"""
import customtkinter as ctk

# =====================================================================
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import sCTkThemes                      
from sCTkButtonPrimary import sCTkButtonPrimary
from sCTkSelector import sCTkSelector

if __name__ == "__main__":
    def on_confirm():
        print(f"Active Selection Telemetry Array: {theSelector.get_selections()}")

    root = ctk.CTk()
    root.geometry("200x380")
    root.title("sCTkSelector Validation Bench")

    # Resolve style metrics safely [INDEX]
    sCTkThemes.apply_sCTkThemes()

    items = ["vw", "porsche", "roadster", "tesla", "ferrari", "mclaren"]

    # MULTI-ROUTE CONFIGURE TESTING LAYOUT:
    
    # Route A: Add search field lane dynamically after creation
    # theSelector = sCTkSelector(root, items=items, multiple_choices=True, searchBox=False)
    # theSelector.configure(searchBox=True)

    # Route B: Delete search box layout cell after creation
    # theSelector = sCTkSelector(root, items=items, multiple_choices=True, searchBox=True)
    # theSelector.configure(searchBox=False)

    # Route C: Normal Case Profile
    theSelector = sCTkSelector(root, items=items, multiple_choices=True)

    theSelector.pack(expand=True, fill="both", padx=15, pady=15)

    confirm_btn = sCTkButtonPrimary(root, text="Confirm Selections", command=on_confirm)
    confirm_btn.pack(pady=(0, 15))

    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    theSelector.state("disabled")
    print("state (Disabled Pass) =", theSelector.get_state())  # Output: disabled
    theSelector.state("normal")
    print("state (Normal Pass)   =", theSelector.get_state())  # Output: normal
    print("========================================\n")

    root.mainloop()
```

[Return to Table of Contents](#contents)
