## sCTkDialRange

Ranged potentiometer dial module tracking discrete value limits, engineered with absolute dead stops, and reporting absolute scalar integer tracking metrics.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | *Not Available Natively* | `sCTkDialRange(master)` *(Ranged Potentiometer)* |
| **File Mapping** | No comparable native drawing component framework. | Inherits vector math mechanics directly out of `sCTKDialBase.py`. |
| `_from` / `_to` | *Not Available Natively* | `int` minimum boundary floor values and maximum boundary ceiling targets. |
| `set(value)` | *Not Available Natively* | `Method (int)` forces the dial pointer to a value with strict threshold limits. |
| `get()` | *Not Available Natively* | `Method -> int` returns the absolute scalar numerical integer current location value. |

---

### Constructor

Initialize a custom ranged potentiometer element instance. Keyword parameters seamlessly support standard minimum and maximum terminology variations.

```python
# Instantiate the themed ranged potentiometer element
volume_pot = sCTkDialRange(
    master=frame_range,
    from_=0,
    to=100,
    arc_angle=270,
    divisions=5,
    diameter=110,
    command=on_volume_pot_rotated
)

# Secure the initialization volume value to 25% at application boot
volume_pot.set(25)
```

---

### Callback Signature & Usage

Dispatches real-time absolute calculated scalar data values down to interface listeners directly upon pointer movements.

#### Command 

```python
# Fires on numerical location shifts via scroll adjustments or vector pointer drag tracks
def on_volume_pot_rotated(absolute_value: int):
    # Receives raw integer values calculated dynamically from your min/max limits
    print(f"Potentiometer Value updated to: {absolute_value}")
```

### Other notes
* **Clamped Hard Bounding Stops:** Integrates rigid limit boundary filters (`max(self._from, min(self._to, ...))`), locking the pointer line securely at thresholds during dragging cycles instead of looping.
* **Polymorphic Scale Rendering:** Automatically reads the `divisions` argument to divide your custom arc wedge into distinct, numerically labeled index points.


### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed an `sCTkSlider` alongside a live telemetry monitor.

```python
#!/usr/bin/python3
"""
sCTkDialRange - Standalone Interactive Testing Harness
"""
import customtkinter as ctk
from sCTkFrame import sCTkFrame
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkDialRange import sCTkDialRange

# Initial test scalar baseline metrics
audio_volume_pct = 25

def on_volume_pot_rotated(absolute_value):
    """Callback for Range Module: Receives absolute bounded scalar integer coordinates."""
    if lbl_range_display.winfo_exists():
        lbl_range_display.configure(text=f"Volume: {absolute_value}%")

def toggle_operational_state():
    """Toggles interaction channels and visual states back and forth."""
    current_mode = dial_range.cget("state")
    target = "disabled" if current_mode == "normal" else "normal"
    
    dial_range.configure(state=target)
    lbl_range_display.configure(state=target)
    btn_toggle.configure(text="Lock Pot (Set 'disabled')" if target == "normal" else "Unlock Pot (Set 'normal')")
    print(f"Logged Verification Hook -> dial_range.get_state() = {dial_range.get_state()}")

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("sCTkDialRange Test Deck")
    root.geometry("380x360")

    base = sCTkFrame(root, corner_radius=8)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    lbl_title = sCTkLabelSecondary(base, text="2. POTENTIOMETER (RANGE)", font=("Arial", 12, "bold"))
    lbl_title.pack(pady=(12, 2))

    dial_range = sCTkDialRange(
        base, 
        from_=0, 
        to=100, 
        arc_angle=270, 
        command=on_volume_pot_rotated, 
        diameter=110,
        divisions=5
    )
    dial_range.pack(pady=10)
    dial_range.set(audio_volume_pct)

    lbl_range_display = sCTkLabelSecondary(base, text=f"Volume: {audio_volume_pct}%", font=("Arial", 11, "bold"))
    lbl_range_display.pack(pady=10)

    btn_toggle = ctk.CTkButton(base, text="Lock Pot (Set 'disabled')", command=toggle_operational_state)
    btn_toggle.pack(side="bottom", pady=15)

    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    print(f"Initial Potentiometer State = {dial_range.get_state().upper()}")
    print("========================================\n")

    root.mainloop()
```