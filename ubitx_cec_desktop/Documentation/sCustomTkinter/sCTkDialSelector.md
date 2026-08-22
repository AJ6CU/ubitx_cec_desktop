## sCTkDialSelector

Rotary switch selector module constrained to custom arc sweeps, designed to loop infinitely past terminal thresholds, and report active array choice index positions.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | *Not Available Natively* | `sCTkDialSelector(master)` *(Rotary Switch Switcher)* |
| **File Mapping** | No comparable native drawing component framework. | Inherits vector math mechanics directly out of `sCTKDialBase.py`. |
| `labels` | *Not Available Natively* | `list` of strings mapped symmetrically onto visual canvas index tick lines. |
| `arc_angle` | *Not Available Natively* | `float` bounding the total available active degree wedge for layout markers. |
| `set(index)` | *Not Available Natively* | `Method (int)` forces the selector pointer needle to a specific item index. |
| `get()` | *Not Available Natively* | `Method -> int` query returning the active chosen item row location index. |

---

### Constructor

Initialize a custom rotary option tracking switch instance. String label configurations passed out of designer files are processed cleanly.

```python
# Instantiate the themed rotary selector element
mode_selector = sCTkDialSelector(
    master=frame_selector,
    labels=["CW", "USB", "LSB", "AM", "FM", "RTTY"],
    arc_angle=270,
    diameter=110,
    command=on_mode_switch_rotated
)

# Initialize the needle selection slot position at boot frame
mode_selector.set(0)
```

---

### Callback Signature & Usage

Dispatches absolute zero-indexed selection row integers down to tracking systems upon pointer index notch updates.

#### Command 

```python
# Fires on pointer index notch changes via wheel scrolls or dragging motion lines
def on_mode_switch_rotated(active_index: int):
    # Receives standard absolute positive index integers: 0, 1, 2, 3, etc.
    mode_string = operating_modes[active_index]
    print(f"Active Mode: {mode_string}")
```

### Other notes
* **Comma-Separated Parsing Layer:** The internal property parser cleanly strips brackets and quotes from raw string text inputs, allowing Pygubu Designer to pass comma-separated list properties without errors.
* **Rolling Index Loop:** Reaching the end of the option array loops the selector needle around smoothly (e.g., clicking past the maximum option loops it back to `0`).


### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed an `sCTkSlider` alongside a live telemetry monitor.

```python
#!/usr/bin/python3
"""
sCTkDialSelector - Standalone Interactive Testing Harness
"""
import customtkinter as ctk
from sCTkFrame import sCTkFrame
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkDialSelector import sCTkDialSelector

# Operational radio station rig test parameters
operating_modes = ["CW", "USB", "LSB", "AM", "FM", "RTTY"]

def on_mode_switch_rotated(active_index):
    """Callback for Selector Module: Receives absolute integer array index choices."""
    mode_string = operating_modes[active_index]
    if lbl_selector_display.winfo_exists():
        lbl_selector_display.configure(text=f"Mode: {mode_string} [Idx {active_index}]")

def toggle_operational_state():
    """Toggles interaction channels and visual states back and forth."""
    current_mode = dial_selector.cget("state")
    target = "disabled" if current_mode == "normal" else "normal"
    
    dial_selector.configure(state=target)
    lbl_selector_display.configure(state=target)
    btn_toggle.configure(text="Lock Switch (Set 'disabled')" if target == "normal" else "Unlock Switch (Set 'normal')")
    print(f"Logged Verification Hook -> dial_selector.get_state() = {dial_selector.get_state()}")

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("sCTkDialSelector Test Deck")
    root.geometry("380x360")

    base = sCTkFrame(root, corner_radius=8)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    lbl_title = sCTkLabelSecondary(base, text="1. SELECTOR SWITCH", font=("Arial", 12, "bold"))
    lbl_title.pack(pady=(12, 2))

    dial_selector = sCTkDialSelector(
        base, 
        labels=operating_modes, 
        arc_angle=270,
        command=on_mode_switch_rotated, 
        diameter=110
    )
    dial_selector.pack(pady=10)
    dial_selector.set(0)

    lbl_selector_display = sCTkLabelSecondary(base, text="Mode: CW [Idx 0]", font=("Arial", 11, "bold"))
    lbl_selector_display.pack(pady=10)

    btn_toggle = ctk.CTkButton(base, text="Lock Switch (Set 'disabled')", command=toggle_operational_state)
    btn_toggle.pack(side="bottom", pady=15)

    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    print(f"Initial Selector State = {dial_selector.get_state().upper()}")
    print("========================================\n")

    root.mainloop()
```