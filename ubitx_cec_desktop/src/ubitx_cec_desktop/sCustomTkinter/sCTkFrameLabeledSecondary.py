#!/usr/bin/python3
"""
sCTkFrameLabeledSecondary

A clean CustomTkinter ScrollableFrame that natively hides its scrollbars
by matching their color profile to the frame background.
"""
import customtkinter as ctk
from ThemeableWidget import ThemeableWidget


class sCTkFrameLabeledSecondary(ctk.CTkScrollableFrame, ThemeableWidget):
    properties = frozenset()

    def __init__(self, master=None, **kwargs):
        # 1. Fire our shared theme logic first. It automatically finds the class section inside themes.json
        ThemeableWidget.__init__(self, kwargs)

        # 2. Store your custom maps safely onto instance memory channels
        self._local_defaults = self.final_kw
        self._custom_disabled_map = self._widget_disabled_map

        # 3. Initialize CustomTkinter ScrollableFrame natively with final kwargs safely
        super().__init__(master, **self.final_kw)

        self._custom_current_state = "normal"

        # 4. Force initial scrollbar hiding execution pass
        self._hide_internal_scrollbars()

    def configure(self, *args, **kwargs):
        """Handles Pygubu designer queries and manages composite state updates safely."""

        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Pygubu Inspector compatibility check)
        # -----------------------------------------------------------------
        if args and len(args) == 1:
            pname = args
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "border_color", "label_text_color"]:
                current_state = str(self.state()).lower()
                val = self._custom_disabled_map.get(pname) if current_state == "disabled" else self._local_defaults.get(
                    pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            return super().configure(pname)

        # Handle Pygubu positional dictionary merging layers cleanly
        if args and isinstance(args, dict):
            kwargs = args | kwargs

        # -----------------------------------------------------------------
        # ZONE B: SUB-COMPONENT STATE INTERCEPTION
        # -----------------------------------------------------------------
        if "state" in kwargs:
            target_state = kwargs.pop("state")
            self.state(target_state)

        # -----------------------------------------------------------------
        # ZONE C: RUNTIME KEYWORDS MRO ROUTING PASS & REDRAW PROPS
        # -----------------------------------------------------------------
        if kwargs:
            result = super().configure(**kwargs)
            self._hide_internal_scrollbars()
            return result
        return None

    def get_state(self):
        """Explicit getter synchronized with your standalone test harness script assertions."""
        return self.state()

    def state(self, mode: str = None):
        """Dedicated container frame state controller."""
        if mode is None:
            return getattr(self, "_custom_current_state", "normal")

        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            self._update_current_visual_state()
            self._custom_current_state = "normal"

        elif mode == "disabled":
            # Safely step in and apply custom disabled color styles manually,
            # keeping the unrecognized "state" key away from CustomTkinter's core frame class.
            for key in ("fg_color", "border_color", "label_text_color"):
                if key in self._custom_disabled_map:
                    try:
                        super().configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"
            self._hide_internal_scrollbars()

    def _update_current_visual_state(self):
        """MASTER VISUAL ROUTER: Restores active theme layouts out of memory."""
        super().configure(
            fg_color=self.final_kw.get("fg_color", self._local_defaults.get("fg_color")),
            border_color=self.final_kw.get("border_color", self._local_defaults.get("border_color")),
            label_text_color=self.final_kw.get("label_text_color", self._local_defaults.get("label_text_color"))
        )
        self._hide_internal_scrollbars()

    def _hide_internal_scrollbars(self):
        """Forces the scrollbar track elements to match the frame background color seamlessly."""
        try:
            bg_color = super().cget("fg_color")
            if hasattr(self, "_scrollbar") and self._scrollbar is not None:
                self._scrollbar.configure(
                    fg_color=bg_color,
                    button_color=bg_color,
                    button_hover_color=bg_color,
                    width=0
                )
        except Exception:
            pass

    def winfo_children(self):
        """
        MASTER CHILD INTERCEPTOR:
        Bypasses CustomTkinter's private system structural frames to natively
        extract ONLY your true user-placed child component labels.
        """
        if hasattr(self, "_parent_frame") and self._parent_frame is not None:
            if hasattr(self._parent_frame, "_view_frame") and self._parent_frame._view_frame is not None:
                return self._parent_frame._view_frame.winfo_children()

        if hasattr(self, "_view_frame") and self._view_frame is not None:
            return self._view_frame.winfo_children()

        return super().winfo_children()

    def get_children(self):
        """Explicit companion getter shortcut pointing natively to winfo_children."""
        return self.winfo_children()

    def get_container(self):
        return self


# !/usr/bin/python3
"""
sCTkFrameLabeledSecondary - Standalone Interactive Testing Harness
"""
import customtkinter as ctk
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
