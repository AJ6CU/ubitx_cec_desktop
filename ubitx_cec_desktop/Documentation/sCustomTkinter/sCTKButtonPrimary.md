## sCTkButtonPrimary

High-visibility primary action button equipped with state-latching mechanisms, emergency alarm state overrides, and multi-zone Pygubu Inspector design-time compatibility.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkButton(master)` | `sCTkButtonPrimary(master)` *(Functions as Core Action Trigger)* |
| **Maintenance** | Manual color changes across multiple layouts. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Everything runs under one core native pipeline. | Separated across `sCTkButtonPrimary.py`, `sCTkButtonPrimaryui.py`, and `ThemeableWidget.py`. |
| `is_pressed` | *Not Available Natively* | `bool` tracking if the component is toggled into its latching profile. |
| `is_alarm` | *Not Available Natively* | `bool` high-priority override flag forcing the button into alert layouts. |
| `set_pressed(pressed)` | *Not Available Natively* | `Method (bool)` to explicitly latch/unlatch custom pressed map configurations. |
| `set_alarm_state(active)`| *Not Available Natively* | `Method (bool)` top-priority visual interceptor forcing emergency color overwrites. |
| `state(mode)` | `self.configure(state=...)` | `Method (str)` handling layout tracking map transformations (`'normal'`, `'disabled'`). |
| `get_state()` | `self.cget("state")` | `Method -> str` explicit verification query matching system test assertions. |

---

### Constructor

Initialize a primary action widget instance. Any direct property configuration passed here will safely layer over your centralized `themes.json` asset settings at runtime.

```python
# Instantiate the customized primary button element
action_button = sCTkButtonPrimary(
    master=base_frame,
    text="Execute System Flash",
    width=160,                     # Override centralized theme file dimension profile
    command=primary_action_fired   # Attach your interactive loop callback function
)

# Render the layout inside your parent container geometry grid
action_button.pack(padx=20, pady=10)
```

---

### Callback Signature & Usage

Executes standard command sequences and reports event loops natively without adding low-level canvas window hardware bindings.

#### Command 

```python
# Fires on button selection via standard mouse release or tap tracking loops
def primary_button_clicked():
    print("Primary action initiated successfully.")
```

### Dynamic Property Modifiers Live
```python
# Transition the primary widget into an active alarm state or update text dynamically on the fly
button.set_alarm_state(active=True)
button.configure(text="CRITICAL ALERT ACTIVE")
```

### Convenience Functions
```python
# Query current state value string or toggle operational availability cleanly
current_mode = button.get_state()  # Returns 'normal' or 'disabled'
button.state("disabled")           # Completely locks interaction layers and applies muted styles
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkButtonPrimary": {
        "width": 140,
        "height": 34,
        "font": ["Arial", 15, "normal"],
        "fg_color": ["#1A4375", "#2471A3"],
        "hover_color": ["#112A4B", "#1F618D"],
        "text_color": ["#FFFFFF", "#FFFFFF"],
        "corner_radius": 6,
        "disabled_map": {
            "fg_color": ["#E5E7EB", "#374151"],
            "hover_color": ["#E5E7EB", "#374151"],
            "text_color": ["#94A3B8", "#64748B"]
        },
        "pressed_map": {
            "fg_color": ["#3B5984", "#2E4A75"],
            "hover_color": ["#3B5984", "#2E4A75"],
            "text_color": ["#FFFFFF", "#FFFFFF"]
        },
        "alarm_map": {
            "fg_color": ["#990000", "#E74C3C"],
            "hover_color": ["#990000", "#E74C3C"],
            "text_color": ["#FFFFFF", "#FFFFFF"]
        }
    }
}
```

### Other notes
* **Alarm Override Priority:** Turning on the alarm state forcefully turns off any persistent latching pressed visual looks.
* **Pygubu Zone-A Interception:** The widget safely responds to single positional property queries coming from design-time editor tools without crashing or locking execution tracks.

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed the `sCTkButtonPrimary` inside a root window workspace panel layout using the strict interactive test configuration loops.

```python
import customtkinter as ctk
from sCTkButtonPrimary import sCTkButtonPrimary
# =====================================================================
# 3. INTERACTIVE RUNTIME APP EXECUTION & TEST SEQUENCES
# =====================================================================
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("450x200")
    root.title("Primary Button Test Harness")
    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # Instantiate two primary actions
    widget = sCTkButtonPrimary(base, text="System Alarm Button")
    widget1 = sCTkButtonPrimary(base, text="Latching Preset Toggle")

    widget.pack(padx=40, pady=15)
    widget1.pack(padx=40, pady=15)

    # -----------------------------------------------------------------
    # A. INITIAL CONSOLE LOG TEST SEQUENCE
    # -----------------------------------------------------------------
    print("--- BOOT TEST: FORCING DISABLED PASS ---")
    widget.state("disabled")
    widget1.state("disabled")
    print("Widget 0 state =", widget.get_state())
    print("Widget 1 state =", widget1.get_state())

    print("\n--- BOOT TEST: REVERTING TO NORMAL PASS ---")
    widget.state("normal")
    widget1.state("normal")
    print("Widget 0 state =", widget.get_state())
    print("Widget 1 state =", widget1.get_state())
    print("\n=== SYSTEM ONLINE: BUTTON INTERACTION ACTIVE ===\n")

    # -----------------------------------------------------------------
    # B. 🛠️ THE INTERACTION FIX: MAKE BUTTONS ALIVE AND RESPOND TO CLICKS
    # -----------------------------------------------------------------
    # 🛠️ THE ALARM TOGGLE FIX: Change the command loop sequence to flip the alarm flag!
    widget.configure(
        command=lambda: [print("System Alarm Toggle Triggered"), widget.set_alarm_state(not widget.is_alarm)])

    # Clicking 'widget1' remains assigned to your standard layout latch toggle
    widget1.configure(command=lambda: [print("Latching Preset Clicked"), widget1.set_pressed(not widget1.is_pressed)])

    root.mainloop()
```


[Return to Table of Contents](#contents)