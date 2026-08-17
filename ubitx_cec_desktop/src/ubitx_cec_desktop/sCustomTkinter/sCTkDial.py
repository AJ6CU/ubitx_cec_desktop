import sys
import math
import time
import customtkinter as ctk
from sCTkFrame import sCTkFrame
from ThemeableWidget import ThemeableWidget
from sCTkThemes import THEME_DEFAULTS


class sCTkDialBase(sCTkFrame, ThemeableWidget):
    """Abstract Base Class for theme-adaptive mechanical rotary encoder widgets."""

    def __init__(self, master=None, divisions=24, state="normal", width=120, height=120, **kw):
        child_classname = self.__class__.__name__
        theme_defaults = THEME_DEFAULTS.get(child_classname, THEME_DEFAULTS["sCTkDial"])
        ThemeableWidget.__init__(self, theme_defaults, kw)

        theme_bg_raw = theme_defaults.get("fg_color")
        self.final_kw.pop("fg_color", None)
        self.final_kw.pop("text_color", None)
        self.final_kw.pop("dial_color", None)
        self.final_kw.pop("shadow_color", None)
        self.final_kw.pop("disabled_text_color", None)
        self.final_kw.pop("disabled_dial_color", None)
        self.final_kw.pop("disabled_dimple_glow", None)
        self.final_kw.pop("pointer_color", None)
        self.final_kw.pop("pointer_glow_color", None)
        self.final_kw.pop("diameter", None)

        target_diameter = kw.get("diameter", None)
        if target_diameter is not None:
            width, height = int(target_diameter), int(target_diameter)

        super().__init__(master, width=width, height=height, fg_color=theme_bg_raw, **self.final_kw)

        self._divisions = int(divisions) if int(divisions) > 0 else 24
        self._state = "normal" if state.lower() == "normal" else "disabled"
        self._current_value = 0
        self._scroll_cooldown_seconds = 0.060
        self._last_scroll_time = 0.0
        self._last_y = 0

        self.canvas = ctk.CTkCanvas(self, highlightthickness=0, bd=0,
                                    bg=ThemeableWidget._resolve_color(self, theme_bg_raw))
        self.canvas.pack(fill="both", expand=True)
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.canvas.bind("<Enter>", lambda e: self._on_mouse_enter())
        self.canvas.bind("<Button-1>", self._on_left_click_step)
        self.canvas.bind("<Button-2>", self._on_right_click_step)
        self.canvas.bind("<Button-3>", self._on_right_click_step)
        self.canvas.bind("<Shift-ButtonPress-1>", self._on_button_press)
        self.canvas.bind("<Shift-B1-Motion>", self._on_button_motion)
        self.canvas.bind("<Configure>", lambda e: self._draw_dial_base())
        self.after(50, self._inject_private_layer_bindings)

    def _inject_private_layer_bindings(self):
        layers_to_bind = [self.canvas, self]
        if hasattr(self, "_canvas") and self._canvas is not None: layers_to_bind.append(self._canvas)
        for target_layer in layers_to_bind:
            if sys.platform == "darwin": target_layer.bind("<TouchpadScroll>", self._process_mac_touchpad_scroll,
                                                           add="+")
            target_layer.bind("<MouseWheel>", self._process_scroll_wheel, add="+")
            target_layer.bind("<Button-4>", self._process_scroll_wheel, add="+")
            target_layer.bind("<Button-5>", self._process_scroll_wheel, add="+")

    def _on_mouse_enter(self):
        if self._state == "normal": self.canvas.focus_set()

    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)
        if hasattr(self, "canvas") and self.canvas.winfo_exists(): self.after(20, self._process_theme_repaint)

    def _process_theme_repaint(self):
        theme_map = THEME_DEFAULTS.get(self.__class__.__name__, THEME_DEFAULTS["sCTkDial"])
        self.canvas.configure(bg=self._resolve_color(theme_map.get("fg_color")))
        self._draw_dial_base()

    def _decode_mac_touchpad_delta(self, raw_delta):
        raw = raw_delta & 0xFFFFFFFF
        delta_y = raw & 0xFFFF
        if delta_y >= 0x8000: delta_y -= 0x10000
        return delta_y

    def configure(self, **kwargs):
        if "state" in kwargs: self._state = "normal" if kwargs.pop("state").lower() == "normal" else "disabled"
        if "diameter" in kwargs:
            dim = int(kwargs.pop("diameter"))
            super().configure(width=dim, height=dim)
        if "divisions" in kwargs: self._divisions = int(kwargs.pop("divisions"))
        super().configure(**kwargs)
        if self.canvas.winfo_exists(): self._draw_dial_base()

    def cget(self, attribute_name):
        if attribute_name == "state": return self._state
        if attribute_name == "diameter": return self.winfo_width()
        if attribute_name == "divisions": return self._divisions
        return super().cget(attribute_name)

    def _draw_dial_base(self):
        """
        Polymorphic Vector Drawing Engine.
        Dynamically adjusts graphics, colors, angular sweeps, and indicator pointer
        styles depending on whether a Selector, Range, or Continuous module is calling it.
        """
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # FIXED DESIGNER FALLBACK:
        # If running inside Pygubu's preview manager loops and winfo returns zero,
        # fallback directly to the diameter layout property setting to force rendering visible!
        if width < 10 or height < 10:
            width = int(getattr(self, "width", 120))
            height = width

        child_classname = self.__class__.__name__
        theme_map = THEME_DEFAULTS.get(child_classname, THEME_DEFAULTS["sCTkDial"])

        bg_color = self._resolve_color(theme_map.get("fg_color"))
        shadow_paint = self._resolve_color(theme_map.get("shadow_color"))
        is_dark_mode = (ctk.get_appearance_mode() == "Dark")

        if self._state == "disabled":
            text_color = self._resolve_color(theme_map.get("disabled_text_color"))
            dial_color = self._resolve_color(theme_map.get("disabled_dial_color"))
            pointer_glow = self._resolve_color(
                theme_map.get("disabled_dimple_glow", theme_map.get("disabled_text_color")))
        else:
            text_color = self._resolve_color(theme_map.get("text_color"))
            dial_color = self._resolve_color(theme_map.get("dial_color"))
            pointer_glow = self._resolve_color(("#CBD5E1", "#3A455C"))

        self.canvas.configure(bg=bg_color)

        center_x = width / 2
        center_y = height / 2
        max_radius = min(center_x, center_y) - 6

        # FIXED: Increased buffer subtraction from -20 to -28 to safely draw
        # perimeter text text indicators fully inside the Canvas viewport mask box!
        knob_radius = min(center_x, center_y) - 28

        has_arc_constraints = hasattr(self, "_arc_angle")
        if has_arc_constraints:
            arc_sweep = float(self._arc_angle)
            start_deg = -90.0 - (arc_sweep / 2.0)
        else:
            arc_sweep = 360.0
            start_deg = 0.0

        # Evaluate distinct grid mark channels
        if child_classname == "sCTkDialSelector" and hasattr(self, "_labels"):
            total_ticks = len(self._labels)
        elif child_classname == "sCTkDialRange" and hasattr(self, "_divisions"):
            total_ticks = self._divisions
        else:
            total_ticks = self._divisions

        for i in range(total_ticks):
            if total_ticks > 1 and has_arc_constraints:
                fraction = i / (total_ticks - 1)
            else:
                fraction = i / total_ticks

            angle_deg = start_deg + (fraction * arc_sweep)
            angle_rad = math.radians(-angle_deg)

            x1 = center_x + knob_radius * math.cos(angle_rad)
            y1 = center_y - knob_radius * math.sin(angle_rad)
            x2 = center_x + (knob_radius + 6) * math.cos(angle_rad)
            y2 = center_y - (knob_radius + 6) * math.sin(angle_rad)

            self.canvas.create_line(x1, y1, x2, y2, fill=text_color, width=2.0)

            if child_classname == "sCTkDialSelector" and hasattr(self, "_labels") and i < len(self._labels):
                tx = center_x + (knob_radius + 18) * math.cos(angle_rad)
                ty = center_y - (knob_radius + 18) * math.sin(angle_rad)
                self.canvas.create_text(tx, ty, text=str(self._labels[i]), fill=text_color, font=("Arial", 9, "bold"))
            elif child_classname == "sCTkDialRange":
                range_val = int(self._from + (self._to - self._from) * fraction)
                tx = center_x + (knob_radius + 18) * math.cos(angle_rad)
                ty = center_y - (knob_radius + 18) * math.sin(angle_rad)
                self.canvas.create_text(tx, ty, text=str(range_val), fill=text_color, font=("Arial", 9, "bold"))

        # Metallic Matte 3D Knob Chassis
        self.canvas.create_oval(center_x - knob_radius + 1, center_y - knob_radius + 4,
                                center_x + knob_radius + 4, center_y + knob_radius + 4, fill=shadow_paint, outline="")

        if child_classname == "sCTkDialContinuous":
            num_side_teeth = 72
            teeth_shadow = "#000000" if is_dark_mode else "#334155"
            for k in range(num_side_teeth):
                k_angle = math.radians(-(k * (360.0 / num_side_teeth)))
                kx1 = center_x + knob_radius * math.cos(k_angle)
                ky1 = center_y - knob_radius * math.sin(k_angle)
                kx2 = center_x + (knob_radius - 3) * math.cos(k_angle)
                ky2 = center_y - (knob_radius - 3) * math.sin(k_angle)
                self.canvas.create_line(kx1, ky1, kx2, ky2, fill=teeth_shadow, width=1.5)

        bbox_knob = (center_x - knob_radius + 2, center_y - knob_radius + 2, center_x + knob_radius - 2,
                     center_y + knob_radius - 2)
        self.canvas.create_oval(bbox_knob, fill=dial_color, outline="#111625" if is_dark_mode else "#475569", width=1)

        rim_sparkle = "#4A5568" if is_dark_mode else "#E2E8F0"
        self.canvas.create_oval(center_x - knob_radius + 3, center_y - knob_radius + 3,
                                center_x + knob_radius - 3, center_y + knob_radius - 3, fill="", outline=rim_sparkle,
                                width=1)

        # Render Active Indicators
        val_pct = self._get_value_fraction()
        pointer_deg = start_deg + (val_pct * arc_sweep)
        pointer_rad = math.radians(-pointer_deg)

        if child_classname in ["sCTkDialSelector", "sCTkDialRange"]:
            px = center_x + (knob_radius - 2) * math.cos(pointer_rad)
            py = center_y - (knob_radius - 2) * math.sin(pointer_rad)
            pointer_paint = self._resolve_color(theme_map.get("pointer_color", text_color))
            self.canvas.create_line(center_x, center_y, px, py, fill=pointer_paint, width=3.0, arrow="last",
                                    arrowshape=(8, 10, 3))
            self.canvas.create_oval(center_x - 6, center_y - 6, center_x + 6, center_y + 6, fill=dial_color,
                                    outline=rim_sparkle, width=1)
        else:
            dimple_center_radius = knob_radius - 14
            dx = center_x + dimple_center_radius * math.cos(pointer_rad)
            dy = center_y - dimple_center_radius * math.sin(pointer_rad)
            ind_radius = 14.5
            dimple_abyss = "#010205" if is_dark_mode else "#0F172A"
            dimple_shade = "#0A0F1D" if is_dark_mode else "#334155"
            dimple_face = "#181E2B" if is_dark_mode else "#475569"

            self.canvas.create_oval(dx - ind_radius, dy - ind_radius, dx + ind_radius, dy + ind_radius,
                                    fill=dimple_face, outline="")
            self.canvas.create_oval(dx - ind_radius - 1.5, dy - ind_radius - 1.5, dx + ind_radius - 1,
                                    dy + ind_radius - 1, fill=dimple_shade, outline="")
            self.canvas.create_oval(dx - ind_radius - 2.5, dy - ind_radius - 2.5, dx + ind_radius - 2,
                                    dy + ind_radius - 2, fill=dimple_abyss, outline="")
            self.canvas.create_oval(dx - ind_radius + 1.5, dy - ind_radius + 1.5, dx + ind_radius + 1.5,
                                    dy + ind_radius + 1.5, fill="", outline=pointer_glow, width=1.5)


class sCTkDialSelector(sCTkDialBase):
    """Rotary switch selector module. Constrained to custom arc angles (default 270)."""

    def __init__(self, master=None, labels=None, arc_angle=270, command=None, diameter=120, **kw):
        self._labels = labels if labels is not None else ["POS 1", "POS 2", "POS 3"]
        self._arc_angle = float(arc_angle)
        super().__init__(master, divisions=len(self._labels), diameter=diameter, **kw)
        self._scroll_cooldown_seconds = 0.150
        self._command = command
        self._current_value = 0

    def _get_value_fraction(self):
        total_steps = len(self._labels) - 1
        return self._current_value / total_steps if total_steps > 0 else 0.0

    def configure(self, **kwargs):
        if "labels" in kwargs:
            self._labels = kwargs.pop("labels")
            self._divisions = len(self._labels)
        if "arc_angle" in kwargs: self._arc_angle = float(kwargs.pop("arc_angle"))
        if "command" in kwargs: self._command = kwargs.pop("command")
        super().configure(**kwargs)

    def cget(self, attribute_name):
        if attribute_name == "labels": return self._labels
        if attribute_name == "arc_angle": return self._arc_angle
        if attribute_name == "command": return self._command
        return super().cget(attribute_name)

    def set(self, value):
        target = int(value)
        total_len = len(self._labels)
        if total_len == 0: return
        if target >= total_len:
            target = 0
        elif target < 0:
            target = total_len - 1
        self._current_value = target
        if self.canvas.winfo_exists(): self._draw_dial_base()
        if self._command is not None and self._state == "normal": self._command(self._current_value)

    def get(self):
        return self._current_value

    def _on_left_click_step(self, event):
        self.set(self._current_value - 1)

    def _on_right_click_step(self, event):
        self.set(self._current_value + 1)

    def _on_button_press(self, event):
        self._last_y = event.y

    def _on_button_motion(self, event):
        if self._state == "disabled": return
        delta_y = self._last_y - event.y
        if abs(delta_y) > 25:
            self.set(self._current_value + (1 if delta_y > 0 else -1))
            self._last_y = event.y

    def _process_mac_touchpad_scroll(self, event):
        if self._state == "disabled": return "break"
        current_time = time.time()
        if current_time - self._last_scroll_time < self._scroll_cooldown_seconds: return "break"
        delta_y = self._decode_mac_touchpad_delta(event.delta)
        if delta_y != 0:
            self._last_scroll_time = current_time
            self.set(self._current_value + (1 if delta_y > 0 else -1))
        return "break"

    def _process_scroll_wheel(self, event):
        if self._state == "disabled": return
        if getattr(event, "num", 0) == 4 or (hasattr(event, "delta") and event.delta > 0):
            direction = 1
        elif getattr(event, "num", 0) == 5 or (hasattr(event, "delta") and event.delta < 0):
            direction = -1
        else:
            return
        self.set(self._current_value + direction)

