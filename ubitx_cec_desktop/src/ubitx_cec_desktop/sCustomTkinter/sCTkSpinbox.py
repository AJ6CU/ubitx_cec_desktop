#!/usr/bin/python3
"""
sCTkSpinbox

A theme-compliant, highly configurable custom spinbox wrapper component.
Supports numerical bounding steps or discrete custom string text arrays,
complete with orientation toggles, placement options, and wrap logic.
"""
import shlex
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
from ThemeableWidget import ThemeableWidget
from sCTkEntryPrimary import sCTkEntryPrimary


class sCTkSpinbox(ctk.CTkFrame, ThemeableWidget):
    def __init__(self, master=None, from_=0.0, to=100.0, step_size=1.0, command=None,
                 state="normal", wrap=False, justify="left", show=None, textvariable=None,
                 placeholder_text=None, exportselection=True, width=140, height=32, **kw):

        # 1. INTERCEPT CUSTOM LAYOUT & ARRAY PARAMETERS EARLY
        # Pop structural keys immediately to shield the parent frame from validation crashes
        button_width = kw.pop("button_width", 22)
        button_height = kw.pop("button_height", None)  # Dynamically calculated below if None
        button_side = kw.pop("button_side", "right")  # Options: "right", "left", "split"
        orientation = kw.pop("orientation", "vertical")  # Options: "vertical", "horizontal"
        arrow_font_size = kw.pop("arrow_font_size", 8)
        format_str = kw.pop("format", None)

        # Capture discrete text string values and wrap selections early
        values = kw.pop("values", None)
        wrap_val = kw.pop("wrap", wrap)

        theme_defaults = THEME_DEFAULTS["sCTkSpinbox"]

        # 2. Assign instance memory BEFORE running master parent initializers
        # This provides a clean single source of truth for design variables
        self._local_defaults = theme_defaults
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # 3. Run shared theme logic safely now that variables exist
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # 4. CLEAN POP GUARDS: Scrub theme style variables out of final_kw
        # This stops the parent ctk.CTkFrame container from throwing a unknown option error
        for pop_key in ["fg_color", "text_color", "entry_color", "border_color", "border_width",
                        "corner_radius", "font", "placeholder_text_color", "button_color",
                        "button_hover_color", "disabled_text_color", "disabled_entry_color",
                        "disabled_border_color", "disabled_button_color"]:
            self.final_kw.pop(pop_key, None)

        # 5. Construct the base capsule frame container natively
        super().__init__(master, width=width, height=height, fg_color="transparent", **self.final_kw)

        # Core operational constraint variables mirroring standard ttk.Spinbox behavior
        self._from = float(from_)
        self._to = float(to)
        self._step_size = float(step_size)
        self._wrap = wrap_val if isinstance(wrap_val, bool) else (str(wrap_val).lower() in ("true", "1", "yes"))
        self._command = command
        self._placeholder_text = placeholder_text
        self._format = str(format_str) if format_str else ""
        self._textvariable = textvariable

        # Parse value string lists natively to establish text indexing boundaries
        self._values = self._parse_string_list(values) if values else []
        self._current_index = 0 if self._values else -1

        # Save custom layout dimensions and typography rules to instance memory
        self._button_width = int(button_width)
        self._button_side = str(button_side).lower()
        self._orientation = str(orientation).lower()
        self._arrow_font_size = int(arrow_font_size)
        self._state = "normal" if str(state).lower() == "normal" else "disabled"

        # Automatically calculate matching vertical/horizontal button heights if None
        if button_height is not None:
            self._button_height = int(button_height)
        else:
            self._button_height = (height // 2) - 1 if self._orientation == "vertical" else height

        # 6. MOUNT ENTRY FIELD AREA (Explicitly forwards your spinbox theme font)
        used_buttons = 2 if self._button_side == "split" or self._orientation == "horizontal" else 1
        self.entry = sCTkEntryPrimary(
            self,
            width=width - (self._button_width * used_buttons),
            height=height,
            justify=justify,
            show=show,
            textvariable=self._textvariable,
            placeholder_text=self._placeholder_text,
            exportselection=exportselection,
            font=self._local_defaults["font"]
        )

        # Initial startup text population handling
        if self._textvariable is None:
            if self._values:
                # If String Index Mode is active, populate the first textual item row
                self.entry.insert(0, str(self._values[0]))
            else:
                self.entry.insert(0, self._format_value(self._from))
        else:
            # Sync the attached StringVar instantly if it arrived from Pygubu unpopulated
            if str(self._textvariable.get()).strip() == "":
                start_str = self._values[0] if self._values else self._format_value(self._from)
                self._textvariable.set(start_str)

        # Bind validation focus handlers for manual user keyboard typing inputs
        self.entry.bind("<FocusOut>", lambda e: self._validate_and_sanitize_input())
        self.entry.bind("<Return>", lambda e: self._validate_and_sanitize_input())

        # 7. MOUNT UP/DOWN DIRECTIONAL MECHANICAL BUTTON CONTROLS
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

        # 8. EXECUTE COMPONENT GEOMETRY MATRIX MAPPING
        self._rebuild_grid_layout()

        # Route initial state lockdown configurations seamlessly through the pipeline
        if self._state == "disabled":
            self.configure(state="disabled")

    def _parse_string_list(self, input_data) -> list:
        """
        Parses standard ttk.Spinbox text sequences natively.
        Handles collection list structures, CSV entries, and space-separated lines
        containing quoted substrings with embedded space characters cleanly.
        """
        if isinstance(input_data, (list, tuple)):
            return [str(x).strip() for x in input_data]
        raw_str = str(input_data).strip()
        if not raw_str:
            return []
        try:
            # shlex cleanly isolates space-separated tokens while protecting
            # quoted sections containing spaces, like: Item1 "Item Two" Item3
            if "," not in raw_str:
                return shlex.split(raw_str)
            # Fall back to splitting by comma strings if explicitly defined
            return [item.strip().strip('"').strip("'") for item in raw_str.split(',') if item.strip()]
        except Exception:
            # Fallback emergency split catch if shlex parsing fails
            return [item.strip() for item in raw_str.split() if item.strip()]

    def set_values(self, list_of_strings):
        """Programmatic convenience shortcut routine to update your choices list on the fly."""
        self._values = self._parse_string_list(list_of_strings)
        if self._values:
            self._current_index = 0
            self.set(self._values[0])
        else:
            self._current_index = -1
            self.set(getattr(self, "_from", 0.0))

    def _rebuild_grid_layout(self):
        """Calculates rows, columns, padding, and alignments based on side and orientation selections."""
        # 1. Explicitly reset column weights to clear CustomTkinter's geometry cache
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
            self.grid_columnconfigure(1, weight=1)  # Entry field stretches horizontally

            # Switch button arrow characters dynamically to match horizontal flow
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
                self.grid_columnconfigure(1, weight=1)  # Entry field stretches
                self.up_button.grid(row=0, column=0, padx=(0, 1), pady=(0, 1), sticky="nsew")
                self.down_button.grid(row=1, column=0, padx=(0, 1), pady=(1, 0), sticky="nsew")
                self.entry.grid(row=0, column=1, rowspan=2, padx=(1, 0), pady=0, sticky="nsew")
            elif self._button_side == "split":
                self.grid_columnconfigure(1, weight=1)
                self.down_button.grid(row=0, column=0, rowspan=2, padx=(0, 2), pady=0, sticky="nsew")
                self.entry.grid(row=0, column=1, rowspan=2, padx=(2, 2), pady=0, sticky="nsew")
                self.up_button.grid(row=0, column=2, rowspan=2, padx=(2, 0), pady=0, sticky="nsew")
            else:  # Default right
                self.grid_columnconfigure(0, weight=1)  # Entry field stretches
                self.entry.grid(row=0, column=0, rowspan=2, padx=(0, 2), pady=0, sticky="nsew")
                self.up_button.grid(row=0, column=1, padx=(1, 0), pady=(0, 1), sticky="nsew")
                self.down_button.grid(row=1, column=1, padx=(1, 0), pady=(1, 0), sticky="nsew")

        # Force an immediate layout redraw pass to notify CustomTkinter's canvas engine
        self.update_idletasks()

    def configure(self, require_redraw=None, **kwargs):
        """Standardized configuration handler supporting Pygubu workspace layout switches."""
        # --- Zone A: Position Intercept (Pygubu Properties Grid Reflection) ---
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
                                 str(getattr(self, "_textvariable", ""))),
                "wrap": ("wrap", "wrap", "wrap", "False", str(getattr(self, "_wrap", False))),
                "values": ("values", "values", "values", "",
                           " ".join([f'"{v}"' if ' ' in v else v for v in getattr(self, "_values", [])]))
            }
            if require_redraw in mapping: return mapping[require_redraw]
            return super().configure(require_redraw)

        if isinstance(require_redraw, dict):
            kwargs.update(require_redraw)

        # --- Zone B: Sanitization, Text Payload Routing & Variable Synchronization ---
        if "wrap" in kwargs:
            v_wrap = kwargs.pop("wrap")
            self._wrap = v_wrap if isinstance(v_wrap, bool) else (str(v_wrap).lower() in ("true", "1", "yes"))

        if "values" in kwargs:
            self._values = self._parse_string_list(kwargs.pop("values"))
            self._current_index = 0 if self._values else -1
            if self._values:
                self.set(self._values)

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

        # Intercept structural widget dimension adjustments
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

            # Automatically scale button height parameters on active layout switches
            if not kwargs.get("button_height") and hasattr(self, "cget"):
                current_height = int(self.cget("height"))
                self._button_height = (current_height // 2) - 1 if self._orientation == "vertical" else current_height
                self.up_button.configure(height=self._button_height)
                self.down_button.configure(height=self._button_height)
            rebuild_grid = True

        if "arrow_font_size" in kwargs:
            self._arrow_font_size = int(kwargs.pop("arrow_font_size"))
            # Triggers text configuration parameters instantly using your current orientation character symbols
            up_char = "▶" if self._orientation == "horizontal" else "▲"
            down_char = "◀" if self._orientation == "horizontal" else "▼"
            self.up_button.configure(font=("Arial", self._arrow_font_size), text=up_char)
            self.down_button.configure(font=("Arial", self._arrow_font_size), text=down_char)

        if "textvariable" in kwargs:
            new_var = kwargs["textvariable"]
            self._textvariable = new_var

            # Intercept empty Pygubu variables and initialize them to match floor boundaries safely
            if new_var is not None:
                try:
                    if str(new_var.get()).strip() == "":
                        start_str = self._values if self._values else self._format_value(self._from)
                        new_var.set(start_str)
                except Exception:
                    pass

        # Tunnel core entry field modifications down into the nested wrapper module
        for entry_attr in ["justify", "show", "textvariable", "placeholder_text", "exportselection"]:
            if entry_attr in kwargs:
                if hasattr(self, "entry") and self.entry.winfo_exists():
                    self.entry.configure(**{entry_attr: kwargs[entry_attr]})
                if entry_attr == "placeholder_text":
                    self._placeholder_text = kwargs[entry_attr]
                kwargs.pop(entry_attr)

        # Force inner layout geometries to dynamically re-slice boundaries
        if rebuild_grid and hasattr(self, "cget") and hasattr(self, "entry"):
            current_width = int(self.cget("width"))
            used_b = 2 if self._button_side == "split" or self._orientation == "horizontal" else 1
            self.entry.configure(width=current_width - (self._button_width * used_b))
            self._rebuild_grid_layout()

        # --- Zone C: State Controller Management ---
        if "state" in kwargs:
            self._state = str(kwargs.pop("state")).lower()
            for child in [self.entry, self.up_button, self.down_button]:
                if hasattr(child, "winfo_exists") and child.winfo_exists():
                    child.configure(state=self._state)
            self._process_live_theme_repaint()

        # --- Zone D: Base Execution Pass ---
        if kwargs: super().configure(**kwargs)

    def cget(self, attribute_name):
        """Standard tracker getter loop mapped to internal class storage targets."""
        pname = str(attribute_name).lower()
        if pname in ["state", "from_", "to", "step_size", "button_width", "button_height", "button_side", "orientation",
                     "arrow_font_size", "format", "wrap", "values"]:
            return getattr(self, f"_{pname}")
        return super().cget(attribute_name)

    def _format_value(self, val: float) -> str:
        """Utility helper that safely applies string parsing rules to floats."""
        fmt = self._format.strip() if hasattr(self, "_format") and self._format else ""
        if fmt:
            # 1. Handle curly brace format styles (Ideal for Pygubu-Designer)
            if "{" in fmt and "}" in fmt:
                try:
                    return fmt.format(val)
                except Exception:
                    pass
            # 2. Handle raw text indicators if curly braces were left out (e.g. ":.3f")
            elif ":" in fmt and not "{" in fmt:
                try:
                    return ("{" + fmt + "}").format(val)
                except Exception:
                    pass
            # 3. Handle traditional C-style percent format strings
            elif "%" in fmt:
                try:
                    return fmt % val
                except Exception:
                    pass
        # Dynamic fallback guessing based on step_size decimal resolution
        dec_places = len(str(self._step_size).split('.')) if '.' in str(self._step_size) else 0
        return f"{val:.{dec_places}f}"

    def get(self) -> str:
        """Prioritizes active tracking variables if attached to catch manual typing updates."""
        if hasattr(self, "_textvariable") and self._textvariable:
            return str(self._textvariable.get())
        if hasattr(self, "entry") and self.entry.winfo_exists():
            return str(self.entry.get())
        return str(getattr(self, "_from", "0.0"))

    def set(self, value):
        """Standardized setter method ensuring numbers and discrete text lists update synchronously."""
        try:
            if not getattr(self, "_values", None):
                # Pure numerical tracking track
                num = float(value)
                f_limit = getattr(self, "_from", None)
                t_limit = getattr(self, "_to", None)
                if f_limit is not None and num < f_limit: num = f_limit
                if t_limit is not None and num > t_limit: num = t_limit
                display_text = self._format_value(num)
                callback_val = num
            else:
                # String array mode preserves text formatting perfectly
                display_text = str(value)
                if display_text in self._values:
                    self._current_index = self._values.index(display_text)
                callback_val = display_text

            if hasattr(self, "_textvariable") and self._textvariable:
                self._textvariable.set(display_text)

            old_state = self.entry.cget("state")
            self.entry.configure(state="normal")
            self.entry.delete(0, "end")
            self.entry.insert(0, display_text)
            self.entry.configure(state=old_state)

            if self._command:
                try:
                    self._command(callback_val)
                except TypeError:
                    self._command()  # Support callbacks that accept no arguments safely
        except ValueError:
            # Fallback to direct text pass-through if parsing a float fails but strings are active
            if getattr(self, "_values", None):
                display_text = str(value)
                if display_text in self._values:
                    self._current_index = self._values.index(display_text)
                self.entry.configure(state="normal")
                self.entry.delete(0, "end")
                self.entry.insert(0, display_text)
                self.entry.configure(state="normal" if self._state == "normal" else "readonly")

    def _increment_callback(self):
        """Processes upward step increments across both float counters and string array indices."""
        if self._state == "disabled": return
        if hasattr(self, "_values") and self._values:
            next_idx = self._current_index + 1
            if next_idx >= len(self._values):
                next_idx = 0 if self._wrap else (len(self._values) - 1)
            self._current_index = next_idx
            self.set(self._values[self._current_index])
            return
        try:
            current_val = float(self.get())
            next_val = current_val + self._step_size
            if next_val > self._to:
                next_val = self._from if self._wrap else self._to
            self.set(next_val)
        except ValueError:
            self.set(self._from)

    def _decrement_callback(self):
        """Processes downward step decrements across both float counters and string array indices."""
        if self._state == "disabled": return
        if hasattr(self, "_values") and self._values:
            next_idx = self._current_index - 1
            if next_idx < 0:
                next_idx = (len(self._values) - 1) if self._wrap else 0
            self._current_index = next_idx
            self.set(self._values[self._current_index])
            return
        try:
            current_val = float(self.get())
            next_val = current_val - self._step_size
            if next_val < self._from:
                next_val = self._to if self._wrap else self._from
            self.set(next_val)
        except ValueError:
            self.set(self._from)

    def _validate_and_sanitize_input(self):
        """Sanitizes manual user keyboard entries upon widget focus exit boundaries."""
        if getattr(self, "_values", None):
            raw_text = self.get()
            if raw_text in self._values:
                self._current_index = self._values.index(raw_text)
            return
        try:
            raw_text = self.get()
            if not raw_text.strip():
                self.set(self._from)
                return
            self.set(float(raw_text))
        except ValueError:
            self.set(self._from)

    def _process_live_theme_repaint(self):
        """Strict theme repainting using direct explicit lookups from cached defaults."""
        if self._state == "disabled":
            # Extract the nested map directly to satisfy your zero-fallback hard-stop requirements
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
            # Revert completely back to your pure operational active theme defaults
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
# =============================================================================
#   STANDALONE HARNESS TEST DECK (PART 1 OF 2)
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
    app.geometry("490x740")  # Canvas bounds optimized for list data input rows
    app.configure(fg_color=("#F1F5F9", "#1C1C1C"))

    # Event telemetry logging monitor callback
    def on_spinbox_value_changed(val):
        if isinstance(val, float):
            vfo_readout.configure(text=f"Telemetry Output: {val:.3f}")
        else:
            vfo_readout.configure(text=f"Telemetry Output: '{str(val)}'")

    # Outer master panel layout capsule
    dashboard_panel = sCTkFrame(app, fg_color="transparent", border_width=0)
    dashboard_panel.pack(padx=25, pady=15, fill="both", expand=True)

    # 1. MOUNT: Live Readout Status Text Display Block
    vfo_readout = sCTkLabelSecondary(
        dashboard_panel,
        text="Telemetry Output: Initializing...",
        font=("Arial", 22, "bold"),
        text_color=("#1A4375", "#FF9100")
    )
    vfo_readout.pack(pady=10)

    # 2. MOUNT: The Core Spinbox Target Component Instance
    spinbox = sCTkSpinbox(
        dashboard_panel,
        from_=1.0,
        to=50.0,
        step_size=0.5,
        wrap=True,
        justify="center",
        placeholder_text="Enter step...",
        command=on_spinbox_value_changed,
        width=180,
        height=34
    )
    spinbox.pack(pady=10)
    spinbox.set(5.0)  # Initial value seed

    # 3. MOUNT: Properties Panel Card Layout Grid Frame
    control_frame = sCTkFrame(dashboard_panel, fg_color=("#E2E8F0", "#262626"), corner_radius=6)
    control_frame.pack(fill="both", expand=True, padx=5, pady=10)
    control_frame.grid_columnconfigure(0, weight=1)
    control_frame.grid_columnconfigure(1, weight=1)

    # --- Row 0: Component Interactive Input State Controller ---
    lbl_state = sCTkLabelSecondary(control_frame, text="Component State:", font=("Arial", 11, "bold"))
    lbl_state.grid(row=0, column=0, padx=15, pady=5, sticky="w")

    def on_state_dropdown_changed(choice):
        spinbox.configure(state="disabled" if "Disabled" in choice else "normal")

    state_dropdown = ctk.CTkComboBox(control_frame, values=["Normal State (Active)", "Disabled State (Locked)"],
                                     command=on_state_dropdown_changed, width=170)
    state_dropdown.grid(row=0, column=1, padx=15, pady=5, sticky="e")
    state_dropdown.set("Normal State (Active)")

    # --- Row 1: Internal Input Content Arrangement Alignment ---
    lbl_justify = sCTkLabelSecondary(control_frame, text="Text Alignment (Justify):", font=("Arial", 11, "bold"))
    lbl_justify.grid(row=1, column=0, padx=15, pady=5, sticky="w")

    def on_justify_changed(choice):
        spinbox.configure(justify=choice.lower())

    justify_dropdown = ctk.CTkComboBox(control_frame, values=["Center", "Left", "Right"], command=on_justify_changed,
                                       width=170)
    justify_dropdown.grid(row=1, column=1, padx=15, pady=5, sticky="e")
    justify_dropdown.set("Center")
    # --- Row 2: Live Masking Format String Controller ---
    lbl_format = sCTkLabelSecondary(control_frame, text="Masking Format Pattern:", font=("Arial", 11, "bold"))
    lbl_format.grid(row=2, column=0, padx=15, pady=5, sticky="w")

    def on_format_changed(choice):
        fmt_map = {"%.1f kHz": "%.1f kHz", "{:.2f}": "{:.2f}", "{:.3f}": "{:.3f}", "None (Default)": ""}
        spinbox.configure(format=fmt_map.get(choice, ""))

    format_dropdown = ctk.CTkComboBox(control_frame, values=["None (Default)", "%.1f kHz", "{:.2f}", "{:.3f}"],
                                      command=on_format_changed, width=170)
    format_dropdown.grid(row=2, column=1, padx=15, pady=5, sticky="e")
    format_dropdown.set("None (Default)")

    # --- Row 3: Mechanical Boundary Iteration Loop Wrap ---
    lbl_wrap = sCTkLabelSecondary(control_frame, text="Boundary Iteration Wrap:", font=("Arial", 11, "bold"))
    lbl_wrap.grid(row=3, column=0, padx=15, pady=5, sticky="w")

    def on_wrap_toggled(choice):
        spinbox.configure(wrap=True if "True" in choice else False)

    wrap_dropdown = ctk.CTkComboBox(control_frame, values=["True (Loop Enabled)", "False (Hard Limits)"],
                                    command=on_wrap_toggled, width=170)
    wrap_dropdown.grid(row=3, column=1, padx=15, pady=5, sticky="e")
    wrap_dropdown.set("True (Loop Enabled)")

    # --- Row 4: String Array Mode vs Numerical Toggle Track ---
    lbl_mode = sCTkLabelSecondary(control_frame, text="Data Array Input Mode:", font=("Arial", 11, "bold"))
    lbl_mode.grid(row=4, column=0, padx=15, pady=5, sticky="w")

    def on_mode_changed(choice):
        if "Discrete List" in choice:
            # ✅ FIXED: Route the raw text string directly through your convenience shortcut!
            # This resets your pointer index back to 0 and displays the first element instantly.
            spinbox.set_values(txt_custom_values.get())
        else:
            # Clear out the list arrays completely and restore pure float boundaries
            spinbox.set_values([])
            spinbox.set(5.0)

    mode_dropdown = ctk.CTkComboBox(control_frame, values=["Numerical Mode (1.0 - 50.0)", "Discrete List Mode (Strings)"],
                                    command=on_mode_changed, width=170)
    mode_dropdown.grid(row=4, column=1, padx=15, pady=5, sticky="e")
    mode_dropdown.set("Numerical Mode (1.0 - 50.0)")

    # --- Row 5: Dynamic Custom String Input Loader Fields ---
    lbl_custom_vals = sCTkLabelSecondary(control_frame, text="List Strings Configuration:", font=("Arial", 11, "bold"))
    lbl_custom_vals.grid(row=5, column=0, padx=15, pady=5, sticky="w")

    def sync_live_text_array(event=None):
        # Force a real-time options reload if already viewing string values
        if "Discrete List" in mode_dropdown.get():
            spinbox.set_values(txt_custom_values.get())

    txt_custom_values = sCTkEntryPrimary(control_frame, width=170, height=28, placeholder_text="Item1 'Item Two' Item3...")
    txt_custom_values.grid(row=5, column=1, padx=15, pady=5, sticky="e")
    txt_custom_values.insert(0, 'Slow Normal Fast "Turbo Speed" Max')
    txt_custom_values.bind("<Return>", sync_live_text_array)
    txt_custom_values.bind("<FocusOut>", sync_live_text_array)

    # --- Row 6: Hardware Alignment Placement Side ---
    lbl_side = sCTkLabelSecondary(control_frame, text="Hardware Button Side:", font=("Arial", 11, "bold"))
    lbl_side.grid(row=6, column=0, padx=15, pady=5, sticky="w")

    def on_side_changed(choice):
        spinbox.configure(button_side=choice.lower())

    side_dropdown = ctk.CTkComboBox(control_frame, values=["Right", "Left", "Split"], command=on_side_changed, width=170)
    side_dropdown.grid(row=6, column=1, padx=15, pady=5, sticky="e")
    side_dropdown.set("Right")

    # --- Row 7: Structural Layout Orientation ---
    lbl_orient = sCTkLabelSecondary(control_frame, text="Control Grid Orientation:", font=("Arial", 11, "bold"))
    lbl_orient.grid(row=7, column=0, padx=15, pady=5, sticky="w")

    def on_orientation_changed(choice):
        spinbox.configure(orientation=choice.lower())

    orient_dropdown = ctk.CTkComboBox(control_frame, values=["Vertical", "Horizontal"], command=on_orientation_changed, width=170)
    orient_dropdown.grid(row=7, column=1, padx=15, pady=5, sticky="e")
    orient_dropdown.set("Vertical")

    # --- Row 8: Dynamic Arrow Character Font Scaler Track ---
    lbl_arrow_size = sCTkLabelSecondary(control_frame, text="Arrow Glyphs Font Size:", font=("Arial", 11, "bold"))
    lbl_arrow_size.grid(row=8, column=0, padx=15, pady=5, sticky="w")

    def on_arrow_size_changed(choice):
        size_num = int(choice.split())
        spinbox.configure(arrow_font_size=size_num)

    arrow_size_dropdown = ctk.CTkComboBox(control_frame, values=["8 pt (Default)", "11 pt (Medium)", "14 pt (Large)", "18 pt"],
                                         command=on_arrow_size_changed, width=170)
    arrow_size_dropdown.grid(row=8, column=1, padx=15, pady=5, sticky="e")
    arrow_size_dropdown.set("8 pt (Default)")

    # 4. Live Visual Theme Workspace Repaint Trigger Switch
    def toggle_theme():
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")

    theme_btn = sCTkButtonPrimary(app, text="Toggle UI Light/Dark Appearance", command=toggle_theme)
    theme_btn.pack(pady=10)

    app.mainloop()
