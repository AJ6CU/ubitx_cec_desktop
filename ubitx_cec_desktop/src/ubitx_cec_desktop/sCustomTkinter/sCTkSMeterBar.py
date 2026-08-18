import math
import customtkinter as ctk

# Direct framework path module and theme dictionary registry imports
from sCTkFrame import sCTkFrame
from ThemeableWidget import ThemeableWidget
from sCTkThemes import THEME_DEFAULTS


class sCTkSMeterBar(sCTkFrame, ThemeableWidget):
    """
    A standalone, low-profile horizontal discrete LED segment bar widget displaying
    simultaneous, independent tracks for incoming S-Units and transmitter SWR ratio levels.
    Inherits geometry patterns from sCTkFrame and style definitions from ThemeableWidget.
    Supports complete runtime visibility toggles and fading states for lower instrument clusters.
    """

    def __init__(self, master=None, sig_min_value=0, sig_max_value=60, swr_max_value=5.0,
                 swr_visible=True, pwr_visible=True, hide_lower_row=False, width=340, height=110, **kw):
        theme_defaults = THEME_DEFAULTS["sCTkSMeterBar"]

        # 1. Initialize Themeable mixin safely to assemble self.final_kw and attributes
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # 2. Map standard compatible configuration fields from registry records
        theme_bg_raw = theme_defaults.get("fg_color", ("#FFFFFF", "#0A0A0A"))

        # 3. Clean custom variables out of the keyword dictionary to shield the frame layer
        self.final_kw.pop("fg_color", None)
        self.final_kw.pop("text_color", None)
        self.final_kw.pop("alarm_color", None)
        self.final_kw.pop("led_on_color", None)
        self.final_kw.pop("led_off_color", None)

        # 4. Construct the custom base frame using raw configuration mappings
        super().__init__(master, width=width, height=height, fg_color=theme_bg_raw, **self.final_kw)

        # Prefixed scaling boundary constraints assignment variables
        self.sig_min_value = float(sig_min_value)
        self.sig_max_value = float(sig_max_value)
        self.swr_max_value = float(swr_max_value)

        #  Capture default values
        import inspect
        sig = inspect.signature(self.__init__)
        self._default_sig_min_value = sig.parameters['sig_min_value'].default
        self._default_sig_max_value = sig.parameters['sig_max_value'].default
        self._default_swr_max_value = sig.parameters['swr_max_value'].default
        self._default_swr_visible = bool(sig.parameters['swr_visible'].default)
        self._default_pwr_visible = bool(sig.parameters['pwr_visible'].default)
        self._default_hide_lower_row = bool(sig.parameters['hide_lower_row'].default)
        self._default_width = sig.parameters['width'].default
        self._default_height = sig.parameters['height'].default

        # Dynamic visibility state parameters
        self._swr_visible = bool(swr_visible)
        self._pwr_visible = bool(pwr_visible)
        self._hide_lower_row = bool(hide_lower_row)

        # Independent live telemetry storage parameters
        self._current_s_value = self.sig_min_value
        self._current_swr_value = 1.0
        self._current_pwr_value = 0.0

        # S-Meter Arc Configuration (Angles in degrees for Tkinter canvas)
        self.start_angle = 50
        self.extent_angle = 80

        # 5. Explicitly pass 'self' into instance method references to translate canvas backgrounds
        bg_resolved_string = ThemeableWidget._resolve_color(self, theme_bg_raw)

        self.canvas = ctk.CTkCanvas(self, highlightthickness=0, bd=0, bg=bg_resolved_string)
        self.canvas.pack(fill="both", expand=True, padx=0, pady=0)

        # Prevent layout shrinkage if nested loosely
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.canvas.bind("<Configure>", lambda e: self._draw_meter())

    def _set_appearance_mode(self, mode_string):
        """
        Intercept CustomTkinter global theme change events to force the underlying
        canvas background to adapt while locking down visual gauge scale parameters.
        """
        super()._set_appearance_mode(mode_string)

        if hasattr(self, "canvas") and self.canvas.winfo_exists():
            self.after(10, self._update_theme_colors)

    def _update_theme_colors(self):
        """Wipes and paint fresh layout parameters using locked device accents."""
        theme_map = THEME_DEFAULTS["sCTkSMeterBar"]
        bg_color = self._resolve_color(theme_map.get("fg_color"))
        self.canvas.configure(bg=bg_color)
        self._draw_meter()

    def configure_visibility(self, swr_visible=None, pwr_visible=None, hide_lower_row=None):
        """Public configuration mapping hook to alter the lower row layout matrix states live."""
        if swr_visible is not None:
            self._swr_visible = bool(swr_visible)
        if pwr_visible is not None:
            self._pwr_visible = bool(pwr_visible)
        if hide_lower_row is not None:
            self._hide_lower_row = bool(hide_lower_row)

        if self.canvas.winfo_exists():
            self._draw_meter()

    # =====================================================================
    # CONFIGURATION ROUTER AND POP-GUARD INTERCEPTS
    # =====================================================================
    def configure(self, *args, **kwargs):
        # 1. POSITIONAL INTERCEPT LOOP: Satisfies Pygubu's unset_property() default value queries
        if args and len(args) == 1:
            pname = args[0]  # Read the single string property name

            # Map standard frame properties safely
            if pname == "width":
                return ('width', 'width', 'Width', self._default_width, self.cget("width"))
            if pname == "height":
                return ('height', 'height', 'Height', self._default_height, self.cget("height"))
            # if pname == "state":
            #     return ('state', 'state', 'State', 'normal', getattr(self, "_state", "normal"))

            # Map every custom specialized parameter to return a safe baseline tuple
            if pname in ["sig_max_value", "sig_min_value", "swr_max_value"]:
                val = getattr(self, f"{pname}", "")
                return (pname, pname, pname, "", val)

            return super().configure(*args, **kwargs)

        # 2. STANDARD GEOMETRY SANITIZATION: Catch empty properties deletions live
        if "width" in kwargs:
            w = kwargs["width"]
            kwargs["width"] = int(w) if (w and str(w).strip()) else self._default_width
        if "height" in kwargs:
            h = kwargs["height"]
            kwargs["height"] = int(h) if (h and str(h).strip()) else self._default_height

        # 3. OPERATIONAL STATE SANITIZATION: Clean standard operational states safely
        # if "state" in kwargs:
        #     st = kwargs.pop("state")
        #     self._state = str(st).strip().lower() if (st and str(st).strip()) else "normal"

        """Public configuration modifier mapping live updates directly into active variables."""
        if "sig_min_value" in kwargs or "from_" in kwargs:
            # 1. Safely extract the raw string value out of the dictionary tree
            val = kwargs.pop("sig_min_value", kwargs.pop("from_", None))

            # 2. Check if the field was completely erased/deleted in the panel
            if val == "" or (val is not None and not str(val).strip()):
                self.sig_min_value = self._default_sig_min_value
            elif val is not None:
                # Only execute float conversion if we have verified a valid numeric text string!
                self.sig_min_value = float(val)

            # # AUTOMATIC CEILING ALIGNMENT RULE:
            # # If the new min overlaps or matches the existing max, force min to below max!
            # if self.sig_min_value >= self.sig_max_value:
            #     self.sig_min_value = self.sig_max_value - 1

        if "sig_max_value" in kwargs or "to" in kwargs:
            # 1. Safely extract the raw string value out of the dictionary tree
            val = kwargs.pop("sig_max_value", kwargs.pop("to", None))

            # 2. Check if the field was completely erased/deleted in the panel
            if val == "" or (val is not None and not str(val).strip()):
                self.sig_max_value = self._default_sig_max_value
            elif val is not None:
                # Only execute float conversion if we have verified a valid numeric text string!
                self.sig_max_value = float(val)


        if "swr_max_value" in kwargs:
            # 1. Safely extract the raw string value out of the dictionary tree
            val = kwargs.pop("swr_max_value")

            # 2. Check if the field was completely erased/deleted in the panel
            if val == "" or (val is not None and not str(val).strip()):
                self.swr_max_value = self._default_swr_max_value
            elif val is not None:
                # Only execute float conversion if we have verified a valid numeric text string!
                self.swr_max_value = float(val)


        if "swr_visible" in kwargs:
            # 1. Safely extract the raw string value out of the dictionary tree
            val = kwargs.pop("swr_visible")

            # 2. Check if the field was completely erased/deleted in the panel
            if val == "" or (val is not None and not str(val).strip()):
                self._swr_visible = self._default_swr_visible
            elif val is not None:
                # Only execute string conversion if we have verified a valid numeric text string!
                self._swr_visible = bool(val)

        if "pwr_visible" in kwargs:
            # 1. Safely extract the raw string value out of the dictionary tree
            val = kwargs.pop("pwr_visible")

            # 2. Check if the field was completely erased/deleted in the panel
            if val == "" or (val is not None and not str(val).strip()):
                self._pwr_visible = self._default_pwr_visible
            elif val is not None:
                # Only execute string conversion if we have verified a valid numeric text string!
                self._pwr_visible = bool(val)

        if "hide_lower_row" in kwargs:
            # 1. Safely extract the raw string value out of the dictionary tree
            val = kwargs.pop("hide_lower_row")

            # 2. Check if the field was completely erased/deleted in the panel
            if val == "" or (val is not None and not str(val).strip()):
                self._hide_lower_row = self._default_hide_lower_row
            elif val is not None:
                # Only execute string conversion if we have verified a valid numeric text string!
                self._hide_lower_row = bool(val)

        super().configure(**kwargs)
        if self.canvas.winfo_exists():
            self._draw_meter()

    def cget(self, attribute_name):
        """Public register parameter property getter lookup."""
        if attribute_name in ["sig_min_value", "from_"]: return self.sig_min_value
        if attribute_name in ["sig_max_value", "to"]: return self.sig_max_value
        if attribute_name == "swr_max_value": return self.swr_max_value
        if attribute_name == "swr_visible": return self._swr_visible
        if attribute_name == "pwr_visible": return self._pwr_visible
        if attribute_name == "hide_lower_row": return self._hide_lower_row
        return super().cget(attribute_name)

    def _draw_meter(self):
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 10 or height < 10:
            return

        theme_map = THEME_DEFAULTS["sCTkSMeterBar"]
        bg_color = self._resolve_color(theme_map.get("fg_color"))
        amber_color = self._resolve_color(theme_map.get("text_color"))
        red_color = self._resolve_color(theme_map.get("alarm_color"))
        led_on_color = self._resolve_color(theme_map.get("led_on_color"))
        led_off_color = self._resolve_color(theme_map.get("led_off_color"))

        # Muted disabled palette color string profile
        disabled_faded_color = ("#94A3B8", "#334155")
        disabled_color = self._resolve_color(disabled_faded_color)

        self.canvas.configure(bg=bg_color)

        # Horizontal layout boundaries
        start_x = 42
        end_x = width - 42
        total_length = end_x - start_x

        if self._hide_lower_row:
            sig_y = int(height * 0.50)
        else:
            sig_y = int(height * 0.28)

        lower_y = int(height * 0.70)

        num_led_segments = 30
        segment_width = (total_length / num_led_segments) - 1.5

        # -----------------------------------------------------------------
        # 1. GENERATE SIG TRACK LED DISPLAY MATRIX
        # -----------------------------------------------------------------
        sig_range = self.sig_max_value - self.sig_min_value
        s_fraction = (max(self.sig_min_value, min(self.sig_max_value,
                                                  self._current_s_value)) - self.sig_min_value) / sig_range if sig_range != 0 else 0.0
        active_sig_segments = int(num_led_segments * s_fraction)

        for i in range(num_led_segments):
            seg_start_x = start_x + (i * (total_length / num_led_segments))
            seg_end_x = seg_start_x + segment_width
            is_sig_redzone = i >= int(num_led_segments * 0.60)

            if i < active_sig_segments:
                fill_color = red_color if is_sig_redzone else led_on_color
            else:
                fill_color = led_off_color

            self.canvas.create_rectangle(seg_start_x, sig_y - 4, seg_end_x, sig_y + 1, fill=fill_color, outline="")

        # -----------------------------------------------------------------
        # FIXED: DYNAMIC TICK GEOMETRY & MATH-DRIVEN SCALE LABELS
        # Discards static text arrays, generating scale labels relative to min/max
        # -----------------------------------------------------------------
        sig_ticks = [0.0, 0.13, 0.26, 0.40, 0.53, 0.66, 0.80, 1.0]

        for tick_idx, pct in enumerate(sig_ticks):
            tx = start_x + (total_length * pct)
            color = red_color if pct >= 0.53 else amber_color
            self.canvas.create_line(tx, sig_y, tx, sig_y - 6, fill=color, width=1)

            # Compute actual numerical scale values dynamically at each fraction tick step
            calculated_value = self.sig_min_value + (sig_range * pct)

            # Formats first label to "S [val]", mid labels to rounded floats, and end label to "[val]dB"
            if tick_idx == 0:
                label_str = f"S{int(round(calculated_value))}"
            elif tick_idx == len(sig_ticks) - 1:
                label_str = f"{int(round(calculated_value))}dB"
            else:
                label_str = f"{calculated_value:.1f}".rstrip('0').rstrip('.')

            text_offset_y = sig_y - 14
            self.canvas.create_text(tx, text_offset_y, text=label_str, fill=color, font=("Arial", 9, "bold"),
                                    anchor="center")

        # "SIG" label centered directly in the middle of its track layout
        sig_mid_x = start_x + (total_length * 0.5)
        self.canvas.create_text(sig_mid_x, sig_y + 6, text="SIG", fill=amber_color, font=("Arial", 10, "bold"),
                                anchor="n")

        if self._hide_lower_row:
            return

        # -----------------------------------------------------------------
        # 2. GENERATE SPLIT LOWER ROW TRACK (LEFT: SWR | RIGHT: RF POWER)
        # -----------------------------------------------------------------
        mid_gap_start = 13
        mid_gap_end = 17

        def get_swr_fraction(swr_val):
            if swr_val <= 1.0: return 0.0
            if swr_val >= self.swr_max_value: return 1.0

            log_min = math.log10(1.0 + 0.5)
            log_max = math.log10(self.swr_max_value + 0.5)
            log_val = math.log10(swr_val + 0.5)

            return (log_val - log_min) / (log_max - log_min)

        active_swr_segments = int(mid_gap_start * get_swr_fraction(self._current_swr_value))

        pwr_fraction = max(0.0, min(100.0, self._current_pwr_value)) / 100.0
        pwr_total_segments = num_led_segments - mid_gap_end
        active_pwr_segments = int(pwr_total_segments * pwr_fraction)

        for i in range(num_led_segments):
            seg_start_x = start_x + (i * (total_length / num_led_segments))
            seg_end_x = seg_start_x + segment_width

            if mid_gap_start <= i < mid_gap_end:
                fill_color = bg_color

            elif i < mid_gap_start:
                left_pct = i / mid_gap_start
                if left_pct >= get_swr_fraction(2.0):
                    is_swr_redzone = True
                else:
                    is_swr_redzone = False

                if i < active_swr_segments and self._swr_visible:
                    fill_color = red_color if is_swr_redzone else led_on_color
                else:
                    fill_color = led_off_color

            else:
                pwr_index = i - mid_gap_end
                is_pwr_redzone = pwr_index >= int(pwr_total_segments * 0.8)
                if pwr_index < active_pwr_segments and self._pwr_visible:
                    fill_color = red_color if is_pwr_redzone else led_on_color
                else:
                    fill_color = led_off_color

            self.canvas.create_rectangle(seg_start_x, lower_y - 4, seg_end_x, lower_y + 1, fill=fill_color, outline="")

        swr_label_color = amber_color if self._swr_visible else disabled_color
        pwr_label_color = amber_color if self._pwr_visible else disabled_color

        swr_length_fraction = mid_gap_start / num_led_segments
        swr_mid_x = start_x + (total_length * (swr_length_fraction * 0.5))
        self.canvas.create_text(swr_mid_x, lower_y - 20, text="SWR", fill=swr_label_color, font=("Arial", 10, "bold"),
                                anchor="n")

        pwr_start_fraction = mid_gap_end / num_led_segments
        pwr_length_fraction = 1.0 - pwr_start_fraction
        pwr_mid_x = start_x + (total_length * (pwr_start_fraction + (pwr_length_fraction * 0.5)))
        self.canvas.create_text(pwr_mid_x, lower_y - 20, text="PWR", fill=pwr_label_color, font=("Arial", 10, "bold"),
                                anchor="n")

        swr_ticks = [1.0, 1.5, 2.0]
        if self.swr_max_value > 2.0:
            step = (self.swr_max_value - 2.0) / 2.0
            swr_ticks.append(round(2.0 + step, 1))
            swr_ticks.append(round(self.swr_max_value, 1))

        for val in swr_ticks:
            fraction = get_swr_fraction(val) * swr_length_fraction
            tx = start_x + (total_length * fraction)

            if self._swr_visible:
                color = red_color if val >= 2.0 else amber_color
            else:
                color = disabled_color

            label_str = str(int(val)) if val.is_integer() else str(val)
            if val == self.swr_max_value:
                label_str += "+"

            self.canvas.create_line(tx, lower_y, tx, lower_y + 6, fill=color, width=1)
            self.canvas.create_text(tx, lower_y + 12, text=label_str, fill=color, font=("Arial", 9, "bold"), anchor="n")

        pwr_ticks = [(0, "0"), (50, "50"), (100, "100%")]

        for val, label in pwr_ticks:
            fraction = pwr_start_fraction + ((val / 100.0) * pwr_length_fraction)
            tx = start_x + (total_length * fraction)

            if self._pwr_visible:
                color = red_color if val >= 80 else amber_color
            else:
                color = disabled_color

            self.canvas.create_line(tx, lower_y, tx, lower_y + 6, fill=color, width=1)

            if val == 100:
                self.canvas.create_text(tx - 4, lower_y + 12, text=label, fill=color, font=("Arial", 9, "bold"),
                                        anchor="n")
            else:
                self.canvas.create_text(tx, lower_y + 12, text=label, fill=color, font=("Arial", 9, "bold"), anchor="n")

    def set(self, s_value=None, swr_value=None, pwr_value=None):
        """Update any telemetry channel row independently."""
        if s_value is not None:
            self._current_s_value = float(s_value)
        if swr_value is not None:
            self._current_swr_value = float(swr_value)
        if pwr_value is not None:
            self._current_pwr_value = float(pwr_value)

        if self.canvas.winfo_exists():
            self._draw_meter()


