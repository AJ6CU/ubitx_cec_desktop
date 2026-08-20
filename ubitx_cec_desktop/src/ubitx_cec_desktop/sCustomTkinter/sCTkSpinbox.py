#!/usr/bin/python3
"""
sCTkSpinbox

A theme-compliant, highly configurable custom spinbox wrapper component.
Operates entirely programmatically via get() and set() methods, bypassing
textvariable trace conflicts to guarantee pristine placeholder rendering.
"""
import shlex
import customtkinter as ctk
from sCTkThemes import THEME_DEFAULTS
from ThemeableWidget import ThemeableWidget
from sCTkEntryPrimary import sCTkEntryPrimary


class sCTkSpinbox(ctk.CTkFrame, ThemeableWidget):
    def __init__(self, master=None, from_=0.0, to=100.0, step_size=1.0, command=None,
                 state="normal", wrap=False, justify="left", show=None,
                 placeholder_text=None, exportselection=True, width=140, height=32, **kw):

        # 1. Initialize local theme defaults from sCTkThemes.py first
        self._local_defaults = THEME_DEFAULTS["sCTkSpinbox"]
        self._custom_disabled_map = self._local_defaults.get("disabled_map", {})

        # 2. Extract structural keyword extensions early
        button_width = kw.pop("button_width", 22)
        button_height = kw.pop("button_height", None)
        button_side = kw.pop("button_side", "right")
        orientation = kw.pop("orientation", "vertical")

        # Safely pull arrow points size from the theme font tuple fallback
        arrow_font_size = kw.pop("arrow_font_size", self._local_defaults["arrow_font"][1])
        format_str = kw.pop("format", None)
        values = kw.pop("values", None)
        wrap_val = kw.pop("wrap", wrap)

        # 3. Run shared mixin logic to populate style keys
        ThemeableWidget.__init__(self, self._local_defaults, kw)

        # 4. Scrub theme properties out of final_kw to protect parent CTkFrame
        for pop_key in ["fg_color", "text_color", "entry_color", "border_color", "border_width",
                        "corner_radius", "font", "placeholder_text_color", "button_color",
                        "button_hover_color", "disabled_text_color", "disabled_entry_color",
                        "disabled_border_color", "disabled_button_color",
                        "arrow_font", "arrow_up_char", "arrow_down_char", "arrow_right_char", "arrow_left_char"]:
            self.final_kw.pop(pop_key, None)

        # 5. Build base container frame
        super().__init__(master, width=width, height=height, fg_color="transparent", **self.final_kw)

        # Unpack styling fonts
        self._arrow_font_family = self._local_defaults["arrow_font"][0]
        self._arrow_font_size = int(arrow_font_size)

        # Core operational constraint boundaries
        self._from = float(from_)
        self._to = float(to)
        self._step_size = float(step_size)
        self._wrap = wrap_val if isinstance(wrap_val, bool) else (str(wrap_val).lower() in ("true", "1", "yes"))
        self._command = command
        self._placeholder_text = placeholder_text
        self._format = str(format_str) if format_str else ""

        # Parse text arrays for Discrete List Mode
        self._values = self._parse_string_list(values) if values else []
        self._current_index = 0 if self._values else -1

        self._button_width = int(button_width)
        self._button_side = str(button_side).lower()
        self._orientation = str(orientation).lower()
        self._state = "normal" if str(state).lower() == "normal" else "disabled"

        if button_height is not None:
            self._button_height = int(button_height)
        else:
            self._button_height = (height // 2) - 1 if self._orientation == "vertical" else height

        # 6. Mount internal text entry sub-widget
        used_buttons = 2 if self._button_side == "split" or self._orientation == "horizontal" else 1
        self.entry = sCTkEntryPrimary(
            self,
            width=width - (self._button_width * used_buttons),
            height=height,
            justify=justify,
            show=show,
            placeholder_text=self._placeholder_text,
            exportselection=exportselection
        )

        # 7. Initial Value Seeding (Only insert if no placeholder prompt exists)
        if not self._placeholder_text or str(self._placeholder_text).strip() == "":
            if self._values:
                self.entry.insert(0, str(self._values))
            else:
                self.entry.insert(0, self._format_value(self._from))

        # Keyboard typing focus handlers
        self.entry.bind("<FocusOut>", lambda e: self._validate_and_sanitize_input())
        self.entry.bind("<Return>", lambda e: self._validate_and_sanitize_input())

        # 8. Mount directional buttons using central theme glyph markers
        self.up_button = ctk.CTkButton(
            self,
            text=self._local_defaults["arrow_up_char"] if self._orientation == "vertical" else self._local_defaults[
                "arrow_right_char"],
            width=self._button_width, height=self._button_height, corner_radius=2,
            fg_color=ThemeableWidget._resolve_color(self, self._local_defaults["button_color"]),
            hover_color=ThemeableWidget._resolve_color(self, self._local_defaults["button_hover_color"]),
            text_color=ThemeableWidget._resolve_color(self, self._local_defaults["text_color"]),
            font=(self._arrow_font_family, self._arrow_font_size), command=self._increment_callback
        )

        self.down_button = ctk.CTkButton(
            self,
            text=self._local_defaults["arrow_down_char"] if self._orientation == "vertical" else self._local_defaults[
                "arrow_left_char"],
            width=self._button_width, height=self._button_height, corner_radius=2,
            fg_color=ThemeableWidget._resolve_color(self, self._local_defaults["button_color"]),
            hover_color=ThemeableWidget._resolve_color(self, self._local_defaults["button_hover_color"]),
            text_color=ThemeableWidget._resolve_color(self, self._local_defaults["text_color"]),
            font=(self._arrow_font_family, self._arrow_font_size), command=self._decrement_callback
        )

        # Map grid geometry structures and lock states
        self._rebuild_grid_layout()
        if self._state == "disabled":
            self.configure(state="disabled")

        # 9. Force a strict theme colors repaint loop
        self._process_live_theme_repaint()

    def _parse_string_list(self, input_data) -> list:
        """Parses standard space-separated or comma-separated configuration string arrays."""
        if isinstance(input_data, (list, tuple)):
            return [str(x).strip() for x in input_data]
        raw_str = str(input_data).strip()
        if not raw_str:
            return []
        try:
            # shlex isolates spaces while preserving double-quoted text substrings neatly
            return shlex.split(raw_str) if "," not in raw_str else [item.strip().strip('"').strip("'") for item in
                                                                    raw_str.split(',') if item.strip()]
        except Exception:
            return [item.strip() for item in raw_str.split() if item.strip()]

    def set_values(self, list_of_strings):
        """Programmatic shortcut routine to swap discrete text choices on the fly."""
        self._values = self._parse_string_list(list_of_strings)
        self._current_index = 0 if self._values else -1
        if self._values:
            self.set(self._values)
        else:
            self.set(getattr(self, "_from", 0.0))

    def _rebuild_grid_layout(self):
        """Calculates rows, columns, and alignments based on button_side and orientation settings."""
        # 1. Clear grid matrices to reset internal weights cache safely
        for i in range(3): self.grid_columnconfigure(i, weight=0, minsize=0)
        for i in range(2): self.grid_rowconfigure(i, weight=0, minsize=0)
        self.entry.grid_forget();
        self.up_button.grid_forget();
        self.down_button.grid_forget()

        if self._orientation == "horizontal":
            self.grid_rowconfigure(0, weight=1);
            self.grid_columnconfigure(1, weight=1)
            self.up_button.configure(text=self._local_defaults["arrow_right_char"],
                                     font=(self._arrow_font_family, self._arrow_font_size))
            self.down_button.configure(text=self._local_defaults["arrow_left_char"],
                                       font=(self._arrow_font_family, self._arrow_font_size))
            if self._button_side == "left":
                self.down_button.grid(row=0, column=0, padx=(0, 1), sticky="nsew")
                self.up_button.grid(row=0, column=1, padx=(1, 1), sticky="nsew")
                self.entry.grid(row=0, column=2, padx=(1, 0), sticky="nsew")
            elif self._button_side == "split":
                self.down_button.grid(row=0, column=0, padx=(0, 2), sticky="nsew")
                self.entry.grid(row=0, column=1, padx=(2, 2), sticky="nsew")
                self.up_button.grid(row=0, column=2, padx=(2, 0), sticky="nsew")
            else:  # Default right
                self.entry.grid(row=0, column=0, padx=(0, 1), sticky="nsew")
                self.down_button.grid(row=0, column=1, padx=(1, 1), sticky="nsew")
                self.up_button.grid(row=0, column=2, padx=(1, 0), sticky="nsew")
        else:  # Default vertical
            self.grid_rowconfigure((0, 1), weight=1)
            self.up_button.configure(text=self._local_defaults["arrow_up_char"],
                                     font=(self._arrow_font_family, self._arrow_font_size))
            self.down_button.configure(text=self._local_defaults["arrow_down_char"],
                                       font=(self._arrow_font_family, self._arrow_font_size))
            if self._button_side == "left":
                self.grid_columnconfigure(1, weight=1)
                self.up_button.grid(row=0, column=0, padx=(0, 1), pady=(0, 1), sticky="nsew")
                self.down_button.grid(row=1, column=0, padx=(0, 1), pady=(1, 0), sticky="nsew")
                self.entry.grid(row=0, column=1, rowspan=2, padx=(1, 0), sticky="nsew")
            elif self._button_side == "split":
                self.grid_columnconfigure(1, weight=1)
                self.down_button.grid(row=0, column=0, rowspan=2, padx=(0, 2), sticky="nsew")
                self.entry.grid(row=0, column=1, rowspan=2, padx=(2, 2), sticky="nsew")
                self.up_button.grid(row=0, column=2, rowspan=2, padx=(2, 0), sticky="nsew")
            else:  # Default right
                self.grid_columnconfigure(0, weight=1)
                self.entry.grid(row=0, column=0, rowspan=2, padx=(0, 2), sticky="nsew")
                self.up_button.grid(row=0, column=1, padx=(1, 0), pady=(0, 1), sticky="nsew")
                self.down_button.grid(row=1, column=1, padx=(1, 0), pady=(1, 0), sticky="nsew")

        self.update_idletasks()

    def configure(self, require_redraw=None, **kwargs):
        """Standardized configuration handler supporting Pygubu workspace properties switches."""
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
                "wrap": ("wrap", "wrap", "wrap", "False", str(getattr(self, "_wrap", False))),
                "values": ("values", "values", "values", "",
                           " ".join([f'"{v}"' if ' ' in v else v for v in getattr(self, "_values", [])]))
            }
            if require_redraw in mapping: return mapping[require_redraw]
            return super().configure(require_redraw)

        if isinstance(require_redraw, dict): kwargs.update(require_redraw)

        if "wrap" in kwargs:
            v_wrap = kwargs.pop("wrap")
            self._wrap = v_wrap if isinstance(v_wrap, bool) else (str(v_wrap).lower() in ("true", "1", "yes"))

        if "values" in kwargs:
            self._values = self._parse_string_list(kwargs.pop("values"))
            self._current_index = 0 if self._values else -1
            if self._values: self.set(self._values)

        for key in ["from_", "to", "step_size"]:
            if key in kwargs: setattr(self, f"_{key}", float(
                kwargs.pop(key) or (0.0 if key == 'from_' else 100.0 if key == 'to' else 1.0)))

        if "command" in kwargs: self._command = kwargs.pop("command")

        if "format" in kwargs:
            self._format = str(kwargs.pop("format") or "")
            try:
                self.set(float(self.get()))
            except Exception:
                pass

        rebuild_grid = False
        if "button_width" in kwargs:
            self._button_width = int(kwargs.pop("button_width"))
            self.up_button.configure(width=self._button_width);
            self.down_button.configure(width=self._button_width);
            rebuild_grid = True
        if "button_height" in kwargs:
            self._button_height = int(kwargs.pop("button_height"))
            self.up_button.configure(height=self._button_height);
            self.down_button.configure(height=self._button_height);
            rebuild_grid = True
        if "button_side" in kwargs:
            self._button_side = str(kwargs.pop("button_side") or "right").strip().lower();
            rebuild_grid = True
        if "orientation" in kwargs:
            self._orientation = str(kwargs.pop("orientation") or "vertical").strip().lower()
            if not kwargs.get("button_height") and hasattr(self, "cget"):
                self._button_height = (int(self.cget("height")) // 2) - 1 if self._orientation == "vertical" else int(
                    self.cget("height"))
                self.up_button.configure(height=self._button_height);
                self.down_button.configure(height=self._button_height)
            rebuild_grid = True

        if "arrow_font_size" in kwargs:
            self._arrow_font_size = int(kwargs.pop("arrow_font_size"))
            up_char = self._local_defaults["arrow_right_char"] if self._orientation == "horizontal" else \
            self._local_defaults["arrow_up_char"]
            down_char = self._local_defaults["arrow_left_char"] if self._orientation == "horizontal" else \
            self._local_defaults["arrow_down_char"]
            self.up_button.configure(font=(self._arrow_font_family, self._arrow_font_size), text=up_char)
            self.down_button.configure(font=(self._arrow_font_family, self._arrow_font_size), text=down_char)

        # Clean check to scrub auto-inserted initial values when a valid placeholder text is configured
        if "placeholder_text" in kwargs:
            self._placeholder_text = kwargs["placeholder_text"]
            if self._placeholder_text and str(self._placeholder_text).strip() != "":
                if hasattr(self, "entry") and self.entry.winfo_exists():
                    current_text = str(self.entry.get()).strip()
                    is_numeric_default = False
                    try:
                        val_check = float(current_text)
                        if val_check == 0.0 or val_check == getattr(self, "_from", 0.0): is_numeric_default = True
                    except ValueError:
                        pass
                    if is_numeric_default or current_text in ("", "0", "0.0"):
                        old_state = self.entry.cget("state");
                        self.entry.configure(state="normal");
                        self.entry.delete(0, "end");
                        self.entry.configure(state=old_state)

        # Tunnel core styling attributes directly down to the entry sub-widget
        for entry_attr in ["justify", "show", "placeholder_text", "exportselection"]:
            if entry_attr in kwargs:
                if hasattr(self, "entry") and self.entry.winfo_exists(): self.entry.configure(
                    **{entry_attr: kwargs[entry_attr]})
                kwargs.pop(entry_attr)

        if rebuild_grid and hasattr(self, "cget") and hasattr(self, "entry"):
            used_b = 2 if self._button_side == "split" or self._orientation == "horizontal" else 1
            self.entry.configure(width=int(self.cget("width")) - (self._button_width * used_b))
            self._rebuild_grid_layout()

        if "state" in kwargs:
            self._state = str(kwargs.pop("state")).lower()
            for child in [self.entry, self.up_button, self.down_button]:
                if hasattr(child, "winfo_exists") and child.winfo_exists(): child.configure(state=self._state)
            self._process_live_theme_repaint()

        if kwargs: super().configure(**kwargs)

    def cget(self, attribute_name):
        """Standard attribute read loop mapped to internal class storage variables."""
        pname = str(attribute_name).lower()
        if pname in ["state", "from_", "to", "step_size", "button_width", "button_height", "button_side", "orientation",
                     "arrow_font_size", "format", "wrap", "values"]:
            return getattr(self, f"_{pname}")
        return super().cget(attribute_name)

    def _format_value(self, val: float) -> str:
        """Utility helper that safely applies string mask rules to floating point numbers."""
        fmt = self._format.strip() if hasattr(self, "_format") and self._format else ""
        if fmt:
            if "{" in fmt and "}" in fmt:
                try:
                    return fmt.format(val)
                except Exception:
                    pass
            elif ":" in fmt and not "{" in fmt:
                try:
                    return ("{" + fmt + "}").format(val)
                except Exception:
                    pass
            elif "%" in fmt:
                try:
                    return fmt % val
                except Exception:
                    pass
        dec_places = len(str(self._step_size).split('.')) if '.' in str(self._step_size) else 0
        return f"{val:.{dec_places}f}"

    def get(self) -> str:
        """Programmatic value query shortcut fetching active input cell layout text."""
        if hasattr(self, "entry") and self.entry.winfo_exists():
            return str(self.entry.get())
        return str(getattr(self, "_from", "0.0"))

    def set(self, value):
        """Programmatic setter method that safely syncs numbers and list tracking ranges."""
        try:
            if not getattr(self, "_values", None):
                num = float(value)
                if getattr(self, "_from", None) is not None and num < self._from: num = self._from
                if getattr(self, "_to", None) is not None and num > self._to: num = self._to
                display_text = self._format_value(num)
                callback_val = num
            else:
                display_text = str(value)
                if display_text in self._values: self._current_index = self._values.index(display_text)
                callback_val = display_text

            old_state = self.entry.cget("state");
            self.entry.configure(state="normal");
            self.entry.delete(0, "end");
            self.entry.insert(0, display_text);
            self.entry.configure(state=old_state)
            if self._command:
                try:
                    self._command(callback_val)
                except TypeError:
                    self._command()
        except ValueError:
            if getattr(self, "_values", None):
                display_text = str(value)
                if display_text in self._values: self._current_index = self._values.index(display_text)
                self.entry.configure(state="normal");
                self.entry.delete(0, "end");
                self.entry.insert(0, display_text);
                self.entry.configure(state="normal" if self._state == "normal" else "readonly")

    def _increment_callback(self):
        """Processes upward step steps across both float counters and string array indices."""
        if self._state == "disabled": return
        if hasattr(self, "_values") and self._values:
            i = self._current_index + 1
            if i >= len(self._values): i = 0 if self._wrap else (len(self._values) - 1)
            self._current_index = i;
            self.set(self._values[i]);
            return
        try:
            n = float(self.get() if self.get().strip() else self._from) + self._step_size
            if n > self._to: n = self._from if self._wrap else self._to
            self.set(n)
        except ValueError:
            self.set(self._from)

    def _decrement_callback(self):
        """Processes downward step steps across both float counters and string array indices."""
        if self._state == "disabled": return
        if hasattr(self, "_values") and self._values:
            i = self._current_index - 1
            if i < 0: i = (len(self._values) - 1) if self._wrap else 0
            self._current_index = i;
            self.set(self._values[i]);
            return
        try:
            n = float(self.get() if self.get().strip() else self._from) - self._step_size
            if n < self._from: n = self._to if self._wrap else self._from
            self.set(n)
        except ValueError:
            self.set(self._from)

    def _validate_and_sanitize_input(self):
        """Sanitizes manual user keyboard entries upon entry widget focus exits."""
        if getattr(self, "_values", None):
            if self.get() in self._values: self._current_index = self._values.index(self.get())
            return
        try:
            if not self.get().strip(): self.set(self._from); return
            self.set(float(self.get()))
        except ValueError:
            self.set(self._from)

    def _process_live_theme_repaint(self):
        """Strict theme repainting using untouched raw light/dark layout tuple pairings."""
        if self._state == "disabled":
            m = self._local_defaults["disabled_map"]
            if hasattr(self, "entry") and self.entry.winfo_exists():
                self.entry.configure(fg_color=m["entry_color"], border_color=m["border_color"],
                                     text_color=m["text_color"],
                                     placeholder_text_color=self._local_defaults["placeholder_text_color"])
                if hasattr(self.entry, "_process_live_theme_repaint"): self.entry._process_live_theme_repaint()
            for b in [self.up_button, self.down_button]:
                if hasattr(b, "winfo_exists") and b.winfo_exists():
                    b.configure(fg_color=ThemeableWidget._resolve_color(self, m["button_color"]),
                                hover_color=ThemeableWidget._resolve_color(self, m["button_color"]),
                                text_color=ThemeableWidget._resolve_color(self, m["text_color"]))
        else:
            if hasattr(self, "entry") and self.entry.winfo_exists():
                self.entry.configure(fg_color=self._local_defaults["entry_color"],
                                     border_color=self._local_defaults["border_color"],
                                     text_color=self._local_defaults["text_color"],
                                     placeholder_text_color=self._local_defaults["placeholder_text_color"])
                if hasattr(self.entry, "_process_live_theme_repaint"): self.entry._process_live_theme_repaint()
            for b in [self.up_button, self.down_button]:
                if hasattr(b, "winfo_exists") and b.winfo_exists():
                    b.configure(fg_color=ThemeableWidget._resolve_color(self, self._local_defaults["button_color"]),
                                hover_color=ThemeableWidget._resolve_color(self,
                                                                           self._local_defaults["button_hover_color"]),
                                text_color=ThemeableWidget._resolve_color(self, self._local_defaults["text_color"]))
