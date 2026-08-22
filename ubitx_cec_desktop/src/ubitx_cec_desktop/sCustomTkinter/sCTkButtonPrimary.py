#!/usr/bin/python3
"""
sCTkButtonPrimary

subclass of CTkButton

UI source file: sCTkButtonPrimary.ui
"""
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter as ctk
import sCTkButtonPrimaryui as baseui
from ThemeableWidget import ThemeableWidget


class sCTkButtonPrimary(baseui.sCTkButtonPrimaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # 1. Run the shared theme logic to load defaults out of themes.json
        ThemeableWidget.__init__(self, kw)

        # Store dictionary references safely onto instance memory
        self._local_defaults = self.final_kw
        self._custom_disabled_map = self._widget_disabled_map
        self._custom_pressed_map = self._widget_pressed_map
        self._custom_alarm_map = self._widget_alarm_map

        # Initialize CustomTkinter with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

        self.is_pressed = False
        self.is_alarm = False

    def configure(self, *args, **kwargs):
        """Handles Pygubu designer queries and manages composite state updates safely."""

        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Pygubu Inspector compatibility check)
        # -----------------------------------------------------------------
        if args and len(args) == 1:
            pname = args[0]
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "border_color", "text_color", "hover_color"]:
                current_state = str(self.state()).lower()
                if current_state == "disabled" and self._custom_disabled_map:
                    val = self._custom_disabled_map.get(pname)
                elif getattr(self, "is_alarm", False) and self._custom_alarm_map:
                    val = self._custom_alarm_map.get(pname)
                elif getattr(self, "is_pressed", False) and self._custom_pressed_map:
                    val = self._custom_pressed_map.get(pname)
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
            # Re-bind core canvas event loops cleanly when coming back to active status using native framework tags
            try:
                self._canvas.bind("<Enter>", self._on_enter)
                self._canvas.bind("<Leave>", self._on_leave)
                self._canvas.bind("<Button-1>", self._on_clicked)
                self._canvas.bind("<ButtonRelease>", self._on_clicked)
            except Exception:
                pass

            # 🛠️ THE TEMPLATE FIX: Use super().configure to bypass Pygubu loops
            super().configure(state="normal", hover=True)
            self._update_current_visual_state()
            self._custom_current_state = "normal"

        elif mode == "disabled":
            # FIX: Explicitly unbind cursor listeners with clean cross-platform identifiers to permanently absorb hovering glitches
            try:
                self._canvas.unbind("<Enter>")
                self._canvas.unbind("<Leave>")
                self._canvas.unbind("<Button-1>")
                self._canvas.unbind("<ButtonRelease>")
            except Exception:
                pass

            # 🛠️ THE TEMPLATE FIX: Use super().configure to bypass Pygubu loops
            super().configure(state="disabled", hover=False)

            # Apply custom flat muted gray states safely via super
            for key in ("fg_color", "hover_color", "text_color"):
                if key in self._custom_disabled_map:
                    try:
                        super().configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass

            self._custom_current_state = "disabled"

    def set_pressed(self, pressed: bool):
        """Toggles the visual pressed state of the button cleanly."""
        if getattr(self, "_custom_current_state", "normal") == "disabled" or self.is_alarm:
            return

        self.is_pressed = pressed
        self._update_current_visual_state()

    def set_alarm_state(self, active: bool):
        """Forces the button into a high-visibility warning red state cleanly."""
        if getattr(self, "_custom_current_state", "normal") == "disabled":
            return

        self.is_alarm = active
        if self.is_alarm:
            self.is_pressed = False

        self._update_current_visual_state()

    def _update_current_visual_state(self):
        """
        MASTER VISUAL ROUTER: Dynamically maps configuration layouts out of memory.
        """
        # A. ALARM STATE TAKES IMMEDIATE PRIORITY
        if self.is_alarm:
            # 🛠️ THE TEMPLATE FIX: Use super().configure to safely hand off to CustomTkinter core
            super().configure(
                fg_color=self._custom_alarm_map.get("fg_color"),
                hover_color=self._custom_alarm_map.get("hover_color"),
                text_color=self._custom_alarm_map.get("text_color"),
                hover=False
            )
        # B. PRESSED STATE TAKES SECONDARY PRIORITY
        elif self.is_pressed:
            # 🛠️ THE TEMPLATE FIX: Use super().configure to safely hand off to CustomTkinter core
            super().configure(
                fg_color=self._custom_pressed_map.get("fg_color"),
                hover_color=self._custom_pressed_map.get("hover_color"),
                text_color=self._custom_pressed_map.get("text_color"),
                hover=False
            )
        # C. FALLBACK TO NORMAL THEME
        else:
            # 🛠️ THE TEMPLATE FIX: Use super().configure to safely hand off to CustomTkinter core
            super().configure(
                fg_color=self.final_kw.get("fg_color", self._local_defaults.get("fg_color")),
                hover_color=self.final_kw.get("hover_color", self._local_defaults.get("hover_color")),
                text_color=self.final_kw.get("text_color", self._local_defaults.get("text_color")),
                hover=True
            )


# =====================================================================
# 3. INTERACTIVE RUNTIME APP EXECUTION & TEST SEQUENCES
# =====================================================================
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("450x200")
    root.title("Primary Button Test Harness")
    from sCTkFrame import sCTkFrame

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    # Instantiate two primary actions
    widget = sCTkButtonPrimary(base, text="System Alarm Button")
    widget1 = sCTkButtonPrimary(base, text="Latching Preset Toggle")

    widget.pack(padx=40, pady=15)
    widget1.pack(padx=40, pady=15)

    # -----------------------------------------------------------------
    # A. INITIAL CONSOLE LOG TEST SEQUENCE
    # -----------------------------------------------------------------
    print("--- BOOT TEST: FORCING DISABLED PASS ---")
    widget.state("disabled")
    widget1.state("disabled")
    print("Widget 0 state =", widget.get_state())
    print("Widget 1 state =", widget1.get_state())

    print("\n--- BOOT TEST: REVERTING TO NORMAL PASS ---")
    widget.state("normal")
    widget1.state("normal")
    print("Widget 0 state =", widget.get_state())
    print("Widget 1 state =", widget1.get_state())
    print("\n=== SYSTEM ONLINE: BUTTON INTERACTION ACTIVE ===\n")

    # -----------------------------------------------------------------
    # B. 🛠️ THE INTERACTION FIX: MAKE BUTTONS ALIVE AND RESPOND TO CLICKS
    # -----------------------------------------------------------------
    # 🛠️ THE ALARM TOGGLE FIX: Change the command loop sequence to flip the alarm flag!
    widget.configure(
        command=lambda: [print("System Alarm Toggle Triggered"), widget.set_alarm_state(not widget.is_alarm)])

    # Clicking 'widget1' remains assigned to your standard layout latch toggle
    widget1.configure(command=lambda: [print("Latching Preset Clicked"), widget1.set_pressed(not widget1.is_pressed)])

    root.mainloop()
