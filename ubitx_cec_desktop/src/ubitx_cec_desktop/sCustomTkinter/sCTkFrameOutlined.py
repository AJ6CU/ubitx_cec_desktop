#!/usr/bin/python3
"""
sCTkFrameOutlined

A clean, theme-compliant outlined CustomTkinter container frame.
Acts as a passive layout group following native Tkinter patterns.
"""
import customtkinter as ctk
from ThemeableWidget import ThemeableWidget


class sCTkFrameOutlined(ctk.CTkFrame, ThemeableWidget):
    properties = frozenset()

    def __init__(self, master=None, **kwargs):
        # 1. Fire our shared theme logic first. It automatically finds "sCTkFrameOutlined" inside themes.json
        ThemeableWidget.__init__(self, kwargs)

        # 2. Store your custom maps safely onto instance memory channels
        self._local_defaults = self.final_kw
        self._custom_disabled_map = self._widget_disabled_map

        # 3. Initialize CustomTkinter CTkFrame natively with final clean kwargs safely
        super().__init__(master, **self.final_kw)

        self._custom_current_state = "normal"

    def configure(self, *args, **kwargs):
        """Handles Pygubu designer queries and manages container configurations safely."""

        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Pygubu Inspector compatibility check)
        # -----------------------------------------------------------------
        if args and len(args) == 1:
            pname = args
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "border_color"]:
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
        # ZONE C: RUNTIME KEYWORDS MRO ROUTING PASS
        # -----------------------------------------------------------------
        if kwargs:
            return super().configure(**kwargs)
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
            # 🛠️ THE ABSORPTION GUARD:
            # We bypass calling super().configure(state="disabled") because plain frames
            # don't support an execution state parameter. Instead, we safely strip the
            # key and apply our custom faded gray outline styling rules directly.
            for key in ("fg_color", "border_color"):
                if key in self._custom_disabled_map:
                    try:
                        super().configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"

    def _update_current_visual_state(self):
        """MASTER VISUAL ROUTER: Restores active theme layouts out of memory."""
        super().configure(
            fg_color=self.final_kw.get("fg_color", self._local_defaults.get("fg_color")),
            border_color=self.final_kw.get("border_color", self._local_defaults.get("border_color"))
        )



import customtkinter as ctk
# from sCTkFrameOutlined import sCTkFrameOutlined
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkEntryPrimary import sCTkEntryPrimary


def toggle_frame_states():
    """Toggles the outlined card panel and cascades the state change down to child widgets, skipping the trigger."""
    current_mode = frame_group.get_state()
    target = "disabled" if current_mode == "normal" else "normal"

    # 1. Transition the parent outline panel colors
    frame_group.configure(state=target)

    # 2. Cascade loop targeting elements resting inside the border frame card
    for child in frame_group.winfo_children():
        # 🛠️ THE BUTTON SKIP FIX:
        # If the loop hits the toggle button widget, skip it!
        # This keeps the button completely functional so you can unlock the panel.
        if child == btn_toggle:
            continue

        if hasattr(child, "configure"):
            child.configure(state=target)

    btn_toggle.configure(
        text="Lock Outline Deck (Set 'disabled')" if target == "normal" else "Unlock Outline Deck (Set 'normal')")
    print(f"Logged Verification Hook -> frame_group.get_state() = {frame_group.get_state()}")


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Passive Outline Frame Test Suite")
    root.geometry("450x300")

    # Instantiate your custom theme-compliant outlined frame panel card
    frame_group = sCTkFrameOutlined(root, border_width=2)
    frame_group.pack(fill="both", expand=True, padx=20, pady=20)

    lbl_title = sCTkLabelSecondary(frame_group, text="TRANSCEIVER FREQUENCY PRESET PROFILE")
    lbl_title.pack(pady=(12, 4), padx=10, fill="x")

    mock_entry = sCTkEntryPrimary(frame_group, placeholder_text="Standard data field...")
    mock_entry.pack(pady=10, padx=25, fill="x")

    btn_toggle = ctk.CTkButton(frame_group, text="Lock Outline Deck (Set 'disabled')", command=toggle_frame_states)
    btn_toggle.pack(side="bottom", pady=15)

    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    print(f"Initial Outline Frame State = {frame_group.get_state().upper()}")
    print("========================================\n")

    root.mainloop()