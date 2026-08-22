## sCTkFrameLabeledSecondary

A theme-compliant scrollable auxiliary container frame variant designed for helper panels, meta blocks, or setting grids. It natively conceals vertical scrollbar elements by locking their track colors to the panel background and flattening handle geometries to zero width. 

This configuration keeps mousewheel scrolling intact while maintaining cross-platform system-level appearance mode adjustments.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkScrollableFrame(master)` | `sCTkFrameLabeledSecondary(master)` *(Secondary container)* |
| **Maintenance** | Local style configurations duplicated manually across files. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Everything runs under one core native framework layout layer. | Separated safely across `sCTkFrameLabeledSecondary.py`, `sCTkFrameLabeledSecondaryui.py`, and `ThemeableWidget.py`. |
| `state(mode)` | *Not Available Natively* | `Method (str)` handling layout tracking map transformations (`'normal'`, `'disabled'`). |
| `get_state()` | *Not Available Natively* | `Method -> str` explicit verification query matching system test assertions. |
| `winfo_children()` | Returns private internal system structural frames. | **Overridden:** Returns only true user-placed child component widgets. |
| `get_children()` | *Not Available Natively* | **Companion Shortcut:** Direct pipeline alias pointing to `winfo_children()`. |

---

### Constructor

Initialize a custom secondary scrollable container frame instance. Header labels and theme layouts map cleanly out of central stylesheet parameters.

```python
# Instantiate a secondary scrollable layout container frame panel card
metadata_deck = sCTkFrameLabeledSecondary(
    master=workspace_panel,
    label_text="AUXILIARY METADATA TRACK MATRIX"
)

# Render the widget inside your parent container coordinate tracker layout
metadata_deck.pack(fill="both", expand=True, padx=25, pady=25)
```

---

### Convenience Functions
```python
# Evaluate active visual modes or apply absolute user interaction locks
current_mode = metadata_deck.get_state()   # Returns 'normal' or 'disabled'
metadata_deck.state("disabled")             # Shifts container accents and hides tracks seamlessly

# Extract only your true user-placed child elements (Bypasses hidden canvas layout frames)
for child in metadata_deck.winfo_children():
    if hasattr(child, "configure"):
        child.configure(state="disabled")
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkFrameLabeledSecondary": {
        "fg_color": ["#FAFAFA", "#1A1A1A"],
        "border_color": ["#CBD5E1", "#2D2D2D"],
        "label_text_color": ["#475569", "#9CA3AF"],
        "label_font": ["Arial", 11, "italic"],
        "disabled_map": {
            "fg_color": ["#F1F5F9", "#121212"],
            "border_color": ["#E2E8F0", "#1F1F1F"],
            "label_text_color": ["#94A3B8", "#4B5563"]
        }
    }
}
```

### Other notes
* **Universal Absorption Guard:** Intercepts incoming `state` configuration commands, popping them completely out of the core keyword stream to protect native CustomTkinter validation threads from fatal unhandled type exceptions.
* **Encapsulated Child Interceptor:** Overriding `winfo_children()` bypasses CustomTkinter's private intermediate frame tree wrapper mapping array, safely exposing your actual layout label components directly.


### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to use an `sCTkFrameLabeledSecondary` and access children.

```python
# !/usr/bin/python3
"""
sCTkFrameLabeledSecondary - Standalone Interactive Testing Harness
"""
import customtkinter as ctk
from sCTkFrameLabeledSecondary import sCTkFrameLabeledSecondary
from sCTkLabelTertiary import sCTkLabelTertiary


def toggle_frame_states():
    """Toggles the container panel and cascades the state down to all child widgets."""
    current_mode = scroll_panel.get_state()
    target = "disabled" if current_mode == "normal" else "normal"

    # 1. Update the parent scrollable frame's visual layout variables
    scroll_panel.configure(state=target)

    # 2. Native standard cascade loop leveraging your winfo_children() override
    true_children = scroll_panel.winfo_children()
    print(f"DEBUG ASSERTER: Successfully captured {len(true_children)} label elements...")

    for child in true_children:
        if hasattr(child, "configure"):
            child.configure(state=target)

    btn_toggle.configure(
        text="Lock Container (Set 'disabled')" if target == "normal" else "Unlock Container (Set 'normal')")
    print(f"Logged Verification Hook -> scroll_panel.get_state() = {scroll_panel.get_state()}\n")


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("450x450")
    root.title("Labeled Scrollable Secondary Frame Test Bench")

    # Instantiate your custom scrollable secondary frame container
    scroll_panel = sCTkFrameLabeledSecondary(root, label_text="AUXILIARY METADATA TRACK MATRIX")
    scroll_panel.pack(expand=True, fill="both", padx=25, pady=25)

    # Populate scroll panel container slots with helper sCTkLabelTertiary notice items
    for i in range(1, 21):
        lbl_item = sCTkLabelTertiary(scroll_panel,
                                     text=f"Helper Node Index [ID: {i:02d}] - Calibration Offset [0.00Hz]")
        lbl_item.pack(pady=4, fill="x", padx=10)

    btn_toggle = ctk.CTkButton(root, text="Lock Container (Set 'disabled')", command=toggle_frame_states)
    btn_toggle.pack(pady=15)

    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    print(f"Initial Container State = {scroll_panel.get_state().upper()}")
    print("========================================\n")

    root.mainloop()

```