import random
import customtkinter as ctk


# Cross-module import reference tracking your standalone LED component file
# from sCTkSMeterBar import sCTkSMeterBar

class HarnessSimulator:
    def __init__(self, master_root, bar_meter):
        self.root = master_root
        self.bar_meter = bar_meter

        # 1. Receiver Track Physics: Horizontal LED Bar (Signal line)
        self.bar_sig_target = 4.0
        self.bar_sig_current = 0.0
        self.bar_sig_inertia = 0.35  # Snappy audio-level envelope reaction tracking

        # 2. Transmitter Track Physics: Split Lower Row (SWR & Forward Power)
        self.swr_target = 1.0
        self.pwr_target = 0.0
        self.swr_current = 1.0
        self.pwr_current = 0.0
        self.tx_inertia = 0.20  # Damped lag profile for keying animations
        self.tx_active = False  # PTT (Push-To-Talk) transmission flag

    def slow_vfo_tuning_cycle(self):
        """Simulates scrolling across frequencies to hit dynamic station thresholds."""
        # Shift the target level for the receiver bar track independently
        self.bar_sig_target = random.uniform(0.5, 13.5)

        # Periodically trigger an active PTT Tx broadcast block cycle
        if not self.tx_active and random.random() > 0.4:
            self.tx_active = True
            # Transmitting keys down forward power and standing wave targets simultaneously
            self.swr_target = random.uniform(1.1, 4.5)  # Simulated reflection mismatch match
            self.pwr_target = random.uniform(35.0, 95.0)  # Forward RF power output percentage

            # Key down lock carrier duration (1.5 to 3 seconds)
            self.root.after(random.randint(1500, 3000), self._release_ptt)

        self.root.after(random.randint(4000, 8000), self.slow_vfo_tuning_cycle)

    def _release_ptt(self):
        """Releases the PTT line, dropping transmitter telemetry values back to un-keyed baselines."""
        self.tx_active = False
        self.swr_target = 1.0  # No reflection when un-keyed
        self.pwr_target = 0.0  # Zero forward carrier output when un-keyed

    def process_fast_physics_tick(self):
        """High-speed 50 FPS animation thread executing real-time fading noise jitter updates."""
        # A. Animate Horizontal LED Bar (Signal Track)
        bar_jitter = random.uniform(-1.2, 1.2)
        bar_live = max(0.0, min(15.0, self.bar_sig_target + bar_jitter))
        self.bar_sig_current += (bar_live - self.bar_sig_current) * self.bar_sig_inertia

        # B. Animate Horizontal Split Transmitter Tracks (SWR & Power lines)
        swr_jitter = random.uniform(-0.15, 0.15) if self.tx_active else 0.0
        pwr_jitter = random.uniform(-2.5, 2.5) if self.tx_active else 0.0

        swr_live = max(1.0, min(5.0, self.swr_target + swr_jitter))
        pwr_live = max(0.0, min(100.0, self.pwr_target + pwr_jitter))

        self.swr_current += (swr_live - self.swr_current) * self.tx_inertia
        self.pwr_current += (pwr_live - self.pwr_current) * self.tx_inertia

        # Push the unified variables down to your standalone bar widget instance registers
        self.bar_meter.set(s_value=self.bar_sig_current, swr_value=self.swr_current, pwr_value=self.pwr_current)

        # Loop the animation clock frame step precisely every 20 milliseconds
        self.root.after(20, self.process_fast_physics_tick)


