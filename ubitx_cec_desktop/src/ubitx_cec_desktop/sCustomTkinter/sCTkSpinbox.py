import sys
import customtkinter as ctk

# Direct framework path module and theme dictionary registry imports
from sCTkFrame import sCTkFrame
from ThemeableWidget import ThemeableWidget
from sCTkThemes import THEME_DEFAULTS


class sCTkSpinbox(sCTkFrame, ThemeableWidget):
    """
    A theme-adaptive numerical spinbox component mirroring standard ttk.Spinbox behaviors.
    Features vertical stacked arrow adjustments, text validation filters, and boundary wrapping.
    Strictly resources parameters from the central registry with zero local design defaults.
    """

    def __init__(self, master=None, from_=0.0, to=100.0, step_size=1.0, command=None,
                 state="normal", wrap=False, justify="left", show=None, textvariable=None,
                 placeholder_text=None, exportselection=True, width=140, height=32, **kw):
        theme_defaults = THEME_DEFAULTS["sCTkSpinbox"]

        # 1. Initialize Themeable mixin safely to assemble self.final_kw and attributes
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # 2. FIXED POP GUARDS: Clean all custom variables out of the keyword dictionary to shield the frame layer.
        self.final_kw.pop("fg_color", None)
        self.final_kw.pop("text_color", None)
        self.final_kw.pop("entry_color", None)
        self.final_kw.pop("border_color", None)
        self.final_kw.pop("border_width", None)
        self.final_kw.pop("corner_radius", None)
        self.final_kw.pop("font", None)
        self.final_kw.pop("placeholder_text_color", None)
        self.final_kw.pop("button_color", None)
        self.final_kw.pop("button_hover_color", None)
        self.final_kw.pop("disabled_text_color", None)
        self.final_kw.pop("disabled_entry_color", None)
        self.final_kw.pop("disabled_border_color", None)
        self.final_kw.pop("disabled_button_color", None)

        # 3. Construct the custom base frame using raw configuration mappings
        super().__init__(master, width=width, height=height, fg_color="transparent", **self.final_kw)

        # Core operational constraint boundaries mimicking ttk.Spinbox variables
        self._from = float(from_)
        self._to = float(to)
        self._step_size = float(step_size)
        self._wrap = bool(wrap)
        self._state = "normal" if state.lower() == "normal" else "disabled"
        self._command = command

        # Configure layout grids inside our frame wrapper capsule
        self.grid_columnconfigure(0, weight=1)  # Entry field expands horizontally
        self.grid_columnconfigure(1, weight=0)  # Buttons column remains compact
        self.grid_rowconfigure((0, 1), weight=1)  # Buttons split vertical height uniformly

        # 4. FIXED MOUNT: Fully mapped text input entry field linking to your custom variables
        self.entry = ctk.CTkEntry(
            self,
            width=width - 24,
            height=height,
            justify=justify,
            show=show,
            textvariable=textvariable,
            placeholder_text=placeholder_text,
            exportselection=exportselection,
            fg_color=ThemeableWidget._resolve_color(self, theme_defaults.get("entry_color")),
            text_color=ThemeableWidget._resolve_color(self, theme_defaults.get("text_color")),
            border_color=ThemeableWidget._resolve_color(self, theme_defaults.get("border_color")),
            placeholder_text_color=ThemeableWidget._resolve_color(self, theme_defaults.get("placeholder_text_color")),
            border_width=theme_defaults.get("border_width", 1.5),
            corner_radius=theme_defaults.get("corner_radius", 6),
            font=theme_defaults.get("font")
        )
        self.entry.grid(row=0, column=0, rowspan=2, padx=(0, 2), pady=0, sticky="nsew")

        # Insert initial baseline register text data value only if a textvariable is absent
        if textvariable is None:
            self.entry.insert(0, str(self._from))

        # Bind value parsing safeguards upon user manual typing entry exit points
        self.entry.bind("<FocusOut>", lambda e: self._validate_and_sanitize_input())
        self.entry.bind("<Return>", lambda e: self._validate_and_sanitize_input())

        # 5. MOUNT: Stacked Vertical Directional Arrow Controls
        btn_w = 22
        btn_h = (height // 2) - 1

        self.up_button = ctk.CTkButton(
            self, text="▲", width=btn_w, height=btn_h, corner_radius=2,
            fg_color=ThemeableWidget._resolve_color(self, theme_defaults.get("button_color")),
            hover_color=ThemeableWidget._resolve_color(self, theme_defaults.get("button_hover_color")),
            text_color=ThemeableWidget._resolve_color(self, theme_defaults.get("text_color")),
            font=("Arial", 8), command=self._increment_callback
        )
        self.up_button.grid(row=0, column=1, padx=(1, 0), pady=(0, 1), sticky="nsew")

        self.down_button = ctk.CTkButton(
            self, text="▼", width=btn_w, height=btn_h, corner_radius=2,
            fg_color=ThemeableWidget._resolve_color(self, theme_defaults.get("button_color")),
            hover_color=ThemeableWidget._resolve_color(self, theme_defaults.get("button_hover_color")),
            text_color=ThemeableWidget._resolve_color(self, theme_defaults.get("text_color")),
            font=("Arial", 8), command=self._decrement_callback
        )
        self.down_button.grid(row=1, column=1, padx=(1, 0), pady=(1, 0), sticky="nsew")

        # Sync initial state configurations
        if self._state == "disabled":
            self.configure(state="disabled")

    def _set_appearance_mode(self, mode_string):
        """Intercepts the top-level application background theme color shifts."""
        super()._set_appearance_mode(mode_string)
        if hasattr(self, "entry") and self.entry.winfo_exists():
            # Delays execution slightly to allow system graphics registers to refresh safely
            self.after(20, self._process_live_theme_repaint)

    def _process_live_theme_repaint(self):
        """Forces all sub-components to perform fresh runtime token re-evaluations."""
        theme_defaults = THEME_DEFAULTS["sCTkSpinbox"]

        if self._state == "disabled":
            e_bg = theme_defaults.get("disabled_entry_color")
            e_bd = theme_defaults.get("disabled_border_color")
            txt = theme_defaults.get("disabled_text_color")
            btn = theme_defaults.get("disabled_button_color")
            btn_h = theme_defaults.get("disabled_button_color")
        else:
            e_bg = theme_defaults.get("entry_color")
            e_bd = theme_defaults.get("border_color")
            txt = theme_defaults.get("text_color")
            btn = theme_defaults.get("button_color")
            btn_h = theme_defaults.get("button_hover_color")

        # Push dynamic, resolved string color tokens down across sub-widget configurations
        self.entry.configure(
            fg_color=ThemeableWidget._resolve_color(self, e_bg),
            border_color=ThemeableWidget._resolve_color(self, e_bd),
            text_color=ThemeableWidget._resolve_color(self, txt),
            # FIXED: Dynamically re-evaluates the dimmed placeholder accent lines on repaint
            placeholder_text_color=ThemeableWidget._resolve_color(self, theme_defaults.get("placeholder_text_color"))
        )
        self.up_button.configure(
            fg_color=ThemeableWidget._resolve_color(self, btn),
            hover_color=ThemeableWidget._resolve_color(self, btn_h),
            text_color=ThemeableWidget._resolve_color(self, txt)
        )
        self.down_button.configure(
            fg_color=ThemeableWidget._resolve_color(self, btn),
            hover_color=ThemeableWidget._resolve_color(self, btn_h),
            text_color=ThemeableWidget._resolve_color(self, txt)
        )

    import sys
    import customtkinter as ctk

    # Direct framework path module and theme dictionary registry imports
    from sCTkFrame import sCTkFrame
    from ThemeableWidget import ThemeableWidget
    from sCTkThemes import THEME_DEFAULTS

    # FIXED: Import your custom high-fidelity design entry wrapper component
    from sCTkEntryPrimary import sCTkEntryPrimary

    class sCTkSpinbox(sCTkFrame, ThemeableWidget):
        """
        A theme-adaptive numerical spinbox component mirroring standard ttk.Spinbox behaviors.
        Features vertical stacked arrow adjustments, text validation filters, and boundary wrapping.
        Natively utilizes sCTkEntryPrimary to guarantee styling and contrast continuity.
        """

        def __init__(self, master=None, from_=0.0, to=100.0, step_size=1.0, command=None,
                     state="normal", wrap=False, justify="left", show=None, textvariable=None,
                     placeholder_text=None, exportselection=True, width=140, height=32, **kw):
            theme_defaults = THEME_DEFAULTS["sCTkSpinbox"]

            # 1. Initialize Themeable mixin safely to assemble self.final_kw and attributes
            ThemeableWidget.__init__(self, theme_defaults, kw)

            # 2. FIXED POP GUARDS: Clean all custom variables out of the keyword dictionary to shield the frame layer.
            self.final_kw.pop("fg_color", None)
            self.final_kw.pop("text_color", None)
            self.final_kw.pop("entry_color", None)
            self.final_kw.pop("border_color", None)
            self.final_kw.pop("border_width", None)
            self.final_kw.pop("corner_radius", None)
            self.final_kw.pop("font", None)
            self.final_kw.pop("placeholder_text_color", None)
            self.final_kw.pop("button_color", None)
            self.final_kw.pop("button_hover_color", None)
            self.final_kw.pop("disabled_text_color", None)
            self.final_kw.pop("disabled_entry_color", None)
            self.final_kw.pop("disabled_border_color", None)
            self.final_kw.pop("disabled_button_color", None)

            # 3. Construct the custom base frame using raw configuration mappings
            super().__init__(master, width=width, height=height, fg_color="transparent", **self.final_kw)

            # Core operational constraint boundaries mimicking ttk.Spinbox variables
            self._from = float(from_)
            self._to = float(to)
            self._step_size = float(step_size)
            self._wrap = bool(wrap)
            self._state = "normal" if state.lower() == "normal" else "disabled"
            self._command = command
            self._placeholder_text = placeholder_text

            # Configure layout grids inside our frame wrapper capsule
            self.grid_columnconfigure(0, weight=1)  # Entry field expands horizontally
            self.grid_columnconfigure(1, weight=0)  # Buttons column remains compact
            self.grid_rowconfigure((0, 1), weight=1)  # Buttons split vertical height uniformly

            # 4. FIXED MOUNT: Fully mapped input entry area utilizing sCTkEntryPrimary natively!
            # It automatically inherits all fonts, borders, contrast levels, and placeholders.
            self.entry = sCTkEntryPrimary(
                self,
                width=width - 24,
                height=height,
                justify=justify,
                show=show,
                textvariable=textvariable,
                placeholder_text=self._placeholder_text,
                exportselection=exportselection
            )
            self.entry.grid(row=0, column=0, rowspan=2, padx=(0, 2), pady=0, sticky="nsew")

            if textvariable is None:
                self.entry.insert(0, str(self._from))

            # Bind value parsing safeguards upon user manual typing entry exit points
            self.entry.bind("<FocusOut>", lambda e: self._validate_and_sanitize_input())
            self.entry.bind("<Return>", lambda e: self._validate_and_sanitize_input())

            # 5. MOUNT: Stacked Vertical Directional Arrow Controls
            btn_w = 22
            btn_h = (height // 2) - 1

            self.up_button = ctk.CTkButton(
                self, text="▲", width=btn_w, height=btn_h, corner_radius=2,
                fg_color=ThemeableWidget._resolve_color(self, theme_defaults.get("button_color")),
                hover_color=ThemeableWidget._resolve_color(self, theme_defaults.get("button_hover_color")),
                text_color=ThemeableWidget._resolve_color(self, theme_defaults.get("text_color")),
                font=("Arial", 8), command=self._increment_callback
            )
            self.up_button.grid(row=0, column=1, padx=(1, 0), pady=(0, 1), sticky="nsew")

            self.down_button = ctk.CTkButton(
                self, text="▼", width=btn_w, height=btn_h, corner_radius=2,
                fg_color=ThemeableWidget._resolve_color(self, theme_defaults.get("button_color")),
                hover_color=ThemeableWidget._resolve_color(self, theme_defaults.get("button_hover_color")),
                text_color=ThemeableWidget._resolve_color(self, theme_defaults.get("text_color")),
                font=("Arial", 8), command=self._decrement_callback
            )
            self.down_button.grid(row=1, column=1, padx=(1, 0), pady=(1, 0), sticky="nsew")

            # Sync initial state configurations
            if self._state == "disabled":
                self.configure(state="disabled")

        def _set_appearance_mode(self, mode_string):
            """Intercepts the top-level application background theme color shifts."""
            super()._set_appearance_mode(mode_string)
            if hasattr(self, "up_button") and self.up_button.winfo_exists():
                # Delays execution slightly to allow button styles to cascade accurately
                self.after(20, self._process_live_theme_repaint)

        def _process_live_theme_repaint(self):
            """Forces button layouts to perform fresh runtime token re-evaluations."""
            theme_defaults = THEME_DEFAULTS["sCTkSpinbox"]

            if self._state == "disabled":
                txt = theme_defaults.get("disabled_text_color")
                btn = theme_defaults.get("disabled_button_color")
                btn_h = theme_defaults.get("disabled_button_color")
            else:
                txt = theme_defaults.get("text_color")
                btn = theme_defaults.get("button_color")
                btn_h = theme_defaults.get("button_hover_color")

            self.up_button.configure(
                fg_color=ThemeableWidget._resolve_color(self, btn),
                hover_color=ThemeableWidget._resolve_color(self, btn_h),
                text_color=ThemeableWidget._resolve_color(self, txt)
            )
            self.down_button.configure(
                fg_color=ThemeableWidget._resolve_color(self, btn),
                hover_color=ThemeableWidget._resolve_color(self, btn_h),
                text_color=ThemeableWidget._resolve_color(self, txt)
            )

    def _increment_callback(self):
        """Advances the internal counter value up by one configured step size slice."""
        if self._state == "disabled": return
        current_val = self.get()
        if current_val is None: current_val = self._from

        new_value = current_val + self._step_size
        if new_value > self._to:
            new_value = self._from if self._wrap else self._to

        self.set(new_value)
        if self._command is not None: self._command()

    def _decrement_callback(self):
        """Drops the internal counter value down by one configured step size slice."""
        if self._state == "disabled": return
        current_val = self.get()
        if current_val is None: current_val = self._from

        new_value = current_val - self._step_size
        if new_value < self._from:
            new_value = self._to if self._wrap else self._from

        self.set(new_value)
        if self._command is not None: self._command()

    def _validate_and_sanitize_input(self):
        """Forces fallback clamps and resets entry characters upon text typing exit events."""
        current_val = self.get()
        if current_val is None:
            self.set(self._from)
            return
        clamped_val = max(self._from, min(self._to, current_val))
        self.set(clamped_val)

    def get(self):
        """Public getter tracking standard numerical values formatted back as float indices."""
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value):
        """Public setter clearing old strings and formatting entries cleanly."""
        try:
            tx_var = self.entry.cget("textvariable")
            if tx_var is not None:
                formatted_str = f"{float(value):.2f}".rstrip('0').rstrip('.')
                if formatted_str == "": formatted_str = "0"
                tx_var.set(formatted_str)
                return
        except Exception:
            pass

        self.entry.delete(0, "end")
        formatted_str = f"{float(value):.2f}".rstrip('0').rstrip('.')
        if formatted_str == "": formatted_str = "0"
        self.entry.insert(0, formatted_str)

    def configure(self, **kwargs):
        """Public unified frame configuration and state machine update triggers."""
        if "state" in kwargs:
            target_state = kwargs["state"].lower()
            self._state = "normal" if target_state == "normal" else "disabled"
            if self._state == "disabled":
                self.entry.configure(state="disabled")
                self.up_button.configure(state="disabled")
                self.down_button.configure(state="disabled")
            else:
                self.entry.configure(state="normal")
                self.up_button.configure(state="normal")
                self.down_button.configure(state="normal")
            del kwargs["state"]

        if "from_" in kwargs:
            self._from = float(kwargs["from_"])
            del kwargs["from_"]
        if "to" in kwargs:
            self._to = float(kwargs["to"])
            del kwargs["to"]
        if "step_size" in kwargs:
            self._step_size = float(kwargs["step_size"])
            del kwargs["step_size"]

        # Cascades pass-through settings straight to your sCTkEntryPrimary component layer
        for entry_attr in ["justify", "show", "textvariable", "placeholder_text", "exportselection"]:
            if entry_attr in kwargs:
                self.entry.configure(**{entry_attr: kwargs[entry_attr]})
                del kwargs[entry_attr]

        super().configure(**kwargs)

    def cget(self, attribute_name):
        """Public operational register attribute getter lookups."""
        if attribute_name == "state": return self._state
        if attribute_name == "from_": return self._from
        if attribute_name == "to": return self._to
        if attribute_name == "step_size": return self._step_size

        if attribute_name in ["justify", "show", "textvariable", "placeholder_text", "exportselection"]:
            return self.entry.cget(attribute_name)

        return super().cget(attribute_name)


import customtkinter as ctk


# Ensure cross-module tracking points find your local widget packages
# from sCTkSpinbox import sCTkSpinbox

def on_spinbox_value_changed():
    """
    Core Event Callback Hook: Automatically invoked on every valid click step change.
    Reads the value from the spinbox instance and updates our cockpit tracking label.
    """
    current_val = spinbox.get()
    if current_val is not None:
        # Formats output text data dynamically to match your dashboard rows
        vfo_readout.configure(text=f"Tuning Step: {current_val:.1f} kHz")


import customtkinter as ctk


# Ensure cross-module tracking points find your local widget packages
# from sCTkSpinbox import sCTkSpinbox

def on_spinbox_value_changed():
    """
    Core Event Callback Hook: Automatically invoked on every valid click step change.
    Reads the value from the spinbox instance and updates our cockpit tracking label.
    """
    current_val = spinbox.get()
    if current_val is not None:
        vfo_readout.configure(text=f"Tuning Step: {current_val:.1f} kHz")
    else:
        # Gracefully handle placeholder string states if the entry field is wiped blank
        vfo_readout.configure(text="Tuning Step: Empty / Incomplete")


import customtkinter as ctk

# Ensure cross-module tracking points find your local widget packages
from sCTkFrame import sCTkFrame
from sCTkSpinbox import sCTkSpinbox
from sCTkComboBox import sCTkComboBox
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkEntryPrimary import sCTkEntryPrimary
from sCTkCheckBox import sCTkCheckBox
from sCTkButtonPrimary import sCTkButtonPrimary


def on_spinbox_value_changed():
    """
    Core Event Callback Hook: Automatically invoked on every valid click step change.
    Reads the value from the spinbox instance and updates our cockpit tracking label.
    """
    current_val = spinbox.get()
    if current_val is not None:
        vfo_readout.configure(text=f"Tuning Step: {current_val:.1f} kHz")
    else:
        # Gracefully handle placeholder string states if the entry field is wiped blank
        vfo_readout.configure(text="Tuning Step: Empty / Incomplete")


import customtkinter as ctk

# Ensure cross-module tracking points find your local widget packages
from sCTkFrame import sCTkFrame
from sCTkSpinbox import sCTkSpinbox
from sCTkComboBox import sCTkComboBox  # FIXED: Capitalized the 'B' to match your module profile
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkEntryPrimary import sCTkEntryPrimary
from sCTkCheckBox import sCTkCheckBox
from sCTkButtonPrimary import sCTkButtonPrimary


def on_spinbox_value_changed():
    """
    Core Event Callback Hook: Automatically invoked on every valid click step change.
    Reads the value from the spinbox instance and updates our cockpit tracking label.
    """
    current_val = spinbox.get()
    if current_val is not None:
        vfo_readout.configure(text=f"Tuning Step: {current_val:.1f} kHz")
    else:
        # Gracefully handle placeholder string states if the entry field is wiped blank
        vfo_readout.configure(text="Tuning Step: Empty / Incomplete")


# =====================================================================
# SYSTEM ASSEMBLY TEST BENCH RUNNER MAIN
# =====================================================================
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("sCTk Advanced Spinbox Tester Deck")
    app.geometry("480x560")
    app.configure(fg_color=("#F1F5F9", "#1C1C1C"))

    # Outer parent frame layers updated to sCTkFrame
    dashboard_panel = sCTkFrame(app, fg_color="transparent", border_width=0)
    dashboard_panel.pack(padx=25, pady=15, fill="both", expand=True)

    # 1. MOUNT: Core telemetry tracking text status box label (sCTkLabelSecondary)
    vfo_readout = sCTkLabelSecondary(
        dashboard_panel,
        text="Tuning Step: 5.0 kHz",
        font=("Arial", 24, "bold"),
        text_color=("#1A4375", "#FF9100")
    )
    vfo_readout.pack(pady=10)

    # 2. MOUNT: The sCTkSpinbox Module (Natively wrapping sCTkEntryPrimary inside)
    spinbox = sCTkSpinbox(
        dashboard_panel,
        from_=1.0,
        to=50.0,
        step_size=0.5,
        wrap=True,
        justify="center",
        placeholder_text="Enter step...",
        command=on_spinbox_value_changed,
        width=160,
        height=34
    )
    spinbox.pack(pady=10)
    spinbox.set(5.0)

    # 3. MOUNT: Test Deck Configuration Panel Box (sCTkFrame)
    control_frame = sCTkFrame(dashboard_panel, fg_color=("#E2E8F0", "#262626"), corner_radius=6)
    control_frame.pack(fill="x", padx=10, pady=10)

    # --- Row 0: Component State Controller (sCTkLabelSecondary & sCTkComboBox) ---
    lbl_state = sCTkLabelSecondary(control_frame, text="Component State:", font=("Arial", 11, "bold"))
    lbl_state.grid(row=0, column=0, padx=15, pady=6, sticky="w")


    def on_state_dropdown_changed(choice):
        target_state = "normal" if "Normal" in choice else "disabled"
        spinbox.configure(state=target_state)


    # FIXED: Re-mapped to your exact sCTkComboBox name convention
    state_dropdown = sCTkComboBox(control_frame, values=["Normal State (Active)", "Disabled State (Locked)"],
                                  command=on_state_dropdown_changed, width=170)
    state_dropdown.grid(row=0, column=1, padx=15, pady=6, sticky="e")
    state_dropdown.set("Normal State (Active)")

    # --- Row 1: Text Justification (sCTkLabelSecondary & sCTkComboBox) ---
    lbl_justify = sCTkLabelSecondary(control_frame, text="Text Alignment (Justify):", font=("Arial", 11, "bold"))
    lbl_justify.grid(row=1, column=0, padx=15, pady=6, sticky="w")


    def on_justify_changed(choice):
        spinbox.configure(justify=choice.lower())


    # FIXED: Re-mapped to your exact sCTkComboBox name convention
    justify_dropdown = sCTkComboBox(control_frame, values=["Center", "Left", "Right"], command=on_justify_changed,
                                    width=170)
    justify_dropdown.grid(row=1, column=1, padx=15, pady=6, sticky="e")
    justify_dropdown.set("Center")

    # --- Row 2: Live Placeholder Text Updates (sCTkLabelSecondary & sCTkEntryPrimary) ---
    lbl_placeholder = sCTkLabelSecondary(control_frame, text="Placeholder Text String:", font=("Arial", 11, "bold"))
    lbl_placeholder.grid(row=2, column=0, padx=15, pady=6, sticky="w")


    def update_placeholder_text(event=None):
        new_text = txt_placeholder.get()
        spinbox.configure(placeholder_text=new_text)


    txt_placeholder = sCTkEntryPrimary(control_frame, width=170, height=28, placeholder_text="Type placeholder here...")
    txt_placeholder.grid(row=2, column=1, padx=15, pady=6, sticky="e")
    txt_placeholder.insert(0, "Enter step...")
    txt_placeholder.bind("<Return>", update_placeholder_text)
    txt_placeholder.bind("<FocusOut>", update_placeholder_text)


    # --- Row 3: Password Masking Toggle (sCTkCheckBox) ---
    def toggle_password_mask():
        mask_active = bool(check_show.get())
        spinbox.configure(show="*" if mask_active else "")


    check_show = sCTkCheckBox(control_frame, text="Mask Input Characters (show=\"*\")", command=toggle_password_mask,
                              font=("Arial", 11))
    check_show.grid(row=3, column=0, columnspan=2, padx=15, pady=8, sticky="w")


    # 4. Add an on-the-fly theme switcher button to check layout color flips live (sCTkButtonPrimary)
    def toggle_theme():
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")


    theme_btn = sCTkButtonPrimary(app, text="Toggle Light/Dark Theme", command=toggle_theme)
    theme_btn.pack(pady=5)

    app.mainloop()


