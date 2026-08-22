## sCTkButtonSecondary

A specialized, theme-compliant secondary button component widget variant designed to act as a latching status toggle selector. It implements a deep-copy keyword caching shield to preserve custom visual style parameters from native mutation traps and prevent `NoneType` canvas validation exceptions.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkButton(master)` | `sCTkButtonSecondary(master)` *(Latching Toggle Selector)* |
| **File Mapping** | Component definitions bundle under single active tracks. | Separated safely across `sCTkButtonSecondary.py` and `ThemeableWidget.py`. |
| `state(mode)` | `self.configure(state=...)` | `Method (str)` managing layout tracking maps and toggling active canvas event binds. |
| `get_state()` | `self.cget("state")` | `Method -> str` explicit verification query matching system test assertions. |
| `set_pressed(bool)` | *Not Available Natively* | **Latching Hook:** Dynamically updates visual button states to look locked down. |

---

### Constructor

Initialize a custom secondary latching toggle button instance. Geometry constraints and color properties map cleanly out of central stylesheet parameters.

```python
# Instantiate a secondary latching toggle button element
vfo_lock_toggle = sCTkButtonSecondary(
    master=control_panel,
    text="LOCK ACTIVE VFO MODE",
    command=on_vfo_lock_toggled
)

# Render the widget inside your parent container geometry tracker layout
vfo_lock_toggle.pack(fill="x", padx=40, pady=10)
```

---

### Convenience Functions
```python
# Force an active button press visual accent highlight on the fly
vfo_lock_toggle.set_pressed(True)   # Shifts colors to match your pressed_map rules

# Evaluate active visual modes or apply absolute user interaction locks
current_mode = vfo_lock_toggle.get_state() # Returns 'normal' or 'disabled'
vfo_lock_toggle.state("disabled")          # Unbinds mouse canvas routines and applies muted gray fills
```

### Centralized Stylesheet Setup (`sCTkThemes.json`)
```json
{
    "sCTkButtonSecondary": {
        "fg_color": "transparent",
        "border_color": ["#CBD5E1", "#44403C"],
        "text_color": ["#334155", "#E7E5E4"],
        "border_width": 1,
        "corner_radius": 6,
        "disabled_map": {
            "fg_color": ["#F1F5F9", "#171412"],
            "border_color": ["#E2E8F0", "#292524"],
            "text_color": ["#94A3B8", "#57534E"]
        },
        "pressed_map": {
            "fg_color": ["#E2E8F0", "#44403C"],
            "border_color": ["#94A3B8", "#6B7280"],
            "text_color": ["#000000", "#FFFFFF"]
        }
    }
}
```

### Other notes
* **Deep-Copy Dictionary Isolation Shield:** Because CustomTkinter's native button initialization code mutates, strips, and deletes keys directly out of raw dictionary data footprints during its boot phase, the constructor clones your configurations into `self._local_defaults = dict(self.final_kw)` beforehand. This prevents normal state restorations from crashing on missing keys.
* **Canvas Interaction Toggles:** When shifted into a `disabled` state configuration, the widget explicitly unbinds mouse events (`<Enter>`, `<Leave>`, `<Button-1>`) at the canvas level to lock interactions and prevent memory leaks. Shifting back to `normal` restores the listeners seamlessly.

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed an `sCTkButtonSecondary` alongside an interactive latch controller.

```python
import customtkinter as ctk
from ThemeableWidget import ThemeableWidget
from sCTkButtonSecondary import sCTkButtonSecondary
import sCTkThemes
if __name__ == "__main__":
    sCTkThemes.apply_sCTkThemes()
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