# =============================================================================
#   STANDALONE HARNESS TEST DECK (PART 5 OF 5)
# =============================================================================
if __name__ == "__main__":
    import customtkinter as ctk
    # Import your local themed framework sub-components safely
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

    # Outer master panel layout capsule capsule
    dashboard_panel = sCTkFrame(app, fg_color="transparent", border_width=0)
    dashboard_panel.pack(padx=25, pady=15, fill="both", expand=True)

    # 1. MOUNT: Live Readout Status Text Display Block
    vfo_readout = sCTkLabelSecondary(
        dashboard_panel, text="Telemetry Output: Initializing...",
        font=("Arial", 22, "bold"), text_color=("#1A4375", "#FF9100")
    )
    vfo_readout.pack(pady=10)

    # 2. MOUNT: The Core Spinbox Target Component Instance (With high-visibility placeholder)
    spinbox = sCTkSpinbox(
        dashboard_panel, from_=1.0, to=50.0, step_size=0.5, wrap=True,
        justify="center", placeholder_text="Click Me", command=on_spinbox_value_changed,
        width=180, height=34
    )
    spinbox.pack(pady=10)

    # 3. MOUNT: Properties Panel Card Layout Grid Frame
    control_frame = sCTkFrame(dashboard_panel, fg_color=("#E2E8F0", "#262626"), corner_radius=6)
    control_frame.pack(fill="both", expand=True, padx=5, pady=10)
    control_frame.grid_columnconfigure(0, weight=1)
    control_frame.grid_columnconfigure(1, weight=1)

    # --- Row 0: Component Interactive Input State Controller ---
    lbl_state = sCTkLabelSecondary(control_frame, text="Component State:", font=("Arial", 11, "bold"))
    lbl_state.grid(row=0, column=0, padx=15, pady=5, sticky="w")
    state_dropdown = ctk.CTkComboBox(control_frame, values=["Normal State (Active)", "Disabled State (Locked)"], command=lambda choice: spinbox.configure(state="disabled" if "Disabled" in choice else "normal"), width=170)
    state_dropdown.grid(row=0, column=1, padx=15, pady=5, sticky="e")
    state_dropdown.set("Normal State (Active)")

    # --- Row 1: Internal Input Content Arrangement Alignment ---
    lbl_justify = sCTkLabelSecondary(control_frame, text="Text Alignment (Justify):", font=("Arial", 11, "bold"))
    lbl_justify.grid(row=1, column=0, padx=15, pady=5, sticky="w")
    justify_dropdown = ctk.CTkComboBox(control_frame, values=["Center", "Left", "Right"], command=lambda choice: spinbox.configure(justify=choice.lower()), width=170)
    justify_dropdown.grid(row=1, column=1, padx=15, pady=5, sticky="e")
    justify_dropdown.set("Center")

    # --- Row 2: Live Masking Format String Controller ---
    lbl_format = sCTkLabelSecondary(control_frame, text="Masking Format Pattern:", font=("Arial", 11, "bold"))
    lbl_format.grid(row=2, column=0, padx=15, pady=5, sticky="w")
    format_dropdown = ctk.CTkComboBox(control_frame, values=["None (Default)", "%.1f kHz", "{:.2f}", "{:.3f}"], command=lambda choice: spinbox.configure(format={"%.1f kHz": "%.1f kHz", "{:.2f}": "{:.2f}", "{:.3f}": "{:.3f}", "None (Default)": ""}.get(choice, "")), width=170)
    format_dropdown.grid(row=2, column=1, padx=15, pady=5, sticky="e")
    format_dropdown.set("None (Default)")

    # --- Row 3: Mechanical Boundary Iteration Loop Wrap ---
    lbl_wrap = sCTkLabelSecondary(control_frame, text="Boundary Iteration Wrap:", font=("Arial", 11, "bold"))
    lbl_wrap.grid(row=3, column=0, padx=15, pady=5, sticky="w")
    wrap_dropdown = ctk.CTkComboBox(control_frame, values=["True (Loop Enabled)", "False (Hard Limits)"], command=lambda choice: spinbox.configure(wrap=True if "True" in choice else False), width=170)
    wrap_dropdown.grid(row=3, column=1, padx=15, pady=5, sticky="e")
    wrap_dropdown.set("True (Loop Enabled)")

    # --- Row 4: String Array Mode vs Numerical Toggle Track ---
    lbl_mode = sCTkLabelSecondary(control_frame, text="Data Array Input Mode:", font=("Arial", 11, "bold"))
    lbl_mode.grid(row=4, column=0, padx=15, pady=5, sticky="w")
    def on_mode_changed(choice):
        if "Discrete List" in choice: spinbox.set_values(txt_custom_values.get())
        else: spinbox.set_values([]); spinbox.set(5.0)
    mode_dropdown = ctk.CTkComboBox(control_frame, values=["Numerical Mode (1.0 - 50.0)", "Discrete List Mode (Strings)"], command=on_mode_changed, width=170)
    mode_dropdown.grid(row=4, column=1, padx=15, pady=5, sticky="e")
    mode_dropdown.set("Numerical Mode (1.0 - 50.0)")

    # --- Row 5: Dynamic Custom String Input Loader Fields ---
    lbl_custom_vals = sCTkLabelSecondary(control_frame, text="List Strings Configuration:", font=("Arial", 11, "bold"))
    lbl_custom_vals.grid(row=5, column=0, padx=15, pady=5, sticky="w")
    def sync_live_text_array(event=None):
        if "Discrete List" in mode_dropdown.get(): spinbox.set_values(txt_custom_values.get())
    txt_custom_values = sCTkEntryPrimary(control_frame, width=170, height=28, placeholder_text="Item1 'Item Two' Item3...")
    txt_custom_values.grid(row=5, column=1, padx=15, pady=5, sticky="e")
    txt_custom_values.insert(0, 'Slow Normal Fast "Turbo Speed" Max')
    txt_custom_values.bind("<Return>", sync_live_text_array); txt_custom_values.bind("<FocusOut>", sync_live_text_array)

    # --- Row 6: Hardware Alignment Placement Side ---
    lbl_side = sCTkLabelSecondary(control_frame, text="Hardware Button Side:", font=("Arial", 11, "bold"))
    lbl_side.grid(row=6, column=0, padx=15, pady=5, sticky="w")
    side_dropdown = ctk.CTkComboBox(control_frame, values=["Right", "Left", "Split"], command=lambda choice: spinbox.configure(button_side=choice.lower()), width=170)
    side_dropdown.grid(row=6, column=1, padx=15, pady=5, sticky="e")
    side_dropdown.set("Right")

    # --- Row 7: Structural Layout Orientation ---
    lbl_orient = sCTkLabelSecondary(control_frame, text="Control Grid Orientation:", font=("Arial", 11, "bold"))
    lbl_orient.grid(row=7, column=0, padx=15, pady=5, sticky="w")
    orient_dropdown = ctk.CTkComboBox(control_frame, values=["Vertical", "Horizontal"], command=lambda choice: spinbox.configure(orientation=choice.lower()), width=170)
    orient_dropdown.grid(row=7, column=1, padx=15, pady=5, sticky="e")
    orient_dropdown.set("Vertical")

    # --- Row 8: Dynamic Arrow Character Font Scaler Track (Fixed Python 3.14 slice tokens) ---
    lbl_arrow_size = sCTkLabelSecondary(control_frame, text="Arrow Glyphs Font Size:", font=("Arial", 11, "bold"))
    lbl_arrow_size.grid(row=8, column=0, padx=15, pady=5, sticky="w")
    arrow_size_dropdown = ctk.CTkComboBox(control_frame, values=["8 pt (Default)", "11 pt (Medium)", "14 pt (Large)", "18 pt"], command=lambda choice: spinbox.configure(arrow_font_size=int(choice.split()[0])), width=170)
    arrow_size_dropdown.grid(row=8, column=1, padx=15, pady=5, sticky="e")
    arrow_size_dropdown.set("8 pt (Default)")

    # 4. Live Visual Theme Workspace Repaint Trigger Switch
    theme_btn = sCTkButtonPrimary(app, text="Toggle UI Light/Dark Appearance", command=lambda: ctk.set_appearance_mode("Light" if ctk.get_appearance_mode() == "Dark" else "Dark"))
    theme_btn.pack(pady=10)

    # 5. Delayed canvas redraw event pass right at the end of the constructor lifecycle
    def force_boot_placeholder_paint():
        if hasattr(spinbox, "entry") and spinbox.entry.winfo_exists() and hasattr(spinbox.entry, "_update"):
            spinbox.entry._update()
    app.after(10, force_boot_placeholder_paint)

    app.mainloop()