import time


# =====================================================================
# MODULE 2: THE HARD END-STOP POTENTIOMETER (RANGED INTERFACE)
# =====================================================================
class sCTkDialRange(sCTkDialBase):
    """
    Ranged potentiometer module tracking discrete integer boundaries.
    Enforces absolute dead stops (does not loop at thresholds) and reports absolute integer states.
    """

    def __init__(self, master=None, from_=0, to=100, arc_angle=270, command=None, diameter=120, divisions=5, **kw):
        self._from = int(from_)
        self._to = int(to)
        self._arc_angle = float(arc_angle)

        # FIXED: Accept an explicit number of scale divisions separate from from/to range indices
        super().__init__(master, divisions=divisions, diameter=diameter, **kw)
        self._command = command
        self._current_value = self._from

    def _get_value_fraction(self):
        val_range = self._to - self._from
        return (self._current_value - self._from) / val_range if val_range > 0 else 0.0

    def configure(self, **kwargs):
        """Unified configuration intercept system."""
        if "from_" in kwargs or "min_value" in kwargs:
            self._from = int(kwargs.pop("from_", kwargs.pop("min_value", self._from)))
        if "to" in kwargs or "max_value" in kwargs:
            self._to = int(kwargs.pop("to", kwargs.pop("max_value", self._to)))
        if "arc_angle" in kwargs:
            self._arc_angle = float(kwargs.pop("arc_angle"))
        if "command" in kwargs:
            self._command = kwargs.pop("command")
        if "divisions" in kwargs:
            self._divisions = int(kwargs.pop("divisions"))

        super().configure(**kwargs)

    def cget(self, attribute_name):
        if attribute_name in ["from_", "min_value"]: return self._from
        if attribute_name in ["to", "max_value"]: return self._to
        if attribute_name == "arc_angle": return self._arc_angle
        if attribute_name == "command": return self._command
        if attribute_name == "divisions": return self._divisions
        return super().cget(attribute_name)

    def set(self, value):
        target = max(self._from, min(self._to, int(value)))
        if target != self._current_value:
            self._current_value = target
            if self.canvas.winfo_exists(): self._draw_dial_base()
            if self._command is not None and self._state == "normal":
                self._command(self._current_value)

    def get(self):
        return self._current_value

    def _on_left_click_step(self, event):
        self.set(self._current_value - 5)

    def _on_right_click_step(self, event):
        self.set(self._current_value + 5)

    def _on_button_press(self, event):
        self._last_y = event.y

    def _on_button_motion(self, event):
        if self._state == "disabled": return
        delta_y = self._last_y - event.y
        if abs(delta_y) > 2:
            direction = 1 if delta_y > 0 else -1
            self.set(self._current_value + (direction * 2))
            self._last_y = event.y

    def _process_mac_touchpad_scroll(self, event):
        if self._state == "disabled": return "break"
        import time
        current_time = time.time()
        if current_time - self._last_scroll_time < self._scroll_cooldown_seconds: return "break"
        delta_y = self._decode_mac_touchpad_delta(event.delta)
        if delta_y != 0:
            self._last_scroll_time = current_time
            self.set(self._current_value + (5 if delta_y > 0 else -5))
        return "break"

    def _process_scroll_wheel(self, event):
        if self._state == "disabled": return
        if getattr(event, "num", 0) == 4 or (hasattr(event, "delta") and event.delta > 0):
            direction = 5
        elif getattr(event, "num", 0) == 5 or (hasattr(event, "delta") and event.delta < 0):
            direction = -5
        else:
            return
        self.set(self._current_value + direction)


