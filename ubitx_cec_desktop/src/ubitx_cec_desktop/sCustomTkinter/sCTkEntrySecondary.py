#!/usr/bin/python3
"""
sCTkEntrySecondary - Piece 1 of 2

Subclass of CTkEntry via Pygubu UI Class Isolation (Secondary Form Input Field)
Fortified with inner native sub-widget color forcing to fix text dimming bugs.

UI source file: sCTkEntrySecondary.ui
"""
import customtkinter as ctk
import sCTkEntrySecondaryui as baseui
from ThemeableWidget import ThemeableWidget

class sCTkEntrySecondary(baseui.sCTkEntrySecondaryUI, ThemeableWidget):
    def __init__(self, master=None, **kw):
        # 1. PARAMETER POPPING: Capture text field attributes early
        textvariable = kw.pop("textvariable", None)
        placeholder_text = kw.pop("placeholder_text", None)

        # 2. Fire our shared theme logic first to resolve global configurations natively
        ThemeableWidget.__init__(self, kw)

        # 3. 🛠️ THE MUTATION SAFEGUARD DEEP COPY:
        self._local_defaults = dict(self.final_kw)
        self._custom_disabled_map = dict(self._widget_disabled_map)

        # 4. Initialize CustomTkinter natively with the clean final kwargs array safely
        super().__init__(master, **self.final_kw)

        # 5. Build your inner custom properties using your popped parameters safely
        if textvariable:
            super().configure(textvariable=textvariable)
        if placeholder_text:
            super().configure(placeholder_text=placeholder_text)

        self._custom_current_state = "normal"

    def configure(self, *args, **kwargs):
        """Handles Pygubu designer queries and manages composite state updates safely."""
        if args and len(args) == 1:
            pname = args if isinstance(args, (list, tuple)) else args
            if pname == "state":
                return ("state", "state", "state", "normal", str(self.state()))

            if pname in ["fg_color", "border_color", "text_color", "placeholder_text_color"]:
                current_state = str(self.state()).lower()
                val = self._custom_disabled_map.get(pname) if current_state == "disabled" else self._local_defaults.get(pname)
                return (pname, pname, pname, str(self._local_defaults.get(pname)), str(val))

            return super().configure(*args, **kwargs)

        if args and isinstance(args, dict):
            kwargs = args | kwargs

        # Payload Routing
        if "textvariable" in kwargs:
            super().configure(textvariable=kwargs.pop("textvariable"))
        if "placeholder_text" in kwargs:
            super().configure(placeholder_text=kwargs.pop("placeholder_text"))

        if "state" in kwargs:
            target_state = kwargs.pop("state")
            self.state(target_state)

        # Clean empty strings passed by backspacing parameters in Pygubu to prevent exceptions
        for k, v in list(kwargs.items()):
            if v == "":
                kwargs.pop(k)

        if kwargs:
            return super().configure(**kwargs)
        return None

    def cget(self, attribute_name: str) -> any:
        """Safely intercept custom properties like 'state' from throwing errors."""
        if str(attribute_name).lower() == "state":
            return self.state()
        return super().cget(attribute_name)

    def get_state(self):
        """Explicit getter synchronized with your standalone test harness script assertions."""
        return self.state()

    def state(self, mode: str = None):
        """Dedicated text entry operational availability state controller with sub-widget color forcing."""
        if mode is None:
            return str(getattr(self, "_custom_current_state", "normal")).lower()

        mode = mode.lower()
        if mode in ("normal", "enabled", "active"):
            self._custom_current_state = "normal"

            # 1. Restore native active interaction pass
            if hasattr(self, "_entry") and self._entry:
                self._entry.configure(state="normal")

            super().configure(state="normal")
            self._update_current_visual_state()

        elif mode == "disabled":
            self._custom_current_state = "disabled"

            # 2. 🔑 THE SUB-WIDGET INTERCEPT SHIELD:
            # Drop straight below CustomTkinter's abstraction layer to activate the underlying C-core entry
            # in "readonly" mode, locking typing actions completely while keeping color updates wide open!
            if hasattr(self, "_entry") and self._entry:
                self._entry.configure(state="readonly")

            # 3. 🔑 FORCE INNER CANVAS TEXT COLOR PROPAGATION:
            disabled_txt = self._custom_disabled_map.get("text_color", ("#94A3B8", "#4B5563"))
            disabled_fg = self._custom_disabled_map.get("fg_color", ("#F9FAFB", "#1A1A1A"))
            disabled_border = self._custom_disabled_map.get("border_color", ("#E5E7EB", "#222222"))

            resolved_txt = self._resolve_color(disabled_txt)
            resolved_fg = self._resolve_color(disabled_fg)
            resolved_border = self._resolve_color(disabled_border)

            super().configure(
                fg_color=resolved_fg,
                border_color=resolved_border,
                text_color=resolved_txt
            )

            # Force the underlying C-entry core instance to actively repaint its font string cells
            if hasattr(self, "_entry") and self._entry:
                self._entry.configure(
                    fg=resolved_fg,
                    bg=resolved_fg,
                    readonlybackground=resolved_fg,
                    selectbackground=resolved_fg,
                    insertbackground=resolved_txt,
                    foreground=resolved_txt
                )

        return self._custom_current_state

    def _update_current_visual_state(self):
        """MASTER VISUAL ROUTER: Dynamically applies extensible theme properties out of protected memory."""
        config_payload = {}
        for key in ("fg_color", "border_color", "text_color", "placeholder_text_color", "border_width", "font"):
            val = self._local_defaults.get(key)
            if val is not None:
                config_payload[key] = self._resolve_color(val) if "color" in key else val

        if config_payload:
            super().configure(**config_payload)

            # Re-sync active text properties to the inner entry field core natively
            resolved_text_clr = config_payload.get("text_color")
            resolved_fg_clr = config_payload.get("fg_color")
            if resolved_text_clr and hasattr(self, "_entry") and self._entry:
                self._entry.configure(foreground=resolved_text_clr, fg=resolved_text_clr)
            if resolved_fg_clr and hasattr(self, "_entry") and self._entry:
                self._entry.configure(bg=resolved_fg_clr)


