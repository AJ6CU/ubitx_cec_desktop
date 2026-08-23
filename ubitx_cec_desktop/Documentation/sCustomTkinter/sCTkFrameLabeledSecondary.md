## sCTkFrameLabeledSecondary

### Table of Contents
* [API Property Reference](#api-property-reference)
* [Constructor](#constructor)
* [Advanced Layout Inspection API](#advanced-layout-inspection-api)
* [Centralized Stylesheet Setup](#centralized-stylesheet-setup-sctkthemesjson)
* [Other Notes](#other-notes)
* [Implementation Example & Test Harness](#implementation-example--test-harness)

---

An auxiliary/secondary header-labeled scrollable container frame variant designed for background telemetry arrays, sub-metadata node grids, and secondary logging layouts. It natively masks internal scrollbar components out of view by hard-matching scrollbar pixels directly to frame layout canvas colors [INDEX].

*For main matrix controls or primary operational card views, see the dominant component documentation page:* [sCTkFrameLabeledPrimary](sCTkFrameLabeledPrimary.md).

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkFrame(master)` *(No label natively)* | `sCTkFrameLabelPrimary/Secondary(master)` *(Labeled Frame Enclosure)* |
| **File Mapping** | Config metrics look up loose un-managed palette snapshot lists. | Separated safely across the class script and `ThemeableWidget.py`. |
| `winfo_children()` | Returns raw internal widgets, including heading text blocks. | Overridden signature supporting filtered inner form component lookups. |
| `get_children()` | *Not Supported Natively* | Convenience method returning clean application-level custom components. |
| `get_all_children()` | *Not Supported Natively* | Convenience method returning direct, unfiltered access to the entire core frame tree. |

---

### Constructor

Initialize a custom secondary scrollable labeled container card instance. Scrollbars adjust their width metrics directly upon initialization passes [INDEX].

```python
# Instantiate a secondary header-labeled scrollable matrix panel deck frame
metadata_grid = sCTkFrameLabeledSecondary(
    master=root_window,
    label_text="AUXILIARY METADATA TRACK MATRIX"
)

# Render the widget container view using standard geometry packer layout trackers
metadata_grid.pack(expand=True, fill="both", padx=25, pady=25)
```

### Advanced Layout Inspection API

Because labeled frame capsules bundle an integrated text header directly onto their border chassis, native widget sweeps can accidentally overwrite heading text constraints. The class overrides window queries to isolate your layout data cleanly.

#### `winfo_children(include_private: bool = False) -> list`

* **`include_private=False` (Default):** Isolates and hides the internal `CTkLabel` heading widget and frame layout backplane blocks. Loops crawling your dashboard lanes will discover only the actual primary input rows packed inside the box, preventing title typography parameters from getting corrupted during runtime style shifts.
* **`include_private=True`:** Immediately deactivates the filter mesh to return the raw, unmanipulated Tkinter structural window lineage hierarchy.



### Centralized Stylesheet Setup (`sCTkThemes.json`)
```json
{
    "sCTkFrameLabeledSecondary": {
        "fg_color": ["#FAFAFA", "#11141A"],
        "border_color": ["#CBD5E1", "#222933"],
        "label_text_color": ["#475569", "#94A3B8"],
        "border_width": 1,
        "corner_radius": 6,
        "disabled_map": {
            "fg_color": ["#F1F5F9", "#0A0D14"],
            "border_color": ["#E2E8F0", "#171C24"],
            "label_text_color": ["#94A3B8", "#4B5563"]
        }
    }
}
```

### Other notes
* **Chassis Child Interceptor Shield:** Calling standard native `.winfo_children()` on a scrollable canvas widget leaks CustomTkinter's private system geometry framework bars (`_parent_frame`, `_view_frame`, etc.) [INDEX]. This override cuts directly to the true internal workspace array, returning clean arrays of only your custom widgets [INDEX].
* **Scrollbar Suppression Engine:** Instead of executing complex system canvas unbinding loops that destroy track physics, `_hide_internal_scrollbars()` sets scroll widths down to zero and maps track colors to your frame background, matching panel pixels perfectly [INDEX].

---

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed an `sCTkFrameLabeledSecondary` alongside a cascading state loop tracker [INDEX].

```python
#!/usr/bin/python3
"""
sCTkFrameLabeledSecondary - Standalone Interactive Testing Harness
"""
import customtkinter as ctk

# =====================================================================
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import sCTkThemes                    # 🔍 Duplicate import kept close for script scannability
from sCTkFrame import sCTkFrame      # Testing application wrapper container frame
from sCTkLabelTertiary import sCTkLabelTertiary
from sCTkFrameLabeledSecondary import sCTkFrameLabeledSecondary

if __name__ == "__main__":
    # Natively resolves your package assets and populates configurations cleanly [INDEX]
    sCTkThemes.apply_sCTkThemes()

    root = ctk.CTk()
    root.geometry("450x450")
    root.title("Labeled Scrollable Secondary Frame Test Bench")

    # Instantiate your custom scrollable secondary frame container [INDEX]
    scroll_panel = sCTkFrameLabeledSecondary(root, label_text="AUXILIARY METADATA TRACK MATRIX")
    scroll_panel.pack(expand=True, fill="both", padx=25, pady=25)

    # Populate scroll panel container slots with helper sCTkLabelTertiary notice items [INDEX]
    for i in range(1, 21):
        lbl_item = sCTkLabelTertiary(scroll_panel, text=f"Helper Node Index [ID: {i:02d}] - Calibration Offset [0.00Hz]")
        lbl_item.pack(pady=4, fill="x", padx=10)

    def toggle_frame_states():
        """Toggles the container panel and cascades the state down to all child widgets [INDEX]."""
        current_mode = scroll_panel.get_state()
        target = "disabled" if current_mode == "normal" else "normal"

        # 1. Update the parent scrollable frame's visual layout variables via dual-routing syntax [INDEX]
        scroll_panel.configure(state=target)

        # 2. Native standard cascade loop leveraging your winfo_children() override [INDEX]
        true_children = scroll_panel.winfo_children()
        print(f"DEBUG ASSERTER: Successfully captured {len(true_children)} label elements...")

        for child in true_children:
            if hasattr(child, "configure"):
                child.configure(state=target)

        btn_toggle.configure(
            text="Lock Container (Set 'disabled')" if target == "normal" else "Unlock Container (Set 'normal')")
        print(f"Logged Verification Hook -> scroll_panel.get_state() = {scroll_panel.get_state()}\n")

    btn_toggle = ctk.CTkButton(root, text="Lock Container (Set 'disabled')", command=toggle_frame_states)
    btn_toggle.pack(pady=15)

    # Run the interactive boot tracking logs [INDEX]
    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    scroll_panel.state("disabled")
    print(f"state (Disabled Pass) = {scroll_panel.get_state().upper()}")

    scroll_panel.state("normal")
    print(f"state (Normal Pass)   = {scroll_panel.get_state().upper()}")
    print("========================================\n")

    root.mainloop()
```

[Return to Table of Contents](#contents)
