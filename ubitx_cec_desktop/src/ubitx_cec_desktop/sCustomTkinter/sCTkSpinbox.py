#!/usr/bin/python3
"""
sCTkSpinbox

A theme-compliant, highly configurable custom spinbox wrapper component.
"""
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
from ThemeableWidget import ThemeableWidget
from sCTkEntryPrimary import sCTkEntryPrimary


class sCTkSpinbox(ctk.CTkFrame, ThemeableWidget):
    def __init__(self, master=None, from_=0.0, to=100.0, step_size=1.0, command=None,
                 state="normal", wrap=False, justify="left", show=None, textvariable=None,
                 placeholder_text=None, exportselection=True, width=140, height=32, **kw):

        # 1. INTERCEPT CUSTOM LAYOUT PARAMETERS EARLY
        button_width = kw.pop("button_width", 22)
        button_height = kw.pop("button_height", None)  # Dynamically calculated below if None
        button_side = kw.pop("button_side", "right")  # Options: "right", "left", "split"
        orientation = kw.pop("orientation", "vertical")  # Options: "vertical", "horizontal"
        # ADD THIS LINE: Capture custom arrow font size parameters early
        arrow_font_size = kw.pop("arrow_font_size", 8)
        format_str = kw.pop("format", None)

        theme_defaults = THEME_DEFAULTS["sCTkSpinbox"]

        # 2. Assign instance memory BEFORE running master parent initializers
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # 3. Run shared theme logic safely now that variables exist
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # 4. Clean custom style variables out of final_kw to protect parent frame
        for pop_key in ["fg_color", "text_color", "entry_color", "border_color", "border_width",
                        "corner_radius", "font", "placeholder_text_color", "button_color",
                        "button_hover_color", "disabled_text_color", "disabled_entry_color",
                        "disabled_border_color", "disabled_button_color"]:
            self.final_kw.pop(pop_key, None)

        # 5. Construct the base capsule frame natively
        super().__init__(master, width=width, height=height, fg_color="transparent", **self.final_kw)

        # Core operational parameters
        self._from = float(from_)
        self._to = float(to)
        self._step_size = float(step_size)
        self._wrap = bool(wrap)
        self._state = "normal" if str(state).lower() == "normal" else "disabled"
        self._command = command
        self._placeholder_text = placeholder_text
        self._format = str(format_str) if format_str else ""

        # Save custom layout attributes to instance memory
        self._button_width = int(button_width)
        self._button_side = str(button_side).lower()
        self._orientation = str(orientation).lower()
        self._arrow_font_size = int(arrow_font_size)

        # Calculate dynamic button heights if not explicitly overriden
        if button_height is not None:
            self._button_height = int(button_height)
        else:
            self._button_height = (height // 2) - 1 if self._orientation == "vertical" else height

        # 6. MOUNT ENTRY CONTAINER LAYER
        self.entry = sCTkEntryPrimary(
            self,
            width=width - (self._button_width * 2 if self._button_side == "split" or self._orientation == "horizontal" else self._button_width),
            height=height,
            justify=justify,
            show=show,
            textvariable=textvariable,
            placeholder_text=self._placeholder_text,
            exportselection=exportselection,
            # FIXED: Explicitly forward the spinbox's custom theme font straight down!
            # If the "font" key is ever accidentally missing from sCTkThemes, this triggers a loud hard-stop crash.
            font=self._local_defaults["font"]
        )

        # FIXED: Format your very first initial value pass using your custom string controller
        if textvariable is None:
            init_val = self._from
            if self._format:
                try:
                    formatted_txt = self._format % init_val
                except Exception:
                    formatted_txt = f"{init_val:.2f}"
            else:
                # Fallback to smart guessing based on step_size decimals
                dec_places = len(str(self._step_size).split('.')[1]) if '.' in str(self._step_size) else 0
                formatted_txt = f"{init_val:.{dec_places}f}"

            self.entry.insert(0, formatted_txt)

        self.entry.bind("<FocusOut>", lambda e: self._validate_and_sanitize_input())
        self.entry.bind("<Return>", lambda e: self._validate_and_sanitize_input())

        # 7. MOUNT DIRECTIONAL ARROW BUTTONS
        # Update the button font trackers to use your dynamic instance variable string token
        self.up_button = ctk.CTkButton(
            self, text="▲", width=self._button_width, height=self._button_height, corner_radius=2,
            fg_color=ThemeableWidget._resolve_color(self, theme_defaults.get("button_color")),
            hover_color=ThemeableWidget._resolve_color(self, theme_defaults.get("button_hover_color")),
            text_color=ThemeableWidget._resolve_color(self, theme_defaults.get("text_color")),
            font=("Arial", self._arrow_font_size), command=self._increment_callback
        )

        self.down_button = ctk.CTkButton(
            self, text="▼", width=self._button_width, height=self._button_height, corner_radius=2,
            fg_color=ThemeableWidget._resolve_color(self, theme_defaults.get("button_color")),
            hover_color=ThemeableWidget._resolve_color(self, theme_defaults.get("button_hover_color")),
            text_color=ThemeableWidget._resolve_color(self, theme_defaults.get("text_color")),
            font=("Arial", self._arrow_font_size), command=self._decrement_callback
        )

        # 8. PROCESS GRID GEOMETRY MATRIX MAPS
        self._rebuild_grid_layout()

        # Sync initial state configurations through the pipeline
        if self._state == "disabled":
            self.configure(state="disabled")

        # FIXED INITIALIZATION POPULATION PASS:
        # Ensures that even under early Pygubu initialization sweeps, a clean starting number is forced on canvas!
        if textvariable is None:
            self.set(self._from)
        else:
            # If a variable is attached, force its initial state to mirror the floor limit
            if not textvariable.get():
                textvariable.set(self._format_value(self._from))
            self.set(textvariable.get())


    def _rebuild_grid_layout(self):
        """Calculates rows, columns, padding, and alignments based on side and orientation selections."""
        # 1. FIXED: Explicitly reset column weights back to index 0 across ALL possible tracks
        # to clear CustomTkinter's geometry cache before altering orientations!
        for col_idx in range(3):
            self.grid_columnconfigure(col_idx, weight=0, minsize=0)
        for row_idx in range(2):
            self.grid_rowconfigure(row_idx, weight=0, minsize=0)

        # 2. Clear existing geometry placements safely
        self.entry.grid_forget()
        self.up_button.grid_forget()
        self.down_button.grid_forget()

        if self._orientation == "horizontal":
            # Horizontal layout forces buttons to be full height side-by-side or split
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)  # Entry stretches horizontally

            # Switch button arrow characters dynamically to match horizontal flow
            # FIXED: Pass your active instance font variable along when swapping characters!
            self.up_button.configure(text="▶", font=("Arial", self._arrow_font_size))
            self.down_button.configure(text="◀", font=("Arial", self._arrow_font_size))

            if self._button_side == "left":
                self.down_button.grid(row=0, column=0, padx=(0, 1), pady=0, sticky="nsew")
                self.up_button.grid(row=0, column=1, padx=(1, 1), pady=0, sticky="nsew")
                self.entry.grid(row=0, column=2, padx=(1, 0), pady=0, sticky="nsew")
            elif self._button_side == "split":
                # Split puts decrement on far left, increment on far right
                self.down_button.grid(row=0, column=0, padx=(0, 2), pady=0, sticky="nsew")
                self.entry.grid(row=0, column=1, padx=(2, 2), pady=0, sticky="nsew")
                self.up_button.grid(row=0, column=2, padx=(2, 0), pady=0, sticky="nsew")
            else:  # Default right
                self.entry.grid(row=0, column=0, padx=(0, 1), pady=0, sticky="nsew")
                self.down_button.grid(row=0, column=1, padx=(1, 1), pady=0, sticky="nsew")
                self.up_button.grid(row=0, column=2, padx=(1, 0), pady=0, sticky="nsew")

        else:  # Vertical layout stack
            self.grid_rowconfigure((0, 1), weight=1)

            # Restore standard vertical arrow character markers
            self.up_button.configure(text="▲", font=("Arial", self._arrow_font_size))
            self.down_button.configure(text="▼", font=("Arial", self._arrow_font_size))

            if self._button_side == "left":
                self.grid_columnconfigure(1, weight=1)  # Entry stretches
                self.up_button.grid(row=0, column=0, padx=(0, 1), pady=(0, 1), sticky="nsew")
                self.down_button.grid(row=1, column=0, padx=(0, 1), pady=(1, 0), sticky="nsew")
                self.entry.grid(row=0, column=1, rowspan=2, padx=(1, 0), pady=0, sticky="nsew")
            elif self._button_side == "split":
                self.grid_columnconfigure(1, weight=1)
                self.down_button.grid(row=0, column=0, rowspan=2, padx=(0, 2), pady=0, sticky="nsew")
                self.entry.grid(row=0, column=1, rowspan=2, padx=(2, 2), pady=0, sticky="nsew")
                self.up_button.grid(row=0, column=2, rowspan=2, padx=(2, 0), pady=0, sticky="nsew")
            else:  # Default right
                self.grid_columnconfigure(0, weight=1)  # Entry stretches
                self.entry.grid(row=0, column=0, rowspan=2, padx=(0, 2), pady=0, sticky="nsew")
                self.up_button.grid(row=0, column=1, padx=(1, 0), pady=(0, 1), sticky="nsew")
                self.down_button.grid(row=1, column=1, padx=(1, 0), pady=(1, 0), sticky="nsew")

        # 3. FIXED: Force an immediate layout redraw pass to notify CustomTkinter's canvas engine
        self.update_idletasks()

    def configure(self, require_redraw=None, **kwargs):
        """Standardized configuration handler supporting Pygubu layout switches."""
        # --- Zone A: Position Intercept (Pygubu Compatibility) ---
        if require_redraw is not None and not kwargs and isinstance(require_redraw, str):
            mapping = {
                "state": ("state", "state", "state", "normal", str(getattr(self, "_state", "normal"))),
                "from_": ("from_", "from_", "from_", "0.0", str(getattr(self, "_from", 0.0))),
                "to": ("to", "to", "to", "100.0", str(getattr(self, "_to", 100.0))),
                "step_size": ("step_size", "step_size", "step_size", "1.0", str(getattr(self, "_step_size", 1.0))),
                "button_width": ("button_width", "button_width", "button_width", "22",
                                 str(getattr(self, "_button_width", 22))),
                "button_height": ("button_height", "button_height", "button_height", "",
                                  str(getattr(self, "_button_height", ""))),
                "button_side": ("button_side", "button_side", "button_side", "right",
                                str(getattr(self, "_button_side", "right"))),
                "orientation": ("orientation", "orientation", "orientation", "vertical",
                                str(getattr(self, "_orientation", "vertical"))),
                "justify": ("justify", "justify", "justify", "left", str(self.entry.cget("justify"))),
                "placeholder_text": ("placeholder_text", "placeholder_text", "placeholder_text", "",
                                     str(getattr(self, "_placeholder_text", ""))),
                "format": ("format", "format", "format", "", str(getattr(self, "_format", ""))),
                "textvariable": ("textvariable", "textvariable", "textvariable", "",
                                 str(getattr(self, "_textvariable", "")))
            }
            if require_redraw in mapping: return mapping[require_redraw]
            return super().configure(require_redraw)

        if isinstance(require_redraw, dict):
            kwargs.update(require_redraw)

        # =====================================================================
        # ZONE B: SANITIZATION, TEXT PAYLOAD ROUTING & VARIABLE SYNCHRONIZATION
        # =====================================================================
        if "textvariable" in kwargs:
            new_var = kwargs["textvariable"]
            self._textvariable = new_var  # Cache the internal pointer reference

            # FIXED STARTUP SYNC PASS: If the incoming Pygubu variable is completely empty,
            # initialize its value to your current floor boundary BEFORE it links and wipes the screen!
            if new_var is not None:
                try:
                    # Check if the string variable is empty or unpopulated
                    if str(new_var.get()).strip() == "":
                        # Pull your current active value, format it cleanly, and force it onto the variable
                        current_num = getattr(self, "_from", 0.0)
                        formatted_start = self._format_value(current_num)
                        new_var.set(formatted_start)
                except Exception:
                    pass

        for key in ["from_", "to", "step_size"]:
            if key in kwargs:
                setattr(self, f"_{key}",
                        float(kwargs.pop(key) or (0.0 if key == 'from_' else 100.0 if key == 'to' else 1.0)))

        if "command" in kwargs:
            self._command = kwargs.pop("command")

        if "format" in kwargs:
            self._format = str(kwargs.pop("format") or "")
            try:
                current_val = float(self.get())
                self.set(current_val)
            except Exception:
                pass

        # Intercept structural layout property changes
        rebuild_grid = False
        if "button_width" in kwargs:
            self._button_width = int(kwargs.pop("button_width"))
            self.up_button.configure(width=self._button_width)
            self.down_button.configure(width=self._button_width)
            rebuild_grid = True
        if "button_height" in kwargs:
            self._button_height = int(kwargs.pop("button_height"))
            self.up_button.configure(height=self._button_height)
            self.down_button.configure(height=self._button_height)
            rebuild_grid = True
        if "button_side" in kwargs:
            val = kwargs.pop("button_side")
            self._button_side = str(val or "right").strip().lower()
            rebuild_grid = True
        if "orientation" in kwargs:
            val = kwargs.pop("orientation")
            self._orientation = str(val or "vertical").strip().lower()

            if not kwargs.get("button_height") and hasattr(self, "cget"):
                current_height = int(self.cget("height"))
                self._button_height = (current_height // 2) - 1 if self._orientation == "vertical" else current_height
                self.up_button.configure(height=self._button_height)
                self.down_button.configure(height=self._button_height)
            rebuild_grid = True

        if "arrow_font_size" in kwargs:
            self._arrow_font_size = int(kwargs.pop("arrow_font_size"))
            up_char = "▶" if self._orientation == "horizontal" else "▲"
            down_char = "◀" if self._orientation == "horizontal" else "▼"
            self.up_button.configure(font=("Arial", self._arrow_font_size), text=up_char)
            self.down_button.configure(font=("Arial", self._arrow_font_size), text=down_char)

        # FIXED TEXTVARIABLE INTERCEPT TRACK:
        if "textvariable" in kwargs:
            self._textvariable = kwargs["textvariable"]  # Keep internal tracking reference

        for entry_attr in ["justify", "show", "textvariable", "placeholder_text", "exportselection"]:
            if entry_attr in kwargs:
                if hasattr(self, "entry") and self.entry.winfo_exists():
                    self.entry.configure(**{entry_attr: kwargs[entry_attr]})
                if entry_attr == "placeholder_text":
                    self._placeholder_text = kwargs[entry_attr]
                kwargs.pop(entry_attr)

        if rebuild_grid:
            if hasattr(self, "cget") and hasattr(self, "entry"):
                current_width = int(self.cget("width"))
                used_buttons = 2 if self._button_side == "split" or self._orientation == "horizontal" else 1
                self.entry.configure(width=current_width - (self._button_width * used_buttons))
            self._rebuild_grid_layout()

        if "state" in kwargs:
            self._state = str(kwargs.pop("state")).lower()
            for child in [self.entry, self.up_button, self.down_button]:
                if hasattr(child, "winfo_exists") and child.winfo_exists():
                    child.configure(state=self._state)
            self._process_live_theme_repaint()

        if kwargs: super().configure(**kwargs)

    def _format_value(self, val: float) -> str:
        """Utility helper that safely applies string parsing rules to floats."""
        fmt = self._format.strip() if hasattr(self, "_format") and self._format else ""

        if fmt:
            if "{" in fmt and "}" in fmt:
                try:
                    res = fmt.format(val)
                    return res
                except Exception as e:
                    print(f"[FORMAT ENGINE] Curly-Brace calculation failed: {e}")
            elif ":" in fmt and not "{" in fmt:
                try:
                    wrapped = "{" + fmt + "}"
                    res = wrapped.format(val)
                    return res
                except Exception as e:
                    print(f"[FORMAT ENGINE] Raw Colon calculation failed: {e}")
            elif "%" in fmt:
                try:
                    res = fmt % val
                    return res
                except Exception as e:
                    print(f"[FORMAT ENGINE] Percent-Style calculation failed: {e}")

        dec_places = len(str(self._step_size).split('.')) if '.' in str(self._step_size) else 0
        res = f"{val:.{dec_places}f}"
        return res

    def set(self, value):
        """Standardized setter method ensuring tracking variables synchronize dynamically."""
        try:
            num = float(value)
            f_limit = getattr(self, "_from", None)
            t_limit = getattr(self, "_to", None)
            if f_limit is not None and num < f_limit: num = f_limit
            if t_limit is not None and num > t_limit: num = t_limit

            formatted_text = self._format_value(num)

            # FIXED DATA SYNC PASS: Force variables to update tracking states cleanly!
            if hasattr(self, "_textvariable") and self._textvariable:
                self._textvariable.set(formatted_text)

            old_state = self.entry.cget("state")
            self.entry.configure(state="normal")
            self.entry.delete(0, "end")
            self.entry.insert(0, formatted_text)
            self.entry.configure(state=old_state)

            if self._command:
                self._command(num)
        except ValueError:
            pass

    def cget(self, attribute_name):
        pname = str(attribute_name).lower()
        if pname in ["state", "from_", "to", "step_size", "button_width", "button_height", "button_side", "orientation",
                     "arrow_font_size", "format"]:
            return getattr(self, f"_{pname}")
        return super().cget(attribute_name)

    def _process_live_theme_repaint(self):
        """Strict theme repainting using direct explicit lookups from cached defaults."""
        if self._state == "disabled":
            disabled_map = self._local_defaults["disabled_map"]
            if hasattr(self, "entry") and self.entry.winfo_exists():
                self.entry.configure(
                    fg_color=ThemeableWidget._resolve_color(self, disabled_map["entry_color"]),
                    border_color=ThemeableWidget._resolve_color(self, disabled_map["border_color"]),
                    text_color=ThemeableWidget._resolve_color(self, disabled_map["text_color"]),
                    placeholder_text_color=ThemeableWidget._resolve_color(self, self._local_defaults[
                        "placeholder_text_color"])
                )
            for button in [self.up_button, self.down_button]:
                if hasattr(button, "winfo_exists") and button.winfo_exists():
                    button.configure(
                        fg_color=ThemeableWidget._resolve_color(self, disabled_map["button_color"]),
                        hover_color=ThemeableWidget._resolve_color(self, disabled_map["button_color"]),
                        text_color=ThemeableWidget._resolve_color(self, disabled_map["text_color"])
                    )
        else:
            if hasattr(self, "entry") and self.entry.winfo_exists():
                self.entry.configure(
                    fg_color=ThemeableWidget._resolve_color(self, self._local_defaults["entry_color"]),
                    border_color=ThemeableWidget._resolve_color(self, self._local_defaults["border_color"]),
                    text_color=ThemeableWidget._resolve_color(self, self._local_defaults["text_color"]),
                    placeholder_text_color=ThemeableWidget._resolve_color(self, self._local_defaults[
                        "placeholder_text_color"])
                )
            for button in [self.up_button, self.down_button]:
                if hasattr(button, "winfo_exists") and button.winfo_exists():
                    button.configure(
                        fg_color=ThemeableWidget._resolve_color(self, self._local_defaults["button_color"]),
                        hover_color=ThemeableWidget._resolve_color(self, self._local_defaults["button_hover_color"]),
                        text_color=ThemeableWidget._resolve_color(self, self._local_defaults["text_color"])
                    )


    def _increment_callback(self):
        if self._state == "disabled": return
        try:
            current_val = float(self.get())
            next_val = current_val + self._step_size

            if next_val > self._to:
                next_val = self._from if self._wrap else self._to

            self.set(next_val)
        except ValueError:
            self.set(self._from)

    def _decrement_callback(self):
        if self._state == "disabled": return
        try:
            current_val = float(self.get())
            next_val = current_val - self._step_size

            if next_val < self._from:
                next_val = self._to if self._wrap else self._from

            self.set(next_val)
        except ValueError:
            self.set(self._from)



    def _validate_and_sanitize_input(self):
        """Sanitizes manual user keyboard inputs upon text field exit points."""
        try:
            raw_text = self.get()
            if not raw_text.strip():
                self.set(self._from)
                return
            self.set(float(raw_text))
        except ValueError:
            self.set(self._from)

    def get(self) -> str:
        """FIXED GETTER: Prioritizes active tracking variables if attached."""
        if hasattr(self, "_textvariable") and self._textvariable:
            return str(self._textvariable.get())
        if hasattr(self, "entry") and self.entry.winfo_exists():
            return str(self.entry.get())
        return str(getattr(self, "_from", "0.0"))


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


# =====================================================================
# SYSTEM ASSEMBLY TEST BENCH RUNNER MAIN
# =====================================================================
# =============================================================================
#   STANDALONE HARNESS TEST DECK
# =============================================================================
if __name__ == "__main__":
    import customtkinter as ctk
    # Import your local themed sub-components
    from sCTkFrame import sCTkFrame
    from sCTkLabelSecondary import sCTkLabelSecondary
    from sCTkComboBox import sCTkComboBox
    from sCTkEntryPrimary import sCTkEntryPrimary
    from sCTkCheckBox import sCTkCheckBox
    from sCTkButtonPrimary import sCTkButtonPrimary

    app = ctk.CTk()
    app.title("sCTk Advanced Spinbox Tester Deck")
    app.geometry("480x640")  # Expanded height slightly to accommodate new layout controls smoothly
    app.configure(fg_color=("#F1F5F9", "#1C1C1C"))

    # Event tracking logger for value adjustments
    def on_spinbox_value_changed(val):
        vfo_readout.configure(text=f"Tuning Step: {val:.1f} kHz")

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
        width=180,  # Given a bit more width to display split/horizontal structures nicely
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

    state_dropdown = ctk.CTkComboBox(control_frame, values=["Normal State (Active)", "Disabled State (Locked)"],
                                  command=on_state_dropdown_changed, width=170)
    state_dropdown.grid(row=0, column=1, padx=15, pady=6, sticky="e")
    state_dropdown.set("Normal State (Active)")

    # --- Row 1: Text Justification (sCTkLabelSecondary & sCTkComboBox) ---
    lbl_justify = sCTkLabelSecondary(control_frame, text="Text Alignment (Justify):", font=("Arial", 11, "bold"))
    lbl_justify.grid(row=1, column=0, padx=15, pady=6, sticky="w")

    def on_justify_changed(choice):
        spinbox.configure(justify=choice.lower())

    justify_dropdown = ctk.CTkComboBox(control_frame, values=["Center", "Left", "Right"], command=on_justify_changed,
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

    # --- NEW: Row 3: Button Placement Side (sCTkLabelSecondary & sCTkComboBox) ---
    lbl_side = sCTkLabelSecondary(control_frame, text="Button Placement Side:", font=("Arial", 11, "bold"))
    lbl_side.grid(row=3, column=0, padx=15, pady=6, sticky="w")

    def on_side_changed(choice):
        spinbox.configure(button_side=choice.lower())

    side_dropdown = ctk.CTkComboBox(control_frame, values=["Right", "Left", "Split"], command=on_side_changed, width=170)
    side_dropdown.grid(row=3, column=1, padx=15, pady=6, sticky="e")
    side_dropdown.set("Right")

    # --- NEW: Row 4: Component Grid Orientation (sCTkLabelSecondary & sCTkComboBox) ---
    lbl_orient = sCTkLabelSecondary(control_frame, text="Control Orientation:", font=("Arial", 11, "bold"))
    lbl_orient.grid(row=4, column=0, padx=15, pady=6, sticky="w")

    def on_orientation_changed(choice):
        spinbox.configure(orientation=choice.lower())

    orient_dropdown = ctk.CTkComboBox(control_frame, values=["Vertical", "Horizontal"], command=on_orientation_changed, width=170)
    orient_dropdown.grid(row=4, column=1, padx=15, pady=6, sticky="e")
    orient_dropdown.set("Vertical")

    # --- Row 5: Arrow Character Sizing (sCTkLabelSecondary & CTkComboBox) ---
    lbl_arrow_size = sCTkLabelSecondary(control_frame, text="Arrow Indicator Size:", font=("Arial", 11, "bold"))
    lbl_arrow_size.grid(row=5, column=0, padx=15, pady=6, sticky="w")


    def on_arrow_size_changed(choice):
        size_num = int(choice.split()[0])  # Extracts the number from strings like "8 pt" Safely
        spinbox.configure(arrow_font_size=size_num)


    arrow_size_dropdown = ctk.CTkComboBox(
        control_frame,
        values=["6 pt (Small)", "8 pt (Default)", "11 pt (Medium)", "14 pt (Large)", "18 pt", "24 pt", "36 pt"],
        command=on_arrow_size_changed,
        width=170
    )

    arrow_size_dropdown.grid(row=5, column=1, padx=15, pady=6, sticky="e")
    arrow_size_dropdown.set("8 pt (Default)")


    # --- Row 6: Password Masking Toggle (sCTkCheckBox) ---
    def toggle_password_mask():
        mask_active = bool(check_show.get())
        spinbox.configure(show="*" if mask_active else "")


    # 1. INITIALIZE FIRST (Creates the variable token in memory)
    check_show = sCTkCheckBox(control_frame, text="Mask Input Characters (show=\"*\")", command=toggle_password_mask,
                              font=("Arial", 11))

    # 2. GRID SECOND (Now completely safe from NameError exceptions!)
    check_show.grid(row=6, column=0, columnspan=2, padx=15, pady=8, sticky="w")


    # 4. Add an on-the-fly theme switcher button to check layout color flips live (sCTkButtonPrimary)
    def toggle_theme():
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")

    theme_btn = sCTkButtonPrimary(app, text="Toggle Light/Dark Theme", command=toggle_theme)
    theme_btn.pack(pady=5)

    app.mainloop()



