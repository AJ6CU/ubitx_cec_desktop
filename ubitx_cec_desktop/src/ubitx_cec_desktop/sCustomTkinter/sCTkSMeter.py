import math
import customtkinter as ctk

# Direct framework path module and theme dictionary registry imports
from sCTkFrame import sCTkFrame
from ThemeableWidget import ThemeableWidget
from sCTkThemes import THEME_DEFAULTS


class sCTkSMeter(sCTkFrame, ThemeableWidget):
    """
    A standalone, high-fidelity dual-scale analog signal and power output instrument widget.
    Inherits geometry patterns from sCTkFrame and style definitions from ThemeableWidget.
    Supports fixed explicit hardware width and height constraint arguments.
    """

    def __init__(self, master=None, sig_min_value=0, sig_max_value=60, width=340, height=130, **kw):
        theme_defaults = THEME_DEFAULTS["sCTkSMeter"]

        # 1. Initialize Themeable mixin safely to assemble self.final_kw and attributes
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # 2. Map standard compatible configuration fields from registry records
        theme_bg_raw = theme_defaults.get("fg_color", ("#111827", "#0A0A0A"))

        # 3. Clean custom variables out of the keyword dictionary to shield the frame layer
        self.final_kw.pop("fg_color", None)
        self.final_kw.pop("text_color", None)
        self.final_kw.pop("alarm_color", None)
        self.final_kw.pop("needle_color", None)

        # 4. Pass the custom width and height parameters directly down to the frame core.
        super().__init__(master, width=width, height=height, fg_color=theme_bg_raw, **self.final_kw)

        # FIXED: Updated parameters to follow prefixed naming patterns natively
        self.sig_min_value = float(sig_min_value)
        self.sig_max_value = float(sig_max_value)
        self._current_value = self.sig_min_value

        # Exact mathematical arc bounds to match the layout curve signature perfectly
        self.start_angle = 38
        self.extent_angle = 104

        # 5. Explicitly pass 'self' into instance method references to translate canvas backgrounds
        bg_resolved_string = ThemeableWidget._resolve_color(self, theme_bg_raw)

        self.canvas = ctk.CTkCanvas(self, highlightthickness=0, bd=0, bg=bg_resolved_string)
        self.canvas.pack(fill="both", expand=True, padx=0, pady=0)

        # 6. Prevent layout shrinkage if nested loosely
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.canvas.bind("<Configure>", lambda e: self._draw_meter())

    # =====================================================================
    # FIXED: ADDED AUTOCLAMP DEFAULT SCALING FALLBACK HOOKS
    # Dynamically forces omitted max parameters back to standard values
    # if alignment thresholds are breached during live reconfigurations!
    # =====================================================================
    def configure(self, **kwargs):
        """Public unified frame layout configuration and parameter update modifiers."""
        # 1. Pop parameters out safely to shield CustomTkinter
        if "sig_min_value" in kwargs or "from_" in kwargs:
            val = kwargs.pop("sig_min_value", kwargs.pop("from_", None))
            self.sig_min_value = float(val)

            # AUTOMATIC CEILING ALIGNMENT RULE:
            # If the new min overlaps or matches the existing max, force max to default back to 60.0!
            if self.sig_min_value >= self.sig_max_value:
                self.sig_max_value = 60.0

        if "sig_max_value" in kwargs or "to" in kwargs:
            val = kwargs.pop("sig_max_value", kwargs.pop("to", None))
            self.sig_max_value = float(val)

        # 2. Pass sanitized geometry tokens down to CustomTkinter core layers
        super().configure(**kwargs)

        # 3. Force instant, adaptive structural repaint
        if self.canvas.winfo_exists():
            self._draw_meter()

    def cget(self, attribute_name):
        """Public operational register attribute getter lookups."""
        if attribute_name in ["sig_min_value", "from_"]:
            return self.sig_min_value
        if attribute_name in ["sig_max_value", "to"]:
            return self.sig_max_value
        return super().cget(attribute_name)

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
        theme_map = THEME_DEFAULTS["sCTkSMeter"]
        bg_color = self._resolve_color(theme_map.get("fg_color"))
        self.canvas.configure(bg=bg_color)
        self._draw_meter()

    def _draw_meter(self):
        """Draws the complete S-Meter, including arcs, labels, and ticks."""
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 10 or height < 10: return

        theme = THEME_DEFAULTS["sCTkSMeter"]
        bg, amber, red = self._resolve_color(theme.get("fg_color")), \
            self._resolve_color(theme.get("text_color", ("#FF9100", "#FF9100"))), \
            self._resolve_color(theme.get("alarm_color", ("#FF2200", "#FF2200")))
        self.canvas.configure(bg=bg)
        font = theme.get("font", ("Arial", 10, "bold"))

        radius_sig = min(width * 0.52, height * 1.20)
        center_x, center_y = width * 0.44, height * 0.35 + radius_sig
        radius_po = radius_sig - 16

        # Draw Labels and Arcs
        self.canvas.create_text(center_x, height * 0.12, text="SIGNAL", fill=amber, font=font)
        self.canvas.create_text(center_x, height * 0.80, text="RF OUTPUT", fill=amber, font=font)

        total = self.sig_max_value - self.sig_min_value or 15.0
        split = max(0.0, min(1.0, (self.sig_min_value + (total * (9.0 / 15.0)) - self.sig_min_value) / total))
        split_ang = self.start_angle + (self.extent_angle * (1.0 - split))
        bbox = (center_x - radius_sig, center_y - radius_sig, center_x + radius_sig, center_y + radius_sig)

        # Red/Amber arcs
        self.canvas.create_arc(bbox, start=split_ang, extent=self.start_angle + self.extent_angle - split_ang,
                               style="arc", outline=amber, width=2)
        self.canvas.create_arc(bbox, start=self.start_angle, extent=split_ang - self.start_angle, style="arc",
                               outline=red, width=2)

        # Ticks
        for i in range(16):
            frac = i / 15.0
            ang = math.radians(self.start_angle + (self.extent_angle * (1.0 - frac)))
            major, is_red = (i in [0, 1, 5, 9, 11, 13, 15]), (frac >= split)
            l = 10 if major else 5
            x1, y1 = center_x + radius_sig * math.cos(ang), center_y - radius_sig * math.sin(ang)
            x2, y2 = center_x + (radius_sig + l) * math.cos(ang), center_y - (radius_sig + l) * math.sin(ang)
            self.canvas.create_line(x1, y1, x2, y2, fill=red if is_red else amber, width=2.5 if major else 1.2)
            if major:
                val = self.sig_min_value + (total * frac)
                label = f"{int(round(val))}"
                if i == 0:
                    label = f"S {label}"
                elif i == 15:
                    label = f"{val:.1f} dB"
                self.canvas.create_text(center_x + (radius_sig + (32 if i == 15 else 16)) * math.cos(ang),
                                        center_y - (radius_sig + (32 if i == 15 else 16)) * math.sin(ang),
                                        text=label, fill=red if is_red else amber, font=font)

        self._draw_needle(center_x, center_y, radius_sig)

    def _draw_needle(self, cx, cy, rad):
        """Draws the needle at the calculated angle based on current value."""
        total = self.sig_max_value - self.sig_min_value or 15.0
        frac = max(0.0, min(1.0, (self._current_value - self.sig_min_value) / total))
        ang = math.radians(self.start_angle + (self.extent_angle * (1.0 - frac)))

        nx, ny = cx + (rad + 2) * math.cos(ang), cy - (rad + 2) * math.sin(ang)
        bx, by = cx + (rad - 60) * math.cos(ang), cy - (rad - 60) * math.sin(ang)
        color = self._resolve_color(THEME_DEFAULTS["sCTkSMeter"].get("needle_color", ("#94A3B8", "#FF9100")))
        self.canvas.delete("needle")
        self.canvas.create_line(bx, by, nx, ny, fill=color, width=2, tags="needle")

    def set(self, value):
        """Update the indicator positions (Expects ranges between sig_min_value and sig_max_value)."""
        self._current_value = max(self.sig_min_value, min(self.sig_max_value, float(value)))
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w > 10 and h > 10:
            rad = min(w * 0.52, h * 1.20)
            self._draw_needle(w * 0.44, h * 0.35 + rad, rad)


