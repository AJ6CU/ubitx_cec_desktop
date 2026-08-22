## sCTkButtonSecondary

Latching companion state toggle action button engineered with explicit edge borders, structured interaction tracking, and absolute canvas unbinding security tags.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkButton(master, border_width=0)` | `sCTkButtonSecondary(master)` *(Functions as Companion Toggle Outline)* |
| **Maintenance** | Manual color changes across multiple layouts. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Everything runs under one core native pipeline. | Separated safely across `sCTkButtonSecondary.py`, `sCTkButtonSecondaryui.py`, and `ThemeableWidget.py`. |
| `is_pressed` | *Not Available Natively* | `bool` tracker flag indicating if the companion button is toggled down. |
| `set_pressed(pressed)` | *Not Available Natively* | `Method (bool)` to manually lock or unlatch custom pressed map colors. |
| `state(mode)` | `self.configure(state=...)` | `Method (str)` handling layout tracking map transformations (`'normal'`, `'disabled'`). |
| `get_state()` | `self.cget("state")` | `Method -> str` explicit verification query matching system test assertions. |

---

### Constructor

Initialize a companion action toggle widget instance. Any direct configurations passed here layer over your centralized configuration settings.

```python
# Instantiate the customized secondary latching toggle element
companion_button = sCTkButtonSecondary(
    master=base_frame,
    text="Toggle Grid Layout",
    border_width=3,                 # Explicitly widen the border frame rim lines
    command=toggle_action_fired     # Attach your selection event loop callback
)

# Render the layout inside your parent container geometry packer grid
companion_button.pack(padx=20, pady=10)
```

---

### Callback Signature & Usage

Executes custom callback logic stacks on mouse selection changes, smoothly passing command statements down to local tracking terminals.

#### Command 

```python
# Fires instantly upon receiving mouse selection interactions
def companion_toggle_changed():
    print("Secondary action loop execution trace recorded.")
```

### Dynamic Property Modifiers Live
```python
# Modify text value settings or force latching profiles directly on the fly
button_secondary.set_pressed(True)
button_secondary.configure(text="SELECTED COMPANION")
```

### Convenience Functions
```python
# Evaluate current active structural state strings or apply operational changes cleanly
current_status = button_secondary.get_state()
button_secondary.state("disabled")  # Unbinds all listeners and applies flat disabled maps safely
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkButtonSecondary": {
        "font": ["Arial", 15, "normal"],
        "fg_color": ["#E5E7EB", "#374151"],
        "hover_color": ["#D1D5DB", "#4B5563"],
        "text_color": ["#1F2937", "#F9FAFB"],
        "border_width": 2,
        "border_color": ["#9CA3AF", "#4B5563"],
        "corner_radius": 6,
        "disabled_map": {
            "fg_color": ["#F3F4F6", "#1F2937"],
            "hover_color": ["#F3F4F6", "#1F2937"],
            "border_color": ["#E5E7EB", "#374151"],
            "text_color": ["#94A3B8", "#64748B"]
        },
        "pressed_map": {
            "fg_color": ["#CBD5E1", "#1F2937"],
            "hover_color": ["#CBD5E1", "#1F2937"],
            "border_color": ["#475569", "#94A3B8"],
            "text_color": ["#0F172A", "#FFFFFF"]
        }
    }
}
```

### Other notes
* **Memory Lock Leak Protection:** Shifting to `disabled` explicitly unbinds `<Enter>`, `<Leave>`, and `<Button-1>` mouse signals on the raw sub-canvas, preventing hovering graphic glitches.
* **Super Core Redraw Bypass:** Redraws bypass the `configure` multi-zone positional intercept loop using `super()`, preventing deep stack pointer segmentation crashes.

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed the `sCTkButtonSecondary` inside a root window workspace panel layout using the strict interactive test configuration loops.

```python
import customtkinter as ctk
from ThemeableWidget import ThemeableWidget
from sCTkButtonSecondary import sCTkButtonSecondary
if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x200")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget = sCTkButtonSecondary(base, text="System Action Button")
    widget1 = sCTkButtonSecondary(base, text="Latching Preset Toggle")

    widget.pack(padx=40, pady=20)
    widget1.pack(padx=40, pady=20)

    # -----------------------------------------------------------------
    # A. INITIAL BOOT LOG TEST SEQUENCE (Kept Exactly As Is)
    # -----------------------------------------------------------------
    widget.state("normal")
    widget1.set_pressed(True)

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
    print("\n=== SYSTEM ONLINE: SECONDARY BUTTON INTERACTION ACTIVE ===\n")

    # -----------------------------------------------------------------
    # B. 🛠️ THE INTERACTION FIX: MAKE BUTTONS ALIVE AND RESPOND TO CLICKS
    # -----------------------------------------------------------------
    # 🛠️ THE CLICK REPORT FIX: Added a print statement to report the click instantly
    widget.configure(
        command=lambda: [print("System Action Button Clicked"), widget.set_pressed(not widget.is_pressed)])

    # Clicking 'widget1' does the exact same thing, turning its pre-set pressed state off and on!
    widget1.configure(
        command=lambda: [print("Testpressed Button Clicked"), widget1.set_pressed(not widget1.is_pressed)])

    root.mainloop()
```


[Return to Table of Contents](#contents)