class sCTkDialContinuous(sCTkDialBase):
    """Infinite flywheel tuning wheel encoder."""
    def __init__(self, master=None, divisions=24, command=None, left_click_callback=None, right_click_callback=None, diameter=120, **kw):
        super().__init__(master, divisions=divisions, diameter=diameter, **kw)
        self._command = command
        self._left_click_callback = left_click_callback
        self._right_click_callback = right_click_callback
        self._current_value = 0

    def _get_value_fraction(self): return self._current_value / self._divisions
    def configure(self, **kwargs):
        if "command" in kwargs: self._command = kwargs.pop("command")
        if "left_click_callback" in kwargs: self._left_click_callback = kwargs.pop("left_click_callback")
        if "right_click_callback" in kwargs: self._right_click_callback = kwargs.pop("right_click_callback")
        super().configure(**kwargs)

    def cget(self, attribute_name):
        if attribute_name == "command": return self._command
        if attribute_name == "left_click_callback": return self._left_click_callback
        if attribute_name == "right_click_callback": return self._right_click_callback
        return super().cget(attribute_name)

    def set_position_index(self, step_delta):
        self._current_value = (self._current_value + int(step_delta)) % self._divisions
        if self.canvas.winfo_exists(): self._draw_dial_base()
        if self._command is not None and self._state == "normal": self._command(int(step_delta))

    def _on_left_click_step(self, event):
        if self._state == "disabled": return
        if self._left_click_callback is not None: self._left_click_callback()
        else: self.set_position_index(-1)

    def _on_right_click_step(self, event):
        if self._state == "disabled": return
        if self._right_click_callback is not None: self._right_click_callback()
        else: self.set_position_index(1)

    def _on_button_press(self, event): self._last_y = event.y
    def _on_button_motion(self, event):
        if self._state == "disabled": return
        delta_y = self._last_y - event.y
        if abs(delta_y) > 2:
            self.set_position_index(1 if delta_y > 0 else -1)
            self._last_y = event.y

    def _process_mac_touchpad_scroll(self, event):
        if self._state == "disabled": return "break"
        current_time = time.time()
        if current_time - self._last_scroll_time < self._scroll_cooldown_seconds: return "break"
        delta_y = self._decode_mac_touchpad_delta(event.delta)
        if delta_y != 0:
            self._last_scroll_time = current_time
            self.set_position_index(1 if delta_y > 0 else -1)
        return "break"

    def _process_scroll_wheel(self, event):
        if self._state == "disabled": return
        if getattr(event, "num", 0) == 4 or (hasattr(event, "delta") and event.delta > 0): direction = 1
        elif getattr(event, "num", 0) == 5 or (hasattr(event, "delta") and event.delta < 0): direction = -1
        else: return
        self.set_position_index(direction)