# =====================================================================
# 🛠️ TESTING HARNESS IMPORTS & SETUP
# =====================================================================
import sCTkThemes
from sCTkFrame import sCTkFrame
from sCTkLabelSecondary import sCTkLabelSecondary

if __name__ == "__main__":
    sCTkThemes.apply_sCTkThemes()

    root = ctk.CTk()
    root.geometry("450x260")
    root.title("sCTkEntrySecondary Testing Deck")

    base = sCTkFrame(root)
    base.pack(expand=True, fill="both", padx=20, pady=20)

    lbl_monitor = sCTkLabelSecondary(base, text="Console secondary monitor active...")
    lbl_monitor.pack(pady=10)

    input_field = sCTkEntrySecondary(base, placeholder_text="Secondary Data Field Input...")
    input_field.pack(expand=False, fill="x", padx=40, pady=10)

    # Pre-populate dummy text to instantly verify character dimming mechanics
    input_field.insert(0, "Sub-Receiver Delta Offset")

    input_field.bind("<KeyRelease>", lambda e: lbl_monitor.configure(text=f"Live Buffer: {input_field.get()}"))


    def toggle_operational_state():
        """Toggles the input lane between normal active and dimmed disabled profiles."""
        current_mode = input_field.get_state()
        target = "disabled" if current_mode == "normal" else "normal"

        input_field.configure(state=target)
        btn_toggle.configure(
            text="Lock Input (Set 'disabled')" if target == "normal" else "Unlock Input (Set 'normal')")
        print(f"Logged Verification Hook -> input_field.get_state() = {input_field.get_state()}")


    btn_toggle = ctk.CTkButton(base, text="Lock Input (Set 'disabled')", command=toggle_operational_state)
    btn_toggle.pack(side="bottom", pady=15)

    print("--- BOOT INITIALIZATION PASSTHROUGH ---")
    input_field.state("disabled")
    print("state (Disabled Pass) =", input_field.get_state())  # Output: disabled
    input_field.state("normal")
    print("state (Normal Pass)   =", input_field.get_state())  # Output: normal
    print("========================================\n")

    root.mainloop()
