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

    def __init__(self, master=None, min_value=0, max_value=15, width=340, height=130, **kw):
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
        # This locks the widget dimensions down uniformly regardless of parent layout states.
        super().__init__(master, width=width, height=height, fg_color=theme_bg_raw, **self.final_kw)

        self.min_value = min_value
        self.max_value = max_value
        self._current_value = min_value

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
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 10 or height < 10:
            return

        theme_map = THEME_DEFAULTS["sCTkSMeter"]
        bg_color = self._resolve_color(theme_map.get("fg_color"))

        # FIXED: Routed variables strictly through your framework's resolve method
        # to ensure light/dark mode tuple formats are translated into clean individual strings.
        amber_color = self._resolve_color(theme_map.get("text_color", ("#FF9100", "#FF9100")))
        red_color = self._resolve_color(theme_map.get("alarm_color", ("#FF2200", "#FF2200")))

        self.canvas.configure(bg=bg_color)

        # Perfect circular radius geometric calculation to prevent parabolic distortions
        radius_sig = min(width * 0.52, height * 1.20)

        # Shift center point significantly left to width * 0.44, pushing the whole
        # physical gauge graphics stack cleanly to the right to clear right-side clipping.
        center_x = width * 0.44

        # Drop center pivot down further to height * 0.35 to pull the track arc
        # lower down on the chassis panel, ensuring total headroom separation from the text.
        center_y = height * 0.35 + radius_sig

        radius_po = radius_sig - 16

        # -----------------------------------------------------------------
        # Panel Title Indicators (RECALIBRATED RF OUTPUT LOWERED)
        # -----------------------------------------------------------------
        self.canvas.create_text(center_x, height * 0.12, text="SIGNAL", fill=amber_color, font=("Arial", 11, "bold"))
        self.canvas.create_text(center_x, height * 0.80, text="RF OUTPUT", fill=amber_color, font=("Arial", 11, "bold"))

        # -----------------------------------------------------------------
        # Upper Track: Signal Strengths (RECALIBRATED REDLINE TRACK SPLIT)
        # -----------------------------------------------------------------
        bbox_sig = (center_x - radius_sig, center_y - radius_sig, center_x + radius_sig, center_y + radius_sig)

        # Pin the angular track split exactly to index position 9 (S9 boundary)
        split_fraction = 9 / 15
        split_angle = self.start_angle + (self.extent_angle * (1 - split_fraction))

        # Segment 1: S to S9 (Dynamic Mode Track)
        self.canvas.create_arc(bbox_sig, start=split_angle, extent=self.start_angle + self.extent_angle - split_angle,
                               style="arc", outline=amber_color, width=2)
        # Segment 2: S9 to +60dB (Dynamic Mode Warning Track)
        self.canvas.create_arc(bbox_sig, start=self.start_angle, extent=split_angle - self.start_angle,
                               style="arc", outline=red_color, width=2)

        upper_ticks = [
            (0, "S", False, False), (1, "1", True, False), (2, "", False, False), (3, "", False, False),
            (4, "", False, False), (5, "5", True, False), (6, "", False, False), (7, "", False, False),
            (8, "", False, False), (9, "9", True, True), (10, "", False, True), (11, "+20", True, True),
            (12, "", False, True), (13, "+40", True, True), (14, "", False, True), (15, "+60dB", True, True)
        ]

        for idx, label, is_major, is_red in upper_ticks:
            fraction = idx / (len(upper_ticks) - 1)
            angle_deg = self.start_angle + (self.extent_angle * (1 - fraction))
            angle_deg_clamped = angle_deg if angle_deg >= 0 else 0
            angle_rad = math.radians(angle_deg_clamped)

            color = red_color if is_red else amber_color
            tick_len = 10 if is_major else 5

            x1 = center_x + radius_sig * math.cos(angle_rad)
            y1 = center_y - radius_sig * math.sin(angle_rad)
            x2 = center_x + (radius_sig + tick_len) * math.cos(angle_rad)
            y2 = center_y - (radius_sig + tick_len) * math.sin(angle_rad)

            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2.5 if is_major else 1.2)

            if label:
                # Custom visual offset rule solely for the final +60dB boundary text block
                if idx == 15:
                    text_radius = radius_sig + 32
                    adjusted_angle_rad = angle_rad - 0.04
                else:
                    text_radius = radius_sig + 16
                    adjusted_angle_rad = angle_rad

                tx = center_x + text_radius * math.cos(adjusted_angle_rad)
                ty = center_y - text_radius * math.sin(adjusted_angle_rad)
                self.canvas.create_text(tx, ty, text=label, fill=color, font=("Arial", 10, "bold"))

        # -----------------------------------------------------------------
        # Lower Track: Power Output Percentages (Po 0% -> 100%)
        # -----------------------------------------------------------------
        bbox_po = (center_x - radius_po, center_y - radius_po, center_x + radius_po, center_y + radius_po)
        self.canvas.create_arc(bbox_po, start=self.start_angle, extent=self.extent_angle, style="arc",
                               outline=amber_color, width=2)

        lower_ticks = [
            (0.0, "Po"), (1.5, "0"), (4.5, "10"), (7.5, "25"),
            (10.5, "50"), (13.5, "100"), (15.0, "%")
        ]

        for idx, label in lower_ticks:
            fraction = idx / 15.0
            angle_deg = self.start_angle + (self.extent_angle * (1 - fraction))
            angle_deg_clamped = angle_deg if angle_deg >= 0 else 0
            angle_rad = math.radians(angle_deg_clamped)

            x1 = center_x + radius_po * math.cos(angle_rad)
            y1 = center_y - radius_po * math.sin(angle_rad)
            x2 = center_x + (radius_po - 6) * math.cos(angle_rad)
            y2 = center_y - (radius_po - 6) * math.sin(angle_rad)

            if label not in ["Po", "%"]:
                self.canvas.create_line(x1, y1, x2, y2, fill=amber_color, width=1.5)

            tx = center_x + (radius_po - 14) * math.cos(angle_rad)
            ty = center_y - (radius_po - 14) * math.sin(angle_rad)
            self.canvas.create_text(tx, ty, text=label, fill=amber_color, font=("Arial", 10, "bold"))

        self._draw_needle(center_x, center_y, radius_sig)

    def _draw_needle(self, center_x, center_y, radius_sig):
        val_range = self.max_value - self.min_value
        fraction = (self._current_value - self.min_value) / val_range if val_range != 0 else 0
        fraction = max(0.0, min(1.0, fraction))

        angle_deg = self.start_angle + (self.extent_angle * (1 - fraction))
        angle_deg_clamped = angle_deg if angle_deg >= 0 else 0
        angle_rad = math.radians(angle_deg_clamped)

        nx = center_x + (radius_sig + 2) * math.cos(angle_rad)
        ny = center_y - (radius_sig + 2) * math.sin(angle_rad)

        bx = center_x + (radius_sig - 60) * math.cos(angle_rad)
        by = center_y - (radius_sig - 60) * math.sin(angle_rad)

        theme_map = THEME_DEFAULTS["sCTkSMeter"]
        needle_color = self._resolve_color(theme_map.get("needle_color", ("#94A3B8", "#FF9100")))

        self.canvas.delete("needle")
        self.canvas.create_line(bx, by, nx, ny, fill=needle_color, width=2, tags="needle")

    def set(self, value):
        """Update the indicator positions (Expects ranges between 0.0 and 15.0)"""
        self._current_value = value
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width > 10 and height > 10:
            radius_sig = min(width * 0.52, height * 1.20)

            # Match the fresh structural coordinate shifts inside position vector tracks
            center_x = width * 0.44
            center_y = height * 0.35 + radius_sig
            self._draw_needle(center_x, center_y, radius_sig)


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


