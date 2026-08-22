## sCTkFrameLabeledPrimary

### Table of Contents
* [API Property Reference](#api-property-reference)
* [Constructor](#constructor)
* [Centralized Stylesheet Setup](#centralized-stylesheet-setup-sctkthemesjson)
* [Other Notes](#other-notes)
* [Implementation Example & Test Harness](#implementation-example--test-harness)

---

A clean, theme-compliant custom header-labeled scrollable container card frame. It is engineered to act as an organized panel matrix tree that seamlessly suppresses visible scrollbar components out of view by hard-matching scrollbar pixels directly to frame asset color backgrounds.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkScrollableFrame(master)` | `sCTkFrameLabeledPrimary(master)` *(Header Scroll Frame Chassis)* |
| **File Mapping** | Component files run standalone under un-themed frameworks. | Separated safely across `sCTkFrameLabeledPrimary.py` and `ThemeableWidget.py`. |
| **State Lock** | `self.configure(state="disabled")`<br>*(Crashes Natively)* | `scroll_panel.state("disabled")`<br>**OR**<br>`scroll_panel.configure(state="disabled")`<br><br>**Dual-Routing State Pipeline:** Safely catches state keywords, popping them out to block native verification validation crashes while running custom theme maps manually. |
| `winfo_children()` / `get_children()` | Returns private system canvas and structural background frames. | **Chassis Child Interceptor:** Overrides layout trees to extract **ONLY** the true, user-placed widget components nested inside the container. |

---

### Constructor

Initialize a custom scrollable labeled container frame option deck card. Scrollbar tracks are hidden automatically upon completing instantiation passes.

```python
# Instantiate a primary header-labeled scrollable matrix panel deck frame
channel_grid = sCTkFrameLabeledPrimary(
    master=root_window,
    label_text="RIG CHANNEL MATRIX CONTROLLER"
)

# Render the widget container view using standard geometry packer layout trackers
channel_grid.pack(expand=True, fill="both", padx=25, pady=25)
```

---

### Centralized Stylesheet Setup (`sCTkThemes.json`)
```json
{
    "sCTkFrameLabeledPrimary": {
        "fg_color": ["#FFFFFF", "#1E293B"],
        "border_color": ["#E2E8F0", "#334155"],
        "label_text_color": ["#1A4375", "#38BDF8"],
        "border_width": 1,
        "corner_radius": 8,
        "disabled_map": {
            "fg_color": ["#F1F5F9", "#111111"],
            "border_color": ["#E2E8F0", "#222222"],
            "label_text_color": ["#94A3B8", "#4B5563"]
        }
    }
}
```

### Other notes
* **Chassis Child Interceptor Shield:** Calling standard native `.winfo_children()` on a scrollable canvas widget leaks CustomTkinter's private system geometry framework bars (`_parent_frame`, `_view_frame`, etc.). This override cuts directly to the true internal workspace array, returning clean arrays of only your custom widgets.
* **Scrollbar Suppression Engine:** Instead of executing complex system canvas unbinding loops that destroy track physics, `_hide_internal_scrollbars()` sets scroll widths down to zero and maps track colors to your frame background, matching panel pixels perfectly.

---

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed an `sCTkFrameLabeledPrimary` alongside a cascading state loop tracker.

```python
#!/usr/bin/python3
"""
sCTkFrameLabeledPrimary - Standalone Interactive Testing Harness
"""
import customtkinter as ctk

# =====================================================================
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import sCTkThemes                    # 🔍 Duplicate import kept close for script scannability
from sCTkFrame import sCTkFrame      # Testing application wrapper container frame
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkFrameLabeledPrimary import sCTkFrameLabeledPrimary

if __name__ == "__main__":
    # Natively resolves your package assets and populates configurations cleanly
    sCTkThemes.apply_sCTkThemes()

    root = ctk.CTk()
    root.geometry("450x450")
    root.title("Labeled Scrollable Frame Test Bench")

    # Instantiate your custom scrollable primary frame container
    scroll_panel = sCTkFrameLabeledPrimary(root, label_text="RIG CHANNEL MATRIX CONTROLLER")
    scroll_panel.pack(expand=True, fill="both", padx=25, pady=25)

    # Populate scroll panel container layout slots with sCTkLabelSecondary items
    for i in range(1, 21):
        lbl_item = sCTkLabelSecondary(scroll_panel, text=f"Channel Lane Array Entry #{i:02d} - Active Track [100Hz]")
        lbl_item.pack(pady=4, fill="x", padx=10)

    def toggle_frame_states():
        """Toggles the container panel and cascades the state down to all child widgets."""
        current_mode = scroll_panel.get_state()
        target = "disabled" if current_mode == "normal" else "normal"

        # 1. Update the parent scrollable frame's visual layout variables via dual-routing syntax
        scroll_panel.configure(state=target)

        # 2. Extract your children using our newly targeted intercept loop pass
        true_children = scroll_panel.winfo_children()
        print(f"DEBUG ASSERTER: Successfully captured {len(true_children)} label elements...")

        # 3. Cascade the state change down to every single true child label uniformly
        for child in true_children:
            if hasattr(child, "configure"):
                child.configure(state=target)

        btn_toggle.configure(
            text="Lock Container (Set 'disabled')" if target == "normal" else "Unlock Container (Set 'normal')")
        print(f"Logged Verification Hook -> scroll_panel.get_state() = {scroll_panel.get_state()}\n")

    btn_toggle = ctk.CTkButton(root, text="Lock Container (Set 'disabled')", command=toggle_frame_states)
    btn_toggle.pack(pady=15)

    # Run the interactive boot tracking logs
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    scroll_panel.state("disabled")
    print(f"state (Disabled Pass) = {scroll_panel.get_state().upper()}")

    scroll_panel.state("normal")
    print(f"state (Normal Pass)   = {scroll_panel.get_state().upper()}")
    print("========================================\n")

    root.mainloop()
```

[Return to Table of Contents](#contents)
