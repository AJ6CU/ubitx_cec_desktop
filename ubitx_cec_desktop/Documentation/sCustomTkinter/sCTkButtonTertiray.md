## sCTkButtonTertiary

Minimalist ghost / outline tertiary button variant providing high-contrast bounding lines, dynamic background tint matching, and lightweight composite design-time stability.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkButton(master, fg_color="transparent")` | `sCTkButtonTertiary(master)` *(Functions as Ghost / Border Action)* |
| **Maintenance** | Manual color changes across multiple layouts. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Everything runs under one core native pipeline. | Separated safely across `sCTkButtonTertiary.py`, `sCTkButtonTertiaryui.py`, and `ThemeableWidget.py`. |
| `is_pressed` | *Not Available Natively* | `bool` visibility latching flag tracking interactive background tinting status. |
| `set_pressed(pressed)` | *Not Available Natively* | `Method (bool)` to smoothly shift outline buttons into contrast color styles. |
| `state(mode)` | `self.configure(state=...)` | `Method (str)` handling baseline layout tracking map transformations. |
| `get_state()` | `self.cget("state")` | `Method -> str` synchronized assertion getter matching Pygubu queries. |

---

### Constructor

Initialize a tertiary outline / ghost widget instance. Custom keyword overrides layer cleanly over your centralized layout configuration settings.

```python
# Instantiate the minimalist tertiary element
ghost_button = sCTkButtonTertiary(
    master=base_frame,
    text="View Advanced Logs",
    border_width=1.5,               # Override default outline boundary track weight
    command=tertiary_action_fired   # Connect your functional event trigger loop callback
)

# Render the layout inside your parent container geometry tracker path
ghost_button.pack(padx=20, pady=10)
```

---

### Callback Signature & Usage

Routes interaction execution signatures directly to custom functional hooks cleanly on standard click events.

#### Command 

```python
# Fires on tactile button selection loops
def tertiary_action_executed():
    print("Ghost action click recorded.")
```

### Dynamic Property Modifiers Live
```python
# Alter button layout parameters or switch active styles dynamically on the fly
button_tertiary.set_pressed(False)
button_tertiary.configure(text="RE-EVALUATED ACTION")
```

### Convenience Functions
```python
# Query active component states or toggle operational locks cleanly
current_visual = button_tertiary.get_state()
button_tertiary.state("disabled")  # Completely secures layout from hover interactions
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkButtonTertiary": {
        "font": ["Arial", 15, "normal"],
        "fg_color": "transparent",
        "border_width": 1.25,
        "border_color": ["#64748B", "#94A3B8"],
        "hover_color": ["#E2E8F0", "#1E293B"],
        "corner_radius": 6,
        "disabled_map": {
            "border_color": ["#E5E7EB", "#374151"],
            "text_color": ["#94A3B8", "#64748B"]
        },
        "pressed_map": {
            "fg_color": ["#E2E8F0", "#1E293B"],
            "border_color": ["#112A4B", "#1F618D"],
            "text_color": ["#112A4B", "#1F618D"]
        }
    }
}
```

### Other notes
* **Transparency Layer Handling:** The global `_sanitize_value` parser intercepts standard string `"transparent"` definitions, stripping out unsafe dual arrays to prevent underlying core crashes.
* **Isolated Logic Blocks:** Dynamic references match safely without injecting long over-engineered fallback scripts inside shared module systems.

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed the `sCTkButtonTertiary` inside a root window workspace panel layout using the strict interactive test configuration loops.

```python
#!/usr/bin/python3
import customtkinter as ctk
from ThemeableWidget import ThemeableWidget
from sCTkButtonTertiary import sCTkButtonTertiary

# ==========================================
#   MAIN TESTING RUNNER CODE BLOCK
# ==========================================
if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x200")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget1 = sCTkButtonTertiary(base)
    widget = sCTkButtonTertiary(base)

    # -----------------------------------------------------------------
    # 🛠️ THE CLICK REPORT & TOGGLE FIX (Moved cleanly to the Test Harness)
    # -----------------------------------------------------------------
    widget1.configure(
        text="Latching Preset Toggle",
        command=lambda: [
            widget1.set_pressed(not widget1.is_pressed),
            print("Latching Preset Toggle=", widget1.is_pressed)
        ]
    )

    widget.configure(
        text="System Action",
        command=lambda: [
            print("System Action Clicked")
        ]
    )

    widget.pack(expand=False, fill="none", padx=40, pady=15)
    widget1.pack(expand=False, fill="none", padx=40, pady=15)

    # -----------------------------------------------------------------
    # A. INITIAL BOOT LOG TEST SEQUENCE (Kept Exactly As Is)
    # -----------------------------------------------------------------
    # Verify our custom cascading state system locks down the entire panel hierarchy instantly!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("Widget 0 state =", widget.get_state())
    print("Widget 1 state =", widget1.get_state())

    # Verify the cascade pipeline unlocks everything smoothly right back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("Widget 0 state =", widget.get_state())
    print("Widget 1 state =", widget1.get_state())
    print("\n=== SYSTEM ONLINE: TERTIARY BUTTON INTERACTION ACTIVE ===\n")

    root.mainloop()
```


[Return to Table of Contents](#contents)