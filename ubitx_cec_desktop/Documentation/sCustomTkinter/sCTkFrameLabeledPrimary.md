## sCTkFrameLabeledPrimary

A specialized, theme-compliant scrollable container frame variant engineered to cleanly hide its vertical scrollbars by matching their canvas color rendering attributes to the frame background while collapsing their structural footprint down to zero width. 

This layout technique preserves native mousewheel scrolling metrics while rendering a seamless, static frame panel profile across both light and dark system appearance modes.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkScrollableFrame(master)` | `sCTkFrameLabeledPrimary(master)` *(Scrollable Container)* |
| **Maintenance** | Local style overrides duplicated across files manually. | Clean updates across all layouts modified directly in the JSON file. |
| **File Mapping** | Everything runs under one core native layout pipeline. | Separated safely across `sCTkFrameLabeledPrimary.py`, `sCTkFrameLabeledPrimaryui.py`, and `ThemeableWidget.py`. |
| `state(mode)` | *Not Available Natively* | `Method (str)` handling layout tracking map transformations (`'normal'`, `'disabled'`). |
| `get_state()` | *Not Available Natively* | `Method -> str` explicit verification query matching system test assertions. |
| `winfo_children()` | Returns private internal system wrapper frames. | **Overridden:** Returns only true user-placed child component widgets. |
| `get_children()` | *Not Available Natively* | **Companion Shortcut:** Direct pipeline alias pointing to `winfo_children()`. |

---

### Constructor

Initialize a custom scrollable container instance. Label headers, title typography lines, and bounding corner radii parameters can be passed natively or handled entirely out of stylesheet registries.

```python
# Instantiate a theme-compliant scrollable container frame
channel_matrix = sCTkFrameLabeledPrimary(
    master=main_deck_frame,
    label_text="RIG CHANNEL MATRIX CONTROLLER",
    corner_radius=8
)

# Render the widget inside your parent container geometry packer panel
channel_matrix.pack(fill="both", expand=True, padx=25, pady=25)
```

---

### Convenience Functions
```python
# Evaluate active visual modes or apply absolute user interaction locks
current_mode = channel_matrix.get_state()   # Returns 'normal' or 'disabled'
channel_matrix.state("disabled")             # Shifts container accents and hides tracks seamlessly

# Extract only your true user-placed child elements (Bypasses hidden canvas layout frames)
for child in channel_matrix.winfo_children():
    if hasattr(child, "configure"):
        child.configure(state="disabled")
```

### Centralized Stylesheet Setup (`themes.json`)
```json
{
    "sCTkFrameLabeledPrimary": {
        "fg_color": ["#F8FAFC", "#262626"],
        "border_color": ["#E2E8F0", "#1A1A1A"],
        "label_text_color": ["#1A4375", "#FFFFFF"],
        "label_font": ["Arial", 12, "bold"],
        "disabled_map": {
            "fg_color": ["#F1F5F9", "#1E1E1E"],
            "border_color": ["#CBD5E1", "#2D2D2D"],
            "label_text_color": ["#94A3B8", "#4B5563"]
        }
    }
}
```

### Other notes
* **Universal Absorption Guard:** Because native CustomTkinter frames will crash if passed an unrecognized `state` parameter, the custom `configure` method absorbs the key, filters it completely out of the execution stream, and safely routes it to the custom state manager thread.
* **Encapsulated Child Interceptor:** Overriding `winfo_children()` forces queries past CustomTkinter's deep `_parent_frame._view_frame` container hierarchy, mapping developer loop tracks straight onto your child widgets automatically.
* **Dynamic Repaint Hooks:** The scrollbar track concealment function (`_hide_internal_scrollbars`) is linked directly to the core visual update cycle. If the container background shifts colors or switches themes, the scrollbars dynamically update instantly.

### Implementation Example & Test Harness

Below is a complete, self-contained script demonstrating how to layout a scrollable panel card and cascade state updates down to its child content modules uniformly.

```python
import customtkinter as ctk
from sCTkFrameLabeledPrimary import sCTkFrameLabeledPrimary
from sCTkLabelSecondary import sCTkLabelSecondary


def toggle_frame_states():
    """Toggles the container panel and cascades the state down to all child widgets."""
    current_mode = scroll_panel.get_state()
    target = "disabled" if current_mode == "normal" else "normal"

    # 1. Update the parent scrollable frame's visual layout variables
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


if __name__ == "__main__":
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

    btn_toggle = ctk.CTkButton(root, text="Lock Container (Set 'disabled')", command=toggle_frame_states)
    btn_toggle.pack(pady=15)

    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    print(f"Initial Container State = {scroll_panel.get_state().upper()}")
    print("========================================\n")

    root.mainloop()
```
