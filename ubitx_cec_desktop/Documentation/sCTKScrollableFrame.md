## sCTkScrollableFrame

### Table of Contents
* [API Property Reference](#api-property-reference)
* [Constructor](#constructor)
* [Convenience Functions](#convenience-functions)
* [Advanced Layout Inspection API](#advanced-layout-inspection-api)
* [Centralized Stylesheet Setup](#centralized-stylesheet-setup-sctkthemesjson)
* [Other Notes](#other-notes)

---

An advanced scrollable window viewport capsule inheriting from CustomTkinter's composite layouts [INDEX]. It overrides system tracking hooks to isolate background mouse-wheel parameters and freeze scrollbar slider dragging mechanics cleanly under an absolute runtime `.state("disabled")` loop while leaving internal input rows completely focusable [INDEX].

### API Property Reference


| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkScrollableFrame(master)` | `sCTkScrollableFrame(master)` *(Themed Viewport Container)* |
| **File Mapping** | Config metrics look up loose un-managed palette snapshot lists. | Separated safely across `sCTkScrollableFrame.py` and `ThemeableWidget.py`. |
| **State Lock** | *Not Supported Natively* | `test_frame.state("disabled")`<br>**OR**<br>`test_frame.configure(state="disabled")`<br><br>**Polymorphic State Controller:** Unbinds dragging events interior to the scroll frame's private canvas layer without mutating nested form element input values. |
| `winfo_children()` | Returns raw internal Tkinter tree widgets, including private scrollbars. | Overridden signature supporting filtered application widget lookups. |
| `get_children()` | *Not Supported Natively* | Convenience method returning clean application-level custom components. |
| `get_all_children()` | *Not Supported Natively* | Convenience method returning direct, unfiltered access to the entire core tree. |


---

### Constructor

Initialize a custom themed scrollable frame viewport layout chassis. It maps configuration boundaries natively.

```python
# Instantiate a telemetry logging scrollable list frame card
log_viewport = sCTkScrollableFrame(
    master=dashboard,
    width=380,
    height=250,
    label_text="Telemetry Viewport Container"
)

# Render the widget inside your container panel
log_viewport.pack(padx=20, pady=20, fill="both", expand=True)
```

---

### Convenience Functions
```python
# Evaluate current state configurations or apply absolute user interaction locks via dual-routing syntax
current_mode = log_viewport.get_state()      # Returns 'normal' or 'disabled' [INDEX]
log_viewport.state("disabled")               # Freezes the scroll handles and applies desaturated look fills [INDEX]
```

### Advanced Layout Inspection API

To insulate your structural look configurations from breaking when cascading loops pass through composite layouts, the system overrides native Tkinter window query behaviors.

#### `winfo_children(include_private: bool = False) -> list`

* **`include_private=False` (Default):** Drops private internal wrapper artifacts from appearing in clean application loops. The method dynamically strips out underlying `CTkScrollbar`, `CTkCanvas`, and raw `Canvas` components so layout managers and state controllers only target your functional custom entries and forms.
* **`include_private=True`:** Drops the filter shield instantly, returning the raw, unmanipulated C-level native Tkinter core window lineage tree for deep forensic tracking or platform diagnostics.

```python
# Pure application-layer cascade: Targets only form entries, skipping scrollbars natively
for widget in test_frame.winfo_children():
    widget.configure(state="disabled")

# Forensic debugging pass: Uncovers the hidden internal CustomTkinter layers
print(test_frame.winfo_children(include_private=True))
```


### Centralized Stylesheet Setup (`sCTkThemes.json`)
```json
{
    "sCTkScrollableFrame": {
        "fg_color": ["#FAFAFA", "#11141A"],
        "border_color": ["#CBD5E1", "#222933"],
        "label_fg_color": ["#E2E8F0", "#1A222D"],
        "scrollbar_button_color": ["#94A3B8", "#475569"],
        "scrollbar_button_hover_color": ["#64748B", "#334155"],
        "disabled_map": {
            "fg_color": ["#F1F5F9", "#0A0D14"],
            "border_color": ["#E2E8F0", "#171C24"],
            "label_fg_color": ["#F8FAFC", "#0D1117"],
            "scrollbar_button_color": ["#E2E8F0", "#1E293B"]
        }
    }
}
```
### Other Notes
* **Deep-Copy Dictionary Isolation Shield:** Because CustomTkinter's native frame constructor loops mutate and delete attributes directly out of raw dictionary data footprints during its boot pass, the constructor clones your configurations into `self._local_defaults = dict(self.final_kw)` beforehand. This preserves your color mappings safely [INDEX].
* **Private Event Interception:** Calling `.state("disabled")` triggers an explicit layout sweep that actively safely unbinds CustomTkinter's private `<B1-Motion>` and `<Button-1>` mouse trackers from the inner child canvas [INDEX].

### ⚠️ Critical Apple Touch & Multi-Platform Scrolling Constraint

When packing layout controls interior to an `sCTkScrollableFrame` view pane, **you must strictly avoid mixing native CustomTkinter widgets (e.g., `ctk.CTkEntry`, `ctk.CTkButton`) alongside your themed `sCustomTkinter` equivalents.** 

* **The Event Swallowing Trap:** Native `ctk` elements do not participate in our repository's unified recursive event-braid mesh. Because they aggressively capture touch focus inputs on macOS, any native element will act like a layout "black hole"—completely freezing trackpads and Apple Magic Mouse swipes the moment a user hovers their mouse cursor directly over that row.
* **The Resolution Rule:** Always pack your framework's custom theme-aligned classes (e.g., **`sCTkEntryPrimary`**, **`sCTkButtonPrimary`**, **`sCTkCheckBox`**). Because they inherit from our synchronized base mixins, they naturally allow high-precision touch parameters and traditional hardware scrollwheel click ticks to bubble straight up to the master viewport coordinate canvas flawlessly across macOS, Windows, and Linux.

---

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to embed an `sCTkScrollableFrame` along with an interactive toggle switch button [INDEX].

```python
#!/usr/bin/python3
"""
sCTkScrollableFrame - Standalone Interactive Testing Harness
"""
# =================================================================
# STANDALONE TEST HARNESS
# =================================================================
if __name__ == "__main__":
    import customtkinter as ctk
    import sCTkThemes
    from sCTkButtonPrimary import sCTkButtonPrimary
    from sCTkEntryPrimary import sCTkEntryPrimary
    from sCTkScrollableFrame import sCTkScrollableFrame

    root = ctk.CTk()
    root.title("ScrollableFrame Touch Verification")
    root.geometry("450x420")

    sCTkThemes.apply_sCTkThemes()

    test_frame = sCTkScrollableFrame(root, width=380, height=250, label_text="Telemetry Viewport Container")
    test_frame.pack(padx=20, pady=20, fill="both", expand=True)

    for i in range(12):
        mock_entry = sCTkEntryPrimary(test_frame, placeholder_text=f"Active Transceiver Channel {i + 1}")
        mock_entry.pack(padx=10, pady=5, fill="x")


    def toggle_container_state():
        current_state = test_frame.get_state()
        target = "disabled" if current_state == "normal" else "normal"

        # 1. Update the parent frame layout state cleanly
        test_frame.configure(state=target)

        # 2. Pure, clean cascade pass: Tell each child to update its state.
        # It is the ENTRY'S responsibility to know how to draw its own disabled skin!
        for entry_widget in test_frame.get_children():
            if hasattr(entry_widget, "configure"):
                try:
                    entry_widget.configure(state=target)
                except Exception:
                    pass


    toggle_btn = sCTkButtonPrimary(root, text="Enforce State: DISABLED", command=toggle_container_state)
    toggle_btn.pack(side="bottom", pady=15)

    test_frame._toggle_scroll_bindings(bind=True)
    root.mainloop()
```

[Return to Table of Contents](#contents)