# =====================================================================
# START OF TEST HARNESS SECTION
# =====================================================================

# Global frequency tracking registers (Simulating independent rig states)
operating_modes = ["CW", "USB", "LSB", "AM", "FM", "RTTY"]
current_frequency_hz = 14032000
audio_volume_pct = 25


def refresh_frequency_display():
    """Formats raw integers into standard 14.032.000 layout specifications."""
    global current_frequency_hz
    freq_str = f"{current_frequency_hz:08d}"
    formatted_freq = f"{freq_str[-8:-6]}.{freq_str[-6:-3]}.{freq_str[-3:]}"
    if formatted_freq.startswith("."):
        formatted_freq = formatted_freq[1:]

    if 'lbl_vfo_display' in globals() and lbl_vfo_display.winfo_exists():
        lbl_vfo_display.configure(text=f"VFO Freq: {formatted_freq} MHz")


def on_mode_switch_rotated(active_index):
    """Callback for Selector Module: Receives strict integer indexes."""
    mode_string = operating_modes[active_index]
    if 'lbl_selector_display' in globals() and lbl_selector_display.winfo_exists():
        lbl_selector_display.configure(text=f"Mode: {mode_string} [Idx {active_index}]")


def on_volume_pot_rotated(absolute_value):
    """Callback for Range Module: Receives absolute value integers."""
    if 'lbl_range_display' in globals() and lbl_range_display.winfo_exists():
        lbl_range_display.configure(text=f"Volume: {absolute_value}%")


