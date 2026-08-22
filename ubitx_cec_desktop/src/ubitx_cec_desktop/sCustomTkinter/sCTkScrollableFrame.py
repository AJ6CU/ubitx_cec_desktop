#!/usr/bin/python3
"""
sCTkScrollableFrame

A clean, theme-compliant scrollable viewport container frame.
"""
import customtkinter as ctk
from ThemeableWidget import ThemeableWidget

import sCTkScrollableFrameui as baseui


class sCTkScrollableFrame(baseui.sCTkScrollableFrameUI, ThemeableWidget):
    properties = frozenset()

    def __init__(self, master=None, **kwargs):
        theme_defaults = THEME_DEFAULTS.get("sCTkScrollableFrame", {})

        # 1. INITIAL RUNTIME SCRUB: Safely shield native frame from state validation checks
        state_init = kwargs.pop("state", "normal")

        # 2 & 3. RESOLVE THEMES & CACHE LOCAL SCOPE BEFORE INITIALIZERS
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # 4. INITIALIZE THEME ENGINE: Merges dictionary parameters safely
        ThemeableWidget.__init__(self, theme_defaults, kwargs)

        # 5. LEAN PURGE: Remove custom parameters from self.final_kw just in case
        # they were pulled out of the THEME_DEFAULTS config dictionary
        self.final_kw.pop("state", None)

        # 6. INITIALIZE NATIVE BASE LAYER
        super().__init__(master, **self.final_kw)

        # 7. ROUTE TO CONFIG: Safely pass parameters through your validation engine
        self.configure(state=state_init)

    def configure(self, *args, **kwargs):
        """Processes Pygubu designer queries and manages state changes safely."""
        # ZONE A: POSITION INTERCEPT (Pygubu Inspector compatibility)
        if args and len(args) == 1:
            pname = args
            if pname == "state":
                return ("state", "state", "state", "normal", str(getattr(self, "_state_str", "normal")))

            if pname in ["fg_color", "label_fg_color", "scrollbar_button_color"]:
                current_state = str(getattr(self, "_state_str", "normal")).lower()
                if current_state == "disabled" and self._custom_disabled_map:
                    val = self._custom_disabled_map.get(pname)
                else:
                    val = self._local_defaults.get(pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            return super().configure(*args, **kwargs)

        # ZONE C: STATE CONTROLLER (Locks mouse bindings to freeze ONLY the scrollbar safely)
        if "state" in kwargs:
            target_state = str(kwargs.pop("state")).lower()
            self._state_str = target_state

            if target_state == "disabled" and self._custom_disabled_map:
                # Force custom high-contrast disabled map colors down into scrollable viewport surfaces
                target_fg = self._custom_disabled_map.get("fg_color", self._local_defaults["fg_color"])
                target_border = self._custom_disabled_map.get("border_color", self._local_defaults["border_color"])

                super().configure(
                    fg_color=target_fg,
                    border_color=target_border,
                    label_fg_color=self._custom_disabled_map.get("label_fg_color",
                                                                 self._local_defaults.get("label_fg_color"))
                )

                if hasattr(self, "_scrollbar") and self._scrollbar:
                    # 1. Update visual scrollbar colors via CustomTkinter safely using theme values
                    self._scrollbar.configure(
                        button_color=self._custom_disabled_map["scrollbar_button_color"],
                        button_hover_color=self._custom_disabled_map["scrollbar_button_color"]
                    )

                    # 2. FIXED: Target the inner child canvas where CustomTkinter hooks mouse bindings!
                    if hasattr(self._scrollbar, "_canvas") and self._scrollbar._canvas:
                        self._scrollbar._canvas.unbind("<B1-Motion>")
                        self._scrollbar._canvas.unbind("<Button-1>")

                    # 3. Freeze mouse track wheel mechanics on the viewport surfaces
                    if hasattr(self, "_canvas") and self._canvas:
                        self._canvas.unbind("<MouseWheel>")

            elif target_state in ["normal", "active"]:
                # Revert to clean operational theme configurations directly out of local defaults
                super().configure(
                    fg_color=self._local_defaults["fg_color"],
                    border_color=self._local_defaults["border_color"],
                    label_fg_color=self._local_defaults.get("label_fg_color")
                )

                if hasattr(self, "_scrollbar") and self._scrollbar:
                    # 1. Restore visual colors safely out of local defaults
                    self._scrollbar.configure(
                        button_color=self._local_defaults["scrollbar_button_color"],
                        button_hover_color=self._local_defaults["scrollbar_button_hover_color"]
                    )

                    # 2. FIXED: Reconnect the internal canvas mechanics back to CustomTkinter's private callbacks
                    if hasattr(self._scrollbar, "_canvas") and self._scrollbar._canvas:
                        if hasattr(self._scrollbar, "_scrollbar_action"):
                            self._scrollbar._canvas.bind("<B1-Motion>", self._scrollbar._scrollbar_action)
                            self._scrollbar._canvas.bind("<Button-1>", self._scrollbar._scrollbar_action)

                    # 3. Re-link viewport track wheel mechanics back to native operational handlers
                    if hasattr(self, "_canvas") and self._canvas:
                        self._canvas.bind("<MouseWheel>",
                                          self._on_mousewheel if hasattr(self, "_on_mousewheel") else "")

        # ZONE D: EXECUTE DIRECTLY
        if kwargs:
            super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        """Safely intercept custom properties like 'state' from throwing errors."""
        if str(attribute_name).lower() == "state":
            return getattr(self, "_state_str", "normal")
        return super().cget(attribute_name)

    def get_state(self) -> str:
        """Explicit getter synchronized with your other sCTk widgets."""
        return str(getattr(self, "_state_str", "normal")).lower()



# =================================================================
# STANDALONE TEST HARNESS
# =================================================================
if __name__ == "__main__":
    import customtkinter as ctk
    # Import your button class to handle the toggle operations
    from sCTkButtonPrimary import sCTkButtonPrimary

    root = ctk.CTk()
    root.title("ScrollableFrame State Controller Test")
    root.geometry("450x400")

    # 1. Instantiate your custom themed scroll container
    test_frame = sCTkScrollableFrame(
        root,
        width=380,
        height=250,
        label_text="Telemetry Viewport Container"
    )
    test_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # 2. Pack a few active test entries INSIDE the frame to prove they stay active
    for i in range(12):
        mock_entry = ctk.CTkEntry(test_frame, placeholder_text=f"Active Transceiver Channel {i + 1}")
        mock_entry.pack(padx=10, pady=5, fill="x")


    # 3. State Tracking Variable for the Toggle Callback
    def toggle_container_state():
        current_state = test_frame.cget("state")

        if current_state == "normal":
            # Switch to disabled state
            test_frame.configure(state="disabled")
            toggle_btn.configure(text="Enforce State: NORMAL")
            print("❌ Container State Altered -> DISABLED (Scrollbar Frozen)")
        else:
            # Switch back to normal operational state
            test_frame.configure(state="normal")
            toggle_btn.configure(text="Enforce State: DISABLED")
            print("✅ Container State Altered -> NORMAL (Scrollbar Active)")


    # 4. Add your sCTkButtonPrimary at the bottom window layer
    toggle_btn = sCTkButtonPrimary(
        root,
        text="Enforce State: DISABLED",
        command=toggle_container_state
    )
    toggle_btn.pack(padx=20, pady=(0, 20), fill="x", side="bottom")

    root.mainloop()
