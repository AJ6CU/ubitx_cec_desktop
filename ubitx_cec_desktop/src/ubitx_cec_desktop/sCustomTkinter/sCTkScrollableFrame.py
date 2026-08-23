#!/usr/bin/python3
"""
sCTkScrollableFrame - Piece 1 of 2

A clean, theme-compliant scrollable viewport container frame.
Natively intercepts hidden canvas window tags on macOS to support touch gestures [INDEX],
and overrides winfo_children() to report application widgets cleanly [INDEX].
"""
import sys
import platform
import customtkinter as ctk
from ThemeableWidget import ThemeableWidget
import sCTkScrollableFrameui as baseui

class sCTkScrollableFrame(baseui.sCTkScrollableFrameUI, ThemeableWidget):
    properties = frozenset()

    def __init__(self, master=None, **kwargs):
        # 1. INITIAL RUNTIME SCRUB: Safely shield native frame from state checks
        state_init = kwargs.pop("state", "normal")

        # 2. ENFORCE SYSTEM REGISTRY INTERACTION
        ThemeableWidget.__init__(self, kwargs)

        # 3. 🛠️ THE MUTATION SAFEGUARD DEEP COPY SHIELD:
        self._local_defaults = dict(self.final_kw)
        self._custom_disabled_map = dict(self._widget_disabled_map)

        # Remove custom parameters from final_kw to prevent parent collisions
        self.final_kw.pop("state", None)

        # 4. INITIALIZE NATIVE BASE LAYER
        super().__init__(master, **self.final_kw)

        self._state_str = "normal"
        self.configure(state=state_init)

    def configure(self, *args, **kwargs):
        """Processes Pygubu designer queries and manages state changes safely [INDEX]."""
        if args and len(args) == 1:
            pname = args if isinstance(args, (list, tuple)) else args
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "label_fg_color", "scrollbar_button_color"]:
                current_state = str(self.state()).lower()
                val = self._custom_disabled_map.get(pname) if current_state == "disabled" else self._local_defaults.get(pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            return super().configure(*args, **kwargs)

        if args and isinstance(args, dict):
            kwargs = args | kwargs

        if "state" in kwargs:
            self.state(kwargs.pop("state"))

        if kwargs:
            super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        """Safely intercept custom properties like 'state' from throwing errors [INDEX]."""
        if str(attribute_name).lower() == "state":
            return self.state()
        return super().cget(attribute_name)

    def get_state(self) -> str:
        """Explicit getter synchronized with your other sCTk widgets [INDEX]."""
        return self.state()

    def state(self, mode: str = None) -> str:
        """Dedicated polymorphic state manager syncing scroll mechanics and viewport surfaces [INDEX]."""
        if mode is None:
            return str(getattr(self, "_state_str", "normal")).lower()

        target_state = mode.lower()
        self._state_str = target_state

        if target_state == "disabled":
            target_fg = self._custom_disabled_map.get("fg_color", self._local_defaults.get("fg_color"))
            target_border = self._custom_disabled_map.get("border_color", self._local_defaults.get("border_color"))

            super().configure(
                fg_color=target_fg,
                border_color=target_border,
                label_fg_color=self._custom_disabled_map.get("label_fg_color", self._local_defaults.get("label_fg_color"))
            )

            if hasattr(self, "_scrollbar") and self._scrollbar:
                self._scrollbar.configure(
                    button_color=self._custom_disabled_map.get("scrollbar_button_color"),
                    button_hover_color=self._custom_disabled_map.get("scrollbar_button_color")
                )
            self._toggle_scroll_bindings(bind=False)

        elif target_state in ["normal", "active", "enabled"]:
            super().configure(
                fg_color=self._local_defaults.get("fg_color"),
                border_color=self._local_defaults.get("border_color"),
                label_fg_color=self._local_defaults.get("label_fg_color")
            )

            if hasattr(self, "_scrollbar") and self._scrollbar:
                self._scrollbar.configure(
                    button_color=self._local_defaults.get("scrollbar_button_color"),
                    button_hover_color=self._local_defaults.get("scrollbar_button_hover_color")
                )
            self._toggle_scroll_bindings(bind=True)
        return self._state_str

    def _decode_mac_touchpad_delta(self, raw_delta):
        """🛠️ DIAL-VERIFIED PHYSICS MASK: Decodes macOS touchpad bitmasks [INDEX]."""
        raw = raw_delta & 0xFFFFFFFF
        delta_x = (raw >> 16) & 0xFFFF
        if delta_x >= 0x8000: delta_x -= 0x10000
        delta_y = raw & 0xFFFF
        if delta_y >= 0x8000: delta_y -= 0x10000
        return delta_x, delta_y

    def winfo_children(self, include_private: bool = False) -> list:
        """
        🛠️ THE STRUCTURE INTERCEPTOR OVERRIDE (WITH SAFETY HATCH):
        By default, filters CustomTkinter's private background sub-elements out [INDEX].
        Pass `include_private=True` to immediately return the raw, unmanipulated
        Tkinter core window lineage tree [INDEX]!
        """
        raw_children = super().winfo_children()
        if include_private:
            return raw_children

        filtered_children = []
        for child in raw_children:
            # Drop private internal wrapper artifacts from appearing in clean application loops
            if child.__class__.__name__ not in ["CTkScrollbar", "CTkCanvas", "Canvas"]:
                filtered_children.append(child)
        return filtered_children

    def get_children(self) -> list:
        """Convenience function providing a clean, application-level layout array [INDEX]."""
        return self.winfo_children(include_private=False)

    def get_all_children(self) -> list:
        """Convenience function providing direct, unfiltered access to the entire C-level native tree."""
        return self.winfo_children(include_private=True)

    def _toggle_scroll_bindings(self, bind=True):
        """The parent canvas intercept engine routing mouse wheels and touchpad events [INDEX]."""
        SCROLL_EVENTS = ["<MouseWheel>", "<TouchpadScroll>", "<Button-4>", "<Button-5>"]
        layers_to_bind = [self]
        try:
            parent_path = self.winfo_parent()
            parent_widget = self.nametowidget(parent_path)
            if parent_widget and parent_widget.__class__.__name__ == "Canvas":
                layers_to_bind.append(parent_widget)
                grandparent_path = parent_widget.winfo_parent()
                grandparent_widget = self.nametowidget(grandparent_path)
                if grandparent_widget: layers_to_bind.append(grandparent_widget)
        except Exception:
            pass

        for child in self.get_children():
            if child not in layers_to_bind: layers_to_bind.append(child)

        for target_layer in layers_to_bind:
            for event_str in SCROLL_EVENTS:
                try:
                    target_layer.unbind(event_str)
                except Exception:
                    pass

                if bind and self._state_str == "normal":
                    if "Touchpad" in event_str:
                        if sys.platform == "darwin":
                            target_layer.bind("<TouchpadScroll>", self._process_mac_touchpad_scroll, add="+")
                    else:
                        target_layer.bind(event_str, self._process_scroll_wheel, add="+")

    def _process_mac_touchpad_scroll(self, event):
        """Processes Apple high-precision touch masks on the true master canvas [INDEX]."""
        try:
            parent_widget = self.nametowidget(self.winfo_parent())
            if parent_widget and hasattr(parent_widget, "yview_scroll"):
                delta_x, delta_y = self._decode_mac_touchpad_delta(event.delta)
                if delta_y != 0:
                    MAC_SCROLL_SENSITIVITY = 3
                    scaled_scroll = -MAC_SCROLL_SENSITIVITY if delta_y > 0 else MAC_SCROLL_SENSITIVITY
                    parent_widget.yview_scroll(scaled_scroll, "units")
        except Exception:
            pass

    def _process_scroll_wheel(self, event):
        """Processes cross-platform standard mouse wheels and physical tuning knobs [INDEX]."""
        try:
            parent_widget = self.nametowidget(self.winfo_parent())
            if parent_widget and hasattr(parent_widget, "yview_scroll"):
                sys_platform = platform.system()
                if sys_platform == "Darwin":
                    delta = event.delta
                    MAC_SCROLL_SENSITIVITY = 3
                    scaled_scroll = int(-MAC_SCROLL_SENSITIVITY * delta) if abs(delta) >= 1 else (
                        -MAC_SCROLL_SENSITIVITY if delta > 0 else MAC_SCROLL_SENSITIVITY)
                    parent_widget.yview_scroll(scaled_scroll, "units")
                elif sys_platform == "Linux":
                    if event.num == 4:
                        parent_widget.yview_scroll(-1, "units")
                    elif event.num == 5:
                        parent_widget.yview_scroll(1, "units")
                else:
                    parent_widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    def _finalize_split_bindings(self):
        """Standard layout binding connection pass [INDEX]."""
        self._toggle_scroll_bindings(bind=True)

# =================================================================
# STANDALONE TEST HARNESS
# =================================================================
if __name__ == "__main__":
    import sCTkThemes
    from sCTkButtonPrimary import sCTkButtonPrimary
    from sCTkEntryPrimary import sCTkEntryPrimary

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