def on_vfo_dial_rotated(clicks_delta):
    """Unified event-driven callback called automatically on every valid scroll/drag change."""
    global current_frequency_hz
    current_frequency_hz += clicks_delta * 100
    current_frequency_hz = max(0, current_frequency_hz)
    refresh_frequency_display()


# Custom accelerated override routines (Moves physical dial 2 notches on click events)
def my_custom_left_click():
    if tuning_dial.cget("state") == "disabled": return
    tuning_dial.set_position_index(-2)


def my_custom_right_click():
    if tuning_dial.cget("state") == "disabled": return
    tuning_dial.set_position_index(2)


# =====================================================================
# SYSTEM ASSEMBLY TEST BENCH RUNNER MAIN
# =====================================================================
if __name__ == "__main__":
    import customtkinter as ctk

    # Ensure cross-module tracking points find your local widget packages
    from sCTkFrame import sCTkFrame
    from sCTkComboBox import sCTkComboBox
    from sCTkCheckBox import sCTkCheckBox
    from sCTkSlider import sCTkSlider
    from sCTkLabelSecondary import sCTkLabelSecondary
    from sCTkButtonPrimary import sCTkButtonPrimary

    app = ctk.CTk()  # Kept strictly untouched
    app.title("sCTkDial Examples")
    app.geometry("1060x580")  # Expanded slightly for cleaner padding separation
    app.configure(fg_color=("#F1F5F9", "#1C1C1C"))

    main_deck = sCTkFrame(app, fg_color="transparent", border_width=0)
    main_deck.pack(padx=15, pady=15, fill="both", expand=True)

    # -----------------------------------------------------------------
    # CONTAINER 1: THE DISCRETE MODE SELECTOR SWITCH
    # -----------------------------------------------------------------
    # FIXED: Frame width propagation unlocked to prevent side text truncation
    frame_selector = sCTkFrame(main_deck, fg_color=("#E2E8F0", "#262626"), corner_radius=8)
    frame_selector.pack(side="left", padx=10, fill="both", expand=True)

    lbl_sel_title = sCTkLabelSecondary(frame_selector, text="1. SELECTOR SWITCH", font=("Arial", 12, "bold"))
    lbl_sel_title.pack(pady=(12, 2))

    lbl_selector_display = sCTkLabelSecondary(frame_selector, text="Mode: CW [Idx 0]", font=("Arial", 11, "bold"),
                                              text_color=("#1A4375", "#FF9100"))
    lbl_selector_display.pack(side="bottom", pady=20)

    dial_selector = sCTkDialSelector(frame_selector, labels=operating_modes, arc_angle=270,
                                     command=on_mode_switch_rotated, diameter=110)
    dial_selector.pack(pady=10)
    dial_selector.set(0)

    # -----------------------------------------------------------------
    # CONTAINER 2: THE HARD END-STOP POTENTIOMETER (RANGE)
    # -----------------------------------------------------------------
    # FIXED: Frame width propagation unlocked to prevent side text truncation
    frame_range = sCTkFrame(main_deck, fg_color=("#E2E8F0", "#262626"), corner_radius=8)
    frame_range.pack(side="left", padx=10, fill="both", expand=True)

    lbl_rng_title = sCTkLabelSecondary(frame_range, text="2. POTENTIOMETER (RANGE)", font=("Arial", 12, "bold"))
    lbl_rng_title.pack(pady=(12, 2))

    lbl_range_display = sCTkLabelSecondary(frame_range, text=f"Volume: {audio_volume_pct}%", font=("Arial", 11, "bold"),
                                           text_color=("#1A4375", "#FF9100"))
    lbl_range_display.pack(side="bottom", pady=20)

    dial_range = sCTkDialRange(frame_range, from_=0, to=100, arc_angle=270, command=on_volume_pot_rotated, diameter=110,
                               divisions=5)
    dial_range.pack(pady=10)
    dial_range.set(audio_volume_pct)

    # -----------------------------------------------------------------
    # CONTAINER 3: THE INFINITE FLYWHEEL VFO ENCODER (CONTINUOUS)
    # -----------------------------------------------------------------
    # FIXED: Frame width propagation unlocked to prevent side text truncation
    frame_continuous = sCTkFrame(main_deck, fg_color=("#E2E8F0", "#262626"), corner_radius=8)
    frame_continuous.pack(side="left", padx=10, fill="both", expand=True)

    lbl_vfo_title = sCTkLabelSecondary(frame_continuous, text="3. INFINITE VFO WHEEL", font=("Arial", 12, "bold"))
    lbl_vfo_title.pack(pady=(12, 2))

    lbl_vfo_display = sCTkLabelSecondary(frame_continuous, text="VFO Freq: 14.032.000 MHz", font=("Arial", 11, "bold"),
                                         text_color=("#1A4375", "#FF9100"))
    lbl_vfo_display.pack(side="bottom", pady=20)

    tuning_dial = sCTkDialContinuous(
        frame_continuous,
        divisions=24,
        command=on_vfo_dial_rotated,
        left_click_callback=my_custom_left_click,
        right_click_callback=my_custom_right_click,
        diameter=130
    )
    tuning_dial.pack(pady=10)

    lbl_vfo_display = sCTkLabelSecondary(frame_continuous, text="VFO Freq: 14.032.000 MHz", font=("Arial", 11, "bold"),
                                         text_color=("#1A4375", "#FF9100"))
    lbl_vfo_display.pack(pady=4)
    # Selector Live Calibration Sliders Mounting Matrix
    f_sel_ctrl = sCTkFrame(frame_selector, fg_color="transparent", border_width=0)
    f_sel_ctrl.pack(fill="x", padx=15, pady=5)

    sCTkLabelSecondary(f_sel_ctrl, text="Size:", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
    s_sel_size = sCTkSlider(f_sel_ctrl, from_=70, to=160, command=lambda v: dial_selector.configure(diameter=int(v)),
                            width=120)
    s_sel_size.grid(row=0, column=1, padx=5, pady=3, sticky="e")
    s_sel_size.set(110)

    sCTkLabelSecondary(f_sel_ctrl, text="Arc:", font=("Arial", 10)).grid(row=1, column=0, sticky="w")
    s_sel_arc = sCTkSlider(f_sel_ctrl, from_=90, to=320, command=lambda v: dial_selector.configure(arc_angle=float(v)),
                           width=120)
    s_sel_arc.grid(row=1, column=1, padx=5, pady=3, sticky="e")
    s_sel_arc.set(270)

    # Potentiometer Live Calibration Sliders Mounting Matrix
    f_rng_ctrl = sCTkFrame(frame_range, fg_color="transparent", border_width=0)
    f_rng_ctrl.pack(fill="x", padx=15, pady=5)

    sCTkLabelSecondary(f_rng_ctrl, text="Size:", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
    s_rng_size = sCTkSlider(f_rng_ctrl, from_=70, to=160, command=lambda v: dial_range.configure(diameter=int(v)),
                            width=120)
    s_rng_size.grid(row=0, column=1, padx=5, pady=3, sticky="e")
    s_rng_size.set(110)

    sCTkLabelSecondary(f_rng_ctrl, text="Arc:", font=("Arial", 10)).grid(row=1, column=0, sticky="w")
    s_rng_arc = sCTkSlider(f_rng_ctrl, from_=90, to=320, command=lambda v: dial_range.configure(arc_angle=float(v)),
                           width=120)
    s_rng_arc.grid(row=1, column=1, padx=5, pady=3, sticky="e")
    s_rng_arc.set(270)

    sCTkLabelSecondary(f_rng_ctrl, text="Ticks:", font=("Arial", 10)).grid(row=2, column=0, sticky="w")
    s_rng_divs = sCTkSlider(f_rng_ctrl, from_=2, to=10, number_of_steps=8,
                            command=lambda v: dial_range.configure(divisions=int(v)), width=120)
    s_rng_divs.grid(row=2, column=1, padx=5, pady=3, sticky="e")
    s_rng_divs.set(5)

    sCTkLabelSecondary(f_rng_ctrl, text="Max:", font=("Arial", 10)).grid(row=3, column=0, sticky="w")
    s_rng_ceil = sCTkSlider(f_rng_ctrl, from_=50, to=250, command=lambda v: dial_range.configure(to=int(v)), width=120)
    s_rng_ceil.grid(row=3, column=1, padx=5, pady=3, sticky="e")
    s_rng_ceil.set(100)

    # Continuous Live Sizing Sliders Mounting Matrix
    f_vfo_ctrl = sCTkFrame(frame_continuous, fg_color="transparent", border_width=0)
    f_vfo_ctrl.pack(fill="x", padx=15, pady=5)

    sCTkLabelSecondary(f_vfo_ctrl, text="Size:", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
    s_vfo_size = sCTkSlider(f_vfo_ctrl, from_=70, to=160, command=lambda v: tuning_dial.configure(diameter=int(v)),
                            width=120)
    s_vfo_size.grid(row=0, column=1, padx=5, pady=3, sticky="e")
    s_vfo_size.set(130)

    # CONFIGURATION DECK BASE FOOTER ASSEMBLY
    footer = sCTkFrame(app, fg_color="transparent", border_width=0)
    footer.pack(fill="x", padx=25, pady=(5, 15))


    def on_sensitivity_changed(choice):
        numeric_part = choice.split()
        ms_str = numeric_part[0].replace("ms", "")
        ms_value = int(ms_str)
        tuning_dial._scroll_cooldown_seconds = ms_value / 1000.0
        dial_selector._scroll_cooldown_seconds = (ms_value / 1000.0) * 2.5
        dial_range._scroll_cooldown_seconds = ms_value / 1000.0


    sens_dropdown = sCTkComboBox(footer, values=["30ms (Fast)", "60ms (Normal)", "120ms (Slow)", "250ms (Heavy)"],
                                 command=on_sensitivity_changed, width=150)
    sens_dropdown.pack(side="left", padx=10)
    sens_dropdown.set("60ms (Normal)")


    def on_state_toggle_changed(choice):
        target_state = "normal" if "Normal" in choice else "disabled"
        dial_selector.configure(state=target_state)
        dial_range.configure(state=target_state)
        tuning_dial.configure(state=target_state)


    state_dropdown = sCTkComboBox(footer, values=["Normal State (Active)", "Disabled State (Locked)"],
                                  command=on_state_toggle_changed, width=180)
    state_dropdown.pack(side="left", padx=10)
    state_dropdown.set("Normal State (Active)")


    def toggle_theme():
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")


    theme_btn = sCTkButtonPrimary(footer, text="Toggle Layout Themes", command=toggle_theme, width=160)
    theme_btn.pack(side="right", padx=10)

    app.mainloop()





