
```

## sCTkScrollbar

The sCTkScrollbar is an advanced, theme-compliant custom scrollbar element designed for the uBitx desktop transceiver interface. It inherits directly from ctk.CTkScrollbar to preserve Method Resolution Order (MRO) theme tracking while embedding direct event-interception buffers.


### Table of Contents
* [API Property Reference](#api-property-reference)
* [Constructor](#constructor)
* [Centralized Stylesheet Setup](#centralized-stylesheet-setup-sctkthemesjson)
* [Other Notes](#other-notes)
* [Implementation Example & Test Harness](#implementation-example--test-harness)

---

An advanced, theme-compliant custom scrollbar element designed for the uBitx desktop transceiver interface. It inherits directly from `ctk.CTkScrollbar` to preserve Method Resolution Order (MRO) theme tracking while embedding direct event-interception buffers.

### API Property Reference

| Property / Feature | Standard CustomTkinter | Your `sCustomTkinter` Setup |
| :--- | :--- | :--- |
| **Instantiation** | `ctk.CTkScrollbar(master)` | `sCTkScrollbar(master)` *(Isolated External Scroll Handle)* |
| **File Mapping** | Everything runs under one core native framework layout tracker. | Separated safely across `sCTkScrollbar.py` and `ThemeableWidget.py`. |
| **State Lock** | Natively handles basic disabled flags, but drops theme sync if locked. | `scrollbar.state("disabled")`<br>**OR**<br>`scrollbar.configure(state="disabled")`<br><br>**Theme-Preserving State Bypasser:** Absorbs state changes smoothly. The button desaturation updates while the scrollbar handle remains completely reactive to dark/light look switches natively. |
| `get_state()` | *Not Supported Natively* | `Method -> str` explicit verification query matching system test assertions, returning `"normal"` or `"disabled"`. |
| `bind_to_view()` | Uses implicit/direct hooks. | `Method -> None` explicitly binds mouse wheel and high-precision trackpads exclusively to the scrolling target widget. |

---

### Constructor

Initialize a custom theme-compliant scrollbar handle instance.Sizing matrices, hover behaviors, and button background colors map cleanly out of central stylesheet parameters.

```python
#### Initialize your custom scrollbar on the layout right channel lane
scrollbar = sCTkScrollbar(
    master=main_layout,
    orientation="vertical"
)
scrollbar.pack(side="right", fill="y", padx=(5, 10), pady=10)

#### Connect scroll listeners exclusively to the view to avoid frame corruption
scrollbar.bind_to_view(scroll_view)
```

### Core Component Integration Rules

To maintain high-load performance and prevent layout caching locks across active or disabled operational states, the scrollbar must follow strict design rules:
* Zero Lineage Crawling: Never use recursive loops to unbind or sweep parent layout frame paths. Forcing event manipulation on composite container frames deletes CustomTkinter's private theme tracking listeners.
* Isolated View Binding: Explicitly pass the specific scrolling viewport destination target directly down to the scrollbar handle instance at initialization.

#### Proper Viewport Target Attachment

Because a native ctk.CTkScrollableFrame isolates its interior viewport frame container inside a nested hierarchy to prevent external tampering, attempting to pass scroll_view.yview directly will throw an AttributeError. 

To connect the scrollbar natively without hitting any private input validation filters, the application must extract the hidden core canvas component from the container layout matrix.

#### Extraction and Alignment Hook Pattern

```python
# 1. Initialize your custom scrollbar on the layout right channel lane
scrollbar = sCTkScrollbar(main_layout, orientation="vertical")
scrollbar.pack(side="right", fill="y", padx=(5, 10), pady=10)

# 2. Extract the native underlying canvas element sitting interior to the scrollable frame shell
actual_canvas = None
for child in scroll_view.winfo_children():
    if child.__class__.__name__ in ("CTkCanvas", "Canvas"):
        actual_canvas = child
        break

if actual_canvas:
    # 3. Link the canvas coordinate tracking streams natively down beneath the validator filters
    actual_canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=actual_canvas.yview)

# 4. Safely connect scroll listeners exclusively to the view to avoid frame corruption
scrollbar.bind_to_view(scroll_view)



### Centralized Stylesheet Setup (`sCTkThemes.json`)


```json
{
    "sCTkScrollbar": {
        "fg_color": "transparent",
        "button_color": ["#94A3B8", "#475569"],
        "button_hover_color": ["#64748B", "#334155"],
        "border_width": 0,
        "disabled_map": {
            "button_color": ["#E2E8F0", "#1E293B"]
        }
    }
}
```

