#!/usr/bin/python3
"""
sCTkScrollableFrame

subclass of ScrollableFrame tuned for this ux

UI source file: sCTkScrollableFrame.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkScrollableFrameui as baseui
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#

class sCTkScrollableFrame(baseui.sCTkScrollableFrameUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        theme_defaults = {
            # 🔲 Outer Container Framework
            "border_width": 1.5,
            "border_color": ("#64748B", "#94A3B8"),  # Light Mode: Solid Slate | Dark Mode: High-Contrast Light Slate
            "corner_radius": 8,  # Smoothly rounded outer container edges

            # 🎨 Base Canvas Surface Layers
            # Matches your clean Entry field values for structural symmetry
            "fg_color": ("#FFFFFF", "#111827"),
            "label_fg_color": "transparent",  # Hides inner header label blocks if utilized

            # 🎛️ Internal Scrollbar Track Synchronization
            "scrollbar_button_color": ("#64748B", "#4B5563"),
            "scrollbar_button_hover_color": ("#1A4375", "#2471A3"),

            # ⛔ Muted Disabled Overlay
            "disabled_map": {
                "border_color": ("#CBD5E1", "#374151"),
                "scrollbar_button_color": ("#CBD5E1", "#1F2937")
            }
        }

        # Store dictionary references safely onto instance memory
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # Run our shared theme logic first to sanitize parameters and merge dictionaries
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # THE LOCAL FIX: Cleanly pop out "font" locally if it bled into self.final_kw!
        # This shields CustomTkinter's scrollable frame constructor from throwing an error.
        self.final_kw.pop("font", None)

        # Initialize CustomTkinter with the clean final kwargs array securely
        super().__init__(master, **self.final_kw)

    def state(self, mode: str):
        """
        Universal recursive scrollable container state controller.
        Mutes outer boundaries, locks down internal scrollbars, completely absorbs
        hover glow reactions, and cascades state changes down to children.
        """
        mode = mode.lower()

        if mode in ("normal", "enabled", "active"):
            # 1. Restore the frame's active borders and native hover color highlights
            self.configure(
                border_color=self.final_kw.get("border_color", self._local_defaults.get("border_color")),
                scrollbar_button_color=self.final_kw.get("scrollbar_button_color",
                                                         self._local_defaults.get("scrollbar_button_color")),
                scrollbar_button_hover_color=self.final_kw.get("scrollbar_button_hover_color",
                                                               self._local_defaults.get("scrollbar_button_hover_color"))
            )
            self._custom_current_state = "normal"

        elif mode == "disabled":
            # 2. Extract your custom soft muted silver-gray traces from your dictionary map
            target_disabled_color = self._custom_disabled_map.get("scrollbar_button_color", ("#CBD5E1", "#1F2937"))

            updates = {}
            if "border_color" in self._custom_disabled_map:
                updates["border_color"] = self._custom_disabled_map["border_color"]

            if "scrollbar_button_color" in self._custom_disabled_map:
                updates["scrollbar_button_color"] = target_disabled_color
                # Forces the hover color to match the resting color perfectly when locked down
                updates["scrollbar_button_hover_color"] = target_disabled_color

            try:
                self.configure(**updates)
            except Exception:
                pass

            self._custom_current_state = "disabled"

        # 🚀 RECURSIVE CASCADING: Loop over all widgets packed inside the scrollable inner canvas window
        for child in self.winfo_children():
            if hasattr(child, "winfo_children"):
                for inner_child in child.winfo_children():
                    if hasattr(inner_child, "state") and callable(getattr(inner_child, "state")):
                        try:
                            inner_child.state(mode)
                        except Exception:
                            pass

            if hasattr(child, "state") and callable(getattr(child, "state")):
                try:
                    child.state(mode)
                except Exception:
                    pass


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("600x450")
    root.title("Dynamic Scrollable Workspace Panel")

    # Instantiate our theme-protected scrollable frame card
    widget = sCTkScrollableFrame(root)
    widget.pack(expand=True, fill="both", padx=30, pady=30)

    # Inject a high-contrast Header Section at the top of the scroller
    from sCTkLabelPrimary import sCTkLabelPrimary

    header = sCTkLabelPrimary(widget, text="Transceiver Channel Frequency Monitor", anchor="w")
    header.pack(fill="x", padx=15, pady=(10, 15))

    # Inject form fields directly inside the scrolling canvas
    from sCTkEntryPrimary import sCTkEntryPrimary

    vfo_input = sCTkEntryPrimary(widget, placeholder_text="Enter manual calibration offset (MHz)...")
    vfo_input.pack(fill="x", padx=15, pady=10)

    # Dynamic Text Generator Loop! Injects 20 rows to force overflow limits naturally
    from sCTkLabelSecondary import sCTkLabelSecondary

    for channel_id in range(1, 21):
        frequency_mhz = 14.150 + (channel_id * 0.025)
        channel_row = sCTkLabelSecondary(
            widget,
            text=f"CH-{channel_id:02d} | Frequency Status: {frequency_mhz:.3f} MHz | Signal Trace: ACTIVE",
            anchor="w"
        )
        channel_row.pack(fill="x", padx=15, pady=4)

    # Inject primary action button control at the bottom
    from sCTkButtonPrimary import sCTkButtonPrimary

    sync_btn = sCTkButtonPrimary(widget, text="Synchronize Active VFO Banks")
    sync_btn.pack(padx=20, pady=15)

    # 🔄 Verify our custom cascading state system locks down the entire panel hierarchy instantly!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("Container Scrollable Frame tracker =", widget.get_state())
    print("Nested Entry Box tracker           =", vfo_input.get_state())
    print("Nested Sync Button tracker         =", sync_btn.get_state())

    # 🔄 Verify the cascade pipeline unlocks everything smoothly right back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("Container Scrollable Frame tracker =", widget.get_state())
    print("Nested Entry Box tracker           =", vfo_input.get_state())
    print("Nested Sync Button tracker         =", sync_btn.get_state())

    root.mainloop()
