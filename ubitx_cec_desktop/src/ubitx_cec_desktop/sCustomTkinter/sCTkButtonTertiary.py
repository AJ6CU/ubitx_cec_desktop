
#!/usr/bin/python3
"""
sCTkButtonTertiary

subclass of CTkButton (Universal Platform Border-Driven Outline Latching Toggle Variant)

UI source file: sCTkButtonTertiary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import platform
import customtkinter as ctk
import sCTkButtonTertiaryui as baseui
from ThemeableWidget import ThemeableWidget

#
# Manual user code
#
#
#   Need to fix "text_color": ctk.ThemeManager.theme["CTkButton"]["fg_color"],
#  defaultng to "text_color": ["#3B8ED0", "#1F6AA5"],
#

class sCTkButtonTertiary(baseui.sCTkButtonTertiaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):

        # theme_defaults = THEME_DEFAULTS["sCTkButtonTertiary"]
        # 1. Run the shared theme logic to load defaults out of themes.json
        ThemeableWidget.__init__(self, kw)

        # 2. 🛠️ THE DYNAMIC OVERRIDE: Fetch the live theme color from CustomTkinter memory
        # and assign it straight into your final parameters array.
        try:
            live_fg_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
            # Cast it to a tuple so CustomTkinter processes it correctly
            self.final_kw["text_color"] = tuple(live_fg_color)
        except Exception:
            # Safe hardcoded fallback if CustomTkinter's theme engine fails to read
            self.final_kw["text_color"] = ("#3B8ED0", "#1F6AA5")

        # Store dictionary references safely onto instance memory
        self._local_defaults = self.final_kw
        self._custom_disabled_map = self._widget_disabled_map
        self._custom_pressed_map = self._widget_pressed_map

        # Initialize CustomTkinter with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

        self.is_pressed = False

    def configure(self, *args, **kwargs):
        """Handles Pygubu designer queries and manages state updates safely."""

        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Pygubu Inspector compatibility check)
        # -----------------------------------------------------------------
        if args and len(args) == 1:
            pname = args[0]
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "border_color", "text_color"]:
                current_state = str(self.state()).lower()
                if current_state == "disabled" and self._custom_disabled_map:
                    val = self._custom_disabled_map.get(pname)
                else:
                    val = self._local_defaults.get(pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            # Avoid forwarding unnecessary **kwargs dictionary buffers down to super
            return super().configure(pname)

        # -----------------------------------------------------------------
        # ZONE B: SUB-COMPONENT PAYLOAD ROUTING / STATE INTERCEPTION
        # -----------------------------------------------------------------
        if "state" in kwargs:
            target_state = kwargs.pop("state")
            self.state(target_state)

        # Pass any remaining properties down through your verified ThemeableWidget configuration track
        if hasattr(super(), "configure"):
            return super().configure(**kwargs)
        return None


    def get_state(self):
        """Explicit getter synchronized with your standalone test harness script assertions."""
        return self.state()

    def state(self, mode: str = None):
        """Dedicated button state controller."""
        if mode is None:
            return str(super().cget("state")).lower()
        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            try:
                self._canvas.bind("<Enter>", self._on_enter)
                self._canvas.bind("<Leave>", self._on_leave)
                self._canvas.bind("<Button-1>", self._on_clicked)
                self._canvas.bind("<ButtonRelease>", self._on_clicked)
            except Exception:
                pass

            # 🛠️ THE FIXED TRACK: Use super().configure to bypass Pygubu loops
            super().configure(state="normal", hover=True)
            self._update_current_visual_state()
            self._custom_current_state = "normal"

        elif mode == "disabled":
            try:
                self._canvas.unbind("<Enter>")
                self._canvas.unbind("<Leave>")
                self._canvas.unbind("<Button-1>")
                self._canvas.unbind("<ButtonRelease>")
            except Exception:
                pass

            # 🛠️ THE FIXED TRACK: Use super().configure to bypass Pygubu loops
            super().configure(state="disabled", hover=False)

            # Apply disabled overrides from your map safely
            for key in ("fg_color", "border_color", "hover_color", "text_color"):
                if key in self._custom_disabled_map:
                    try:
                        super().configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"

    def _update_current_visual_state(self):
        """
        MASTER VISUAL ROUTER: Dynamically maps configuration layouts out of memory.
        """
        if getattr(self, "is_pressed", False):
            # 🛠️ THE FIXED TRACK: Safe direct CustomTkinter call
            super().configure(
                fg_color=self._custom_pressed_map.get("fg_color"),
                border_color=self._custom_pressed_map.get("border_color"),
                hover_color=self._custom_pressed_map.get("hover_color", self._local_defaults.get("hover_color")),
                text_color=self._custom_pressed_map.get("text_color"),
                hover=False
            )
        else:
            # 🛠️ THE FIXED TRACK: Safe direct CustomTkinter call
            super().configure(
                fg_color=self.final_kw.get("fg_color", self._local_defaults.get("fg_color")),
                border_color=self.final_kw.get("border_color", self._local_defaults.get("border_color")),
                hover_color=self.final_kw.get("hover_color", self._local_defaults.get("hover_color")),
                text_color=self.final_kw.get("text_color", self._local_defaults.get("text_color")),
                hover=True
            )

    def set_pressed(self, pressed: bool):
        """Toggles the visual pressed state of the tertiary button cleanly."""
        if getattr(self, "_custom_current_state", "normal") == "disabled":
            return

        self.is_pressed = pressed
        self._update_current_visual_state()


if __name__ == "__main__":
    # # ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("400x200")

    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    widget1 = sCTkButtonTertiary(base)
    widget = sCTkButtonTertiary(base)

    # -----------------------------------------------------------------
    # 🛠️ THE CLICK REPORT & TOGGLE FIX (Moved cleanly to the Test Harness)
    # -----------------------------------------------------------------
    widget1.configure(
        text="Latching Preset Toggle",
        command=lambda: [
            widget1.set_pressed(not widget1.is_pressed),
            print("Latching Preset Toggle=", widget1.is_pressed)
        ]
    )

    widget.configure(
        text="System Action",
        command=lambda: [
            print("System Action Clicked")
        ]
    )

    widget.pack(expand=False, fill="none", padx=40, pady=15)
    widget1.pack(expand=False, fill="none", padx=40, pady=15)

    # -----------------------------------------------------------------
    # A. INITIAL BOOT LOG TEST SEQUENCE (Kept Exactly As Is)
    # -----------------------------------------------------------------
    # Verify our custom cascading state system locks down the entire panel hierarchy instantly!
    widget.state("disabled")
    print("--- DISABLED PASS ---")
    print("Widget 0 state =", widget.get_state())
    print("Widget 1 state =", widget1.get_state())

    # Verify the cascade pipeline unlocks everything smoothly right back to normal
    widget.state("normal")
    print("\n--- NORMAL PASS ---")
    print("Widget 0 state =", widget.get_state())
    print("Widget 1 state =", widget1.get_state())
    print("\n=== SYSTEM ONLINE: TERTIARY BUTTON INTERACTION ACTIVE ===\n")

    root.mainloop()