### Other notes
* **Zero Lineage Crawling:** Never use recursive loops to unbind or sweep parent layout frame paths. Forcing event manipulation on composite container frames deletes CustomTkinter's private theme tracking listeners.
* **Structural Canvas Extraction:** Because a native `ctk.CTkScrollableFrame` isolates its interior viewport frame container inside a nested hierarchy, attempting to pass `scroll_view.yview` directly will throw an `AttributeError`. The harness code must extract the hidden core canvas component to properly link tracking streams below the validator filters.

---

### Implementation Example & Test Harness

Below is a complete, self-contained test execution script demonstrating how to properly embed an `sCTkScrollbar` asset container alongside a clean native canvas interconnect hook pass.

```python
#!/usr/bin/python3
"""
sCTkScrollbar - Standalone Interactive Testing Harness
"""
import customtkinter as ctk

# =====================================================================
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import sCTkThemes                    
from sCTkFrame import sCTkFrame
from sCTkButtonPrimary import sCTkButtonPrimary
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkScrollbar import sCTkScrollbar

if __name__ == "__main__":
    sCTkThemes.apply_sCTkThemes()

    root = ctk.CTk()
    root.geometry("480x450")
    root.title("sCTkScrollbar Validation Bench")

    # 1. Main visual layout shell container panel
    main_layout = sCTkFrame(root)
    main_layout.pack(expand=True, fill="both", padx=15, pady=15)

    # Live Operational Telemetry Status Monitoring Bar
    status_monitor = sCTkLabelSecondary(
        main_layout, 
        text="SYSTEM STATUS CORE TRACK LANE: [ACTIVE / NORMAL]"
    )
    status_monitor.pack(fill="x", padx=10, pady=(5, 5))

    # TOP-DECK INTERACTIVE MANAGEMENT MATRIX
    def toggle_operational_lock():
        """Cycles the layout rows state based on a pristine tracking pointer."""
        global _view_locked
        
        if not _view_locked:
            target = "disabled"
            _view_locked = True
            btn_lock.configure(text="Enable Telemetry View")
            status_monitor.configure(text="SYSTEM STATUS CORE TRACK LANE: [LOCKED / DISABLED]")
        else:
            target = "normal"
            _view_locked = False
            btn_lock.configure(text="Disable Telemetry View")
            status_monitor.configure(text="SYSTEM STATUS CORE TRACK LANE: [ACTIVE / NORMAL]")
            
        scrollbar.configure(state=target)
        
        # Cascade configuration maps ONLY to content text label elements
        for label_widget in scroll_content.winfo_children():
            if hasattr(label_widget, "state") and "Label" in label_widget.__class__.__name__:
                label_widget.state(target)

    def toggle_appearance_skin():
        current_mode = ctk.get_appearance_mode()
        target = "Light" if current_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(target)

    _view_locked = False

    btn_lock = sCTkButtonPrimary(main_layout, text="Disable Telemetry View", command=toggle_operational_lock)
    btn_lock.pack(fill="x", padx=10, pady=(2, 5))

    btn_theme = sCTkButtonPrimary(main_layout, text="Toggle Theme Skin (Dark / Light)", command=toggle_appearance_skin)
    btn_theme.pack(fill="x", padx=10, pady=(0, 10))

    # Standard layout background container frame card panel
    content_chassis = sCTkFrame(main_layout)
    content_chassis.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

    # The pristine native scroll view region manages internal canvas themes automatically
    scroll_view = ctk.CTkScrollableFrame(content_chassis, fg_color="transparent")
    scroll_view.pack(fill="both", expand=True)

    # Unpack the underlying frame window out of CustomTkinter safely
    scroll_content = scroll_view._parent_frame

    # Populate with theme-aware secondary text label rows using grid alignment parameters
    for i in range(25):
        lbl_item = sCTkLabelSecondary(scroll_content, text=f"▶ Transceiver Core Channel Lane Code: {100 + i} [STATUS: OK]")
        lbl_item.grid(row=i, column=0, sticky="w", padx=10, pady=4)

    # Initialize the custom scrollbar on the layout right channel lane
    scrollbar = sCTkScrollbar(main_layout, orientation="vertical")
    scrollbar.pack(side="right", fill="y", padx=(5, 10), pady=10)
    
    # Unpack the native underlying canvas element sitting interior to the ScrollableFrame block
    actual_canvas = None
    for child in scroll_view.winfo_children():
        if child.__class__.__name__ in ("CTkCanvas", "Canvas"):
            actual_canvas = child
            break

    if actual_canvas:
        # Link the canvas yview coordinate tracking streams natively down beneath the validator filters
        actual_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=actual_canvas.yview)

    # Safely connect scroll listeners exclusively to the view to avoid frame corruption
    scrollbar.bind_to_view(scroll_view)

    root.mainloop()
```

[Return to Table of Contents](#contents)