import random
import customtkinter as ctk


# Ensure the core component is imported
# from sCTkSMeter import sCTkSMeter

class SignalSimulator:
    def __init__(self, master_root, meter_widget):
        self.root = master_root
        self.meter = meter_widget
        self.target_signal = 6.0
        self.current_needle = 0.0
        self.inertia = 0.22

    def shift_vfo_frequency(self):
        """Simulates turning a VFO tuning dial to dynamic transceiver noise thresholds."""
        self.target_signal = random.uniform(1.5, 14.0)
        self.root.after(random.randint(3500, 7000), self.shift_vfo_frequency)

    def process_physics_loop(self):
        """Generates real-time atmospheric fading (QSB) jitter variations."""
        live_jitter = random.uniform(-0.7, 0.7)
        live_signal = max(0.0, min(15.0, self.target_signal + live_jitter))

        self.current_needle += (live_signal - self.current_needle) * self.inertia
        self.meter.set(self.current_needle)

        self.root.after(20, self.process_physics_loop)


# =====================================================================
# SYSTEM EXECUTION RUNNER
# =====================================================================
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("sCTk Standalone Analog Gauge")
    app.geometry("450x260")
    app.configure(fg_color=("#F1F5F9", "#1C1C1C"))

    # 1. Create a parent frame workspace box to mimic a rig chassis section
    # dashboard_frame = ctk.CTkFrame(app, corner_radius=6, border_width=1)
    dashboard_frame = ctk.CTkFrame(app, fg_color="transparent", border_width=0)
    dashboard_frame.pack(padx=20, pady=20)

    # 2. FIXED: Explicitly pass your targeted width and height constraints right
    # into the sCTkSMeter initialization layout signature call.
    smeter = sCTkSMeter(dashboard_frame, width=340, height=130)
    # smeter = sCTkSMeter(dashboard_frame, width=298, height=114)
    smeter.pack(padx=10, pady=10)


    # 3. Add an on-the-fly theme switcher button to check color inversion states
    def toggle_theme():
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")


    theme_btn = ctk.CTkButton(app, text="Toggle Light/Dark Mode", command=toggle_theme)
    theme_btn.pack(pady=10)

    # 4. Fire up background simulation threads
    simulator = SignalSimulator(app, smeter)
    simulator.process_physics_loop()
    simulator.shift_vfo_frequency()

    app.mainloop()


