## sCTkSlider

Standardized live track calibration adjustment slider providing real-time data value interception, disabled layout mapping overrides, and multi-zone Pygubu designer compatibility.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkSlider(master)` | `sCTkSlider(master)` *(Live metric adjuster handle)* |
| **Maintenance** | Local style overrides duplicated across files manually. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Everything runs under one core native pipeline tracker. | Separated safely across `sCTkSlider.py`, `sCTkSliderui.py`, and `ThemeableWidget.py`. |
| `state(mode)` | `self.configure(state=...)` | `Method (str)` handling layout tracking map transformations (`'normal'`, `'disabled'`). |
| `get_state()` | `self.cget("state")` | `Method -> str` explicit verification query matching system test assertions. |

---

### Constructor

Initialize a tracking controller slider adjustment instance. Complex track variables layer safely over your stylesheet metrics at runtime.

```python
# Instantiate the customized live telemetry slider track element
size_calibrator = sCTkSlider(
    master=calibration_panel,
    from_=50,
    to=250,
    command=lambda val: print(f"Current Value Adjusted: {val:.3f}")
)

# Render the slider widget inside your parent container coordinate packer
size_calibrator.pack(fill="x", padx=30, pady=10)
```

---

### Callback Signature & Usage

Routes current floating-point slider knob coordinate metrics down to application listening hooks seamlessly in real time during click-dragging movements.

#### Command

```python
# Fires instantly upon receiving mouse handle interaction dragging motion changes
def on_calibration_scale_changed(current_value: float):
    print(f"Live Track Value Readout: {current_value:.4f}")
```

### Dynamic Property Modifiers Live
```python
# Alter slider scaling thresholds or snap targets on the fly
size_calibrator.configure(from_=0, to=1)
```

### Convenience Functions
```python
# Manually position the tracking handle directly onto a specific decimal location coordinate
size_calibrator.set(0.45)

# Query current operational status or lock the widget out of interaction loops cleanly
current_state = size_calibrator.get_state()  # Returns 'normal' or 'disabled'
size_calibrator.state("disabled")            # Fades the track fill and completely freezes the handle
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkSlider": {
        "fg_color": ["#E2E8F0", "#4B5563"],
        "progress_color": ["#2471A3", "#3B8ED0"],
        "button_color": ["#1A4375", "#1F6AA5"],
        "button_hover_color": ["#112A4B", "#194A7A"],
        "disabled_map": {
            "fg_color": ["#CBD5E1", "#374151"],
            "progress_color": ["#94A3B8", "#4B5563"],
            "button_color": ["#94A3B8", "#4B5563"]
        }
    }
}
```

### Other notes
* **Infinite Recursion Lock Cleared:** Internal state modifications route strictly through `super().configure()` pathways, ensuring secondary cascading locks never trip execution loop crashes.
* **Pygubu Live Preview:** Feeds disabled theme tracking parameters directly back into Pygubu's designer canvas to support real-time visual inspection cycles accurately.

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed an `sCTkSlider` alongside a live telemetry monitor.

```python
import customtkinter as ctk
from sCTkSlider import sCTkSlider
from sCTkLabelSecondary import sCTkLabelSecondary

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x180")
    root.title("Live Slider Telemetry Bench")

    lbl_data = sCTkLabelSecondary(root, text="Coordinate Track: 0.50")
    lbl_data.pack(pady=10)

    slider = sCTkSlider(
        root,
        command=lambda val: lbl_data.configure(text=f"Coordinate Track: {val:.2f}")
    )
    slider.pack(fill="x", padx=40, pady=15)
    slider.set(0.50)

    root.mainloop()
```