# =====================================================================
# SYSTEM ASSEMBLY TEST BENCH RUNNER
# =====================================================================
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("sCTk Bar Instrument Test Harness")
    app.geometry("440x240")
    app.configure(fg_color=("#F1F5F9", "#1C1C1C"))  # High-contrast light / workbench dark mode

    # Create a simple frame canvas chassis panel anchor layout
    panel_container = ctk.CTkFrame(app, fg_color="transparent", border_width=0)
    panel_container.pack(padx=20, pady=15, fill="both", expand=True)

    # Mount Core Piece: The Custom Horizontal LED Bar Segment S/SWR/PWR-Meter
    led_bar_gauge = sCTkSMeterBar(panel_container, width=340, height=110)
    led_bar_gauge.pack(pady=15)


    # Add an on-the-fly theme switcher button to check color inversion states live
    def toggle_theme():
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")


    theme_btn = ctk.CTkButton(app, text="Toggle Light/Dark Theme", command=toggle_theme)
    theme_btn.pack(pady=5)

    # Fire up background simulation threads passing the bar widget instance cleanly
    simulator = HarnessSimulator(app, led_bar_gauge)
    simulator.process_fast_physics_tick()
    simulator.slow_vfo_tuning_cycle()

    # Fade out SWR scale elements entirely while keeping Power active
    # led_bar_gauge.configure_visibility(swr_visible=False, pwr_visible=False)
    #
    # Remove the entire bottom row cleanly from the screen panel asset
    led_bar_gauge.configure_visibility(hide_lower_row=False)

    #
    app.mainloop()

