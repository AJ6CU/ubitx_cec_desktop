## sCTkDialSelector

### Table of Contents
* [API Property Reference](#api-property-reference)
* [Constructor](#constructor)
* [Callback Signature & Usage](#callback-signature--usage)
* [Centralized Stylesheet Setup](#centralized-stylesheet-setup-sctkthemesjson)
* [Other Notes](#other-notes)
* [Implementation Example & Test Harness](#implementation-example--test-harness)

---

A concrete rotary encoder switch variant designed for stepped selector controls (e.g., band configurations, operating modes, or filter sub-selections). It uses an explicit bounding arc configuration and outputs a clean integer mapping parameter tracking list item indices natively [INDEX].

### API Property Reference

| Property / Feature        | Type / Signature | Description |
|:--------------------------| :--- | :--- |
| **Instantiation**         | *Constructor* | `sCTkDialSelector(master)` *(Stepped Arc Selector Dial)* |
| **File Mapping**          | *Inheritance Tree* | Inherits parent 3D mechanical chassis elements and base state tracking directly from `sCTKDialBase.py` [INDEX]. |
| `labels`                  | `list [str]` | Ordered array list mapping string tags directly above calculated step lines. Supports raw comma-separated strings inside layout inspectors [INDEX]. |
| `arc_angle`               | `float` | Angular geometric limit (default 270) restricting the pointer range sweep layout [INDEX]. |
| `_scroll_cooldown_seconds`| `float` | Throttle limiting touchpad refresh rates to stabilize fast selector rolls [INDEX]. |
| `get()` / `set(idx)`      | `Methods -> int` | Unified index query mechanisms to get or force selected positions [INDEX]. |
| `left_click_callback`     | `Callable / None` | **Custom Accelerated Click Hook:** Overrides standard single-step decrements to execute accelerated jumping intervals when clicking the left canvas edge [INDEX]. |
| `right_click_callback`    | `Callable / None` | **Custom Accelerated Click Hook:** Overrides standard single-step increments to execute accelerated jumping intervals when clicking the right canvas edge [INDEX]. |
| **State**                 | `dial.state("disabled")`<br>**OR**<br>`dial.configure(state="disabled")` | **Dual-Routing State Pipeline:** Handles both syntaxes natively [INDEX]. Freezes canvas mouse-wheel scrolling, disables click jump hooks, and shifts visual themes out of `disabled_map` guidelines [INDEX, INDEX]. |

---

### Constructor

Initialize a custom stepped rotary selector switch instance. Properties like `labels` support raw string array text list configurations natively for absolute Pygubu inspector panel compatibility [INDEX].

```python
# Instantiate a 5-position operating mode rotary switch selector
mode_switch = sCTkDialSelector(
    master=control_panel,
    labels=["AM", "FM", "LSB", "USB", "CW-N"],
    arc_angle=180,
    command=on_operating_mode_changed,
    left_click_callback=my_custom_left_click,
    right_click_callback=my_custom_right_click
)
```

---

### Callback Signature & Usage

Dispatches the current absolute active list item integer index directly to runtime configuration listeners [INDEX].

#### Command 

```python
# Fires automatically on valid mouse scrolling, touchpad rolling, or click-drag actions
def on_operating_mode_changed(active_index: int):
    # active_index maps directly to items in your labels block list (0, 1, 2, etc.)
    print(f"Active Selected Option Index position tracker = {active_index}")
```

### Centralized Stylesheet Setup (`sCTkThemes.json`)
```json
{
    "sCTkDialSelector": {
        "fg_color": "transparent",
        "dial_color": ["#1E293B", "#181E2B"],
        "border_color": ["#CBD5E1", "#334155"],
        "text_color": ["#0284C7", "#38BDF8"],
        "pointer_color": ["#0284C7", "#38BDF8"],
        "shadow_color": ["#CBD5E1", "#02040A"],
        "border_width": 0,
        "corner_radius": 0
    }
}
```

### Other notes
* **Rolling Selector Loops:** When spinning scroll wheels beyond boundary edges, the index modulo calculates the length of the string array, snapping the cursor back around to index 0 smoothly [INDEX].
* **Pygubu Comma Separation Track:** Zone B converts designer comma-separated parameter strings into structured, valid list containers cleanly at runtime [INDEX].
* **Unified State Infrastructure:** Implements no internal state query definitions. `get_state()` gracefully routes up to the `sCTKDialBase` layer natively via the Python method resolution order (MRO), eliminating redundant file methods [INDEX].
* **Custom Accelerated Steps:** Attaching optional click callbacks allows click events to jump values by wider intervals rather than dropping onto the baseline single-step tracking paths [INDEX].

---

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed an `sCTkDialSelector` alongside custom click jump hooks and an active mode switch control panel display tracker [INDEX].

```python
#!/usr/bin/python3
"""
sCTkDialSelector - Standalone Interactive Testing Harness
"""


# =====================================================================
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import customtkinter as ctk
import sCTkThemes                # 🔍 Duplicate import kept close for script scannability
from sCTkFrame import sCTkFrame  # Testing application wrapper container frame
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkDial import sCTkDialSelector

if __name__ == "__main__":
    # Natively resolves your package assets and populates configurations cleanly [INDEX]
    sCTkThemes.apply_sCTkThemes()

    root = ctk.CTk()
    root.geometry("450x350")
    root.title("Rotary Switch Selector Bench")

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # 1. Attach a live telemetry readout label 
    lbl_mode_tag = sCTkLabelSecondary(base, text="Selected Mode: AM", font=("Arial", 11, "bold"))
    lbl_mode_tag.pack(pady=15)

    def my_custom_left_click():
        """Accelerated Jump: Moves 2 complete indexing steps left per click tap [INDEX]."""
        if mode_selector.get_state() == "disabled": 
            return
        mode_selector.set(mode_selector.get() - 2)

    def my_custom_right_click():
        """Accelerated Jump: Moves 2 complete indexing steps right per click tap [INDEX]."""
        if mode_selector.get_state() == "disabled": 
            return
        mode_selector.set(mode_selector.get() + 2)

    # 2. Instantiate with unique radio deck selector labels and selection trackers
    mode_selector = sCTkDialSelector(
        base,
        labels=["AM", "FM", "LSB", "USB", "CW-N"],
        arc_angle=180,  # Half-circle step selector arc
        command=lambda idx: lbl_mode_tag.configure(text=f"Selected Mode: {mode_selector._labels[idx]}"),
        left_click_callback=my_custom_left_click,
        right_click_callback=my_custom_right_click
    )
    mode_selector.pack(expand=True, fill="none", padx=10, pady=10)

    # 3. Standard application dashboard interaction lock toggle simulation
    def toggle_widget_lock():
        current_mode = mode_selector.get_state()
        target = "disabled" if current_mode == "normal" else "normal"
        
        mode_selector.configure(state=target)
        btn_lock.configure(
            text="UNLOCK CHANNELS" if target == "disabled" else "LOCK SWITCH (Set 'disabled')"
        )
        print(f"Logged Verification Hook -> mode_selector.get_state() = {mode_selector.get_state()}")

    btn_lock = ctk.CTkButton(base, text="LOCK SWITCH (Set 'disabled')", command=toggle_widget_lock)
    btn_lock.pack(side="bottom", pady=10)

    # Standard test assertions routine verification sequences
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    mode_selector.state("disabled")
    print("state (Disabled Pass) =", mode_selector.get_state())  # Output: disabled

    mode_selector.state("normal")
    print("state (Normal Pass)   =", mode_selector.get_state())  # Output: normal
    print("========================================\n")

    root.mainloop()
```

[Return to Table of Contents](#contents)
