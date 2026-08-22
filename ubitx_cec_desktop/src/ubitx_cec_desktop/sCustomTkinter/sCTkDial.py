#!/usr/bin/python3
"""
sCTKDialBase - Centralized Abstract Base Class for Theme-Adaptive Mechanical Rotary Encoders
"""
import sys
import math
import time
import customtkinter as ctk
from sCTkFrame import sCTkFrame
from ThemeableWidget import ThemeableWidget
from sCTkSlider import sCTkSlider


class sCTKDialBase(sCTkFrame, ThemeableWidget):
    """Abstract Base Class for theme-adaptive mechanical rotary encoder widgets."""

    def __init__(self, master=None, divisions=24, state="normal", width=120, height=120, **kw):
        # 1. Fire our shared theme logic first. It handles filtering completely!
        ThemeableWidget.__init__(self, kw)

        # 🛠️ THE NAMEERROR FIX: Pull the background color string out of memory
        # directly via your Introspection class name map inside GLOBAL_THEME_REGISTRY!
        from ThemeableWidget import GLOBAL_THEME_REGISTRY
        theme_map = GLOBAL_THEME_REGISTRY.get(self.__class__.__name__, GLOBAL_THEME_REGISTRY.get("sCTkDial", {}))
        theme_bg_raw = theme_map.get("fg_color", "transparent")

        # Re-verify geometry dimensions cleanly
        target_diameter = kw.get("diameter", None)
        if target_diameter is not None:
            width, height = int(target_diameter), int(target_diameter)

        # 2. Initialize parent frame wrapper layout directly with pure native keywords
        super().__init__(master, width=width, height=height, **self.final_kw)

        # Store internal operational parameters onto instance memory track
        self._divisions = int(divisions) if int(divisions) > 0 else 24
        self._state = "normal" if state.lower() == "normal" else "disabled"
        self._custom_disabled_map = self._widget_disabled_map
        self._current_value = 0
        self._scroll_cooldown_seconds = 0.060
        self._last_scroll_time = 0.0
        self._last_y = 0

        # 3. Construct inner raw tracking drawing canvas layer safely using resolved color variables
        self.canvas = ctk.CTkCanvas(
            self,
            highlightthickness=0,
            bd=0,
            bg=self._resolve_color(theme_bg_raw)
        )
        self.canvas.pack(fill="both", expand=True)
        self.pack_propagate(False)
        self.grid_propagate(False)

        # Wire up structural core interface bindings
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
        if hasattr(self, "_canvas") and self._canvas is not None:
            layers_to_bind.append(self._canvas)

        for target_layer in layers_to_bind:
            if sys.platform == "darwin":
                target_layer.bind("<TouchpadScroll>", self._process_mac_touchpad_scroll, add="+")
            target_layer.bind("<MouseWheel>", self._process_scroll_wheel, add="+")
            target_layer.bind("<Button-4>", self._process_scroll_wheel, add="+")
            target_layer.bind("<Button-5>", self._process_scroll_wheel, add="+")

    def _on_mouse_enter(self):
        if self._state == "normal":
            self.canvas.focus_set()

    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)
        if hasattr(self, "canvas") and self.canvas.winfo_exists():
            self.after(20, self._process_theme_repaint)

    def _process_theme_repaint(self):
        # Dynamically evaluate the active component skin directly via instance class profiles
        from ThemeableWidget import GLOBAL_THEME_REGISTRY
        theme_map = GLOBAL_THEME_REGISTRY.get(self.__class__.__name__, GLOBAL_THEME_REGISTRY.get("sCTkDial", {}))
        self.canvas.configure(bg=self._resolve_color(theme_map.get("fg_color", "transparent")))
        self._draw_dial_base()

    def _decode_mac_touchpad_delta(self, raw_delta):
        raw = raw_delta & 0xFFFFFFFF
        delta_y = raw & 0xFFFF
        if delta_y >= 0x8000:
            delta_y -= 0x10000
        return delta_y

    def configure(self, *args, **kwargs):
        """Handles Pygubu designer queries and manages composite state updates safely."""

        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Pygubu Inspector compatibility check)
        # -----------------------------------------------------------------
        if args and len(args) == 1:
            pname = args[0]

            if pname == "width":
                current_w = super().cget("width") if hasattr(self, "cget") else 120
                return ('width', 'width', 'Width', 120, current_w)
            if pname == "height":
                current_h = super().cget("height") if hasattr(self, "cget") else 120
                return ('height', 'height', 'Height', 120, current_h)
            if pname == "state":
                return ('state', 'state', 'State', 'normal', getattr(self, "_state", "normal"))

            if pname == "labels":
                return ('labels', 'labels', 'Labels', "POS 1, POS 2, POS 3",
                        ", ".join(getattr(self, "_labels", ["POS 1", "POS 2", "POS 3"])))

            if pname in ["diameter", "divisions", "arc_angle", "from_", "to", "command", "left_click_callback",
                         "right_click_callback"]:
                return (pname, pname, pname, "", "")

            # 🛠️ FIXED: Secure cross-inheritance tracking fallback pass down to parent frame layers
            try:
                return super().configure(pname)
            except Exception:
                return (pname, pname, pname, "", "")

        # -----------------------------------------------------------------
        # ZONE B: SUB-COMPONENT SANITIZATION & STATE INTERCEPTION
        # -----------------------------------------------------------------
        if "width" in kwargs:
            w = kwargs["width"]
            kwargs["width"] = int(w) if (w and str(w).strip()) else 120
        if "height" in kwargs:
            h = kwargs["height"]
            kwargs["height"] = int(h) if (h and str(h).strip()) else 120

        if "state" in kwargs:
            st = kwargs.pop("state")
            self._state = str(st).strip().lower() if (st and str(st).strip()) else "normal"

            # 🛠️ THE CLEAN INTERACTIVE LOCK TRACK (Telemetry Prints Deleted)
            self._custom_current_state = self._state
            SCROLL_EVENTS = ["<MouseWheel>", "<TouchpadScroll>", "<Button-4>", "<Button-5>", "<Shift-ButtonPress-1>",
                             "<Shift-B1-Motion>"]

            if self._state == "normal":
                try:
                    self.canvas.bind("<Button-1>", self._on_left_click_step)
                    self.canvas.bind("<Button-2>", self._on_right_click_step)
                    self.canvas.bind("<Button-3>", self._on_right_click_step)
                except Exception:
                    pass
            else:
                try:
                    self.canvas.unbind("<Button-1>")
                    self.canvas.unbind("<Button-2>")
                    self.canvas.unbind("<Button-3>")
                    for ev in SCROLL_EVENTS:
                        self.canvas.unbind(ev)
                except Exception:
                    pass

            if hasattr(self, "_draw_dial_base"):
                self._draw_dial_base()

        # -----------------------------------------------------------------
        # ZONE C: RUNTIME KEYWORDS MRO ROUTING PASS
        # -----------------------------------------------------------------
        return super().configure(**kwargs)

    def cget(self, attribute_name):
        if attribute_name == "state":
            return self._state
        if attribute_name == "diameter":
            return self.winfo_width()
        if attribute_name == "divisions":
            return self._divisions
        return super().cget(attribute_name)

    def _draw_dial_base(self):
        """
        Polymorphic Vector Drawing Engine.
        Self-corrects dimensional lookups and forcefully synchronizes
        subdivision array states using pre-sanitized mixin mapping tuples.
        """
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 10 or height < 10:
            width = int(self.cget("width") if hasattr(self, "cget") else 120)
            height = width

        child_classname = self.__class__.__name__

        # 🛠️ THE COMPREHENSIVE TEXTURE MAP LOOKUP TRACK:
        # Pull your master configurations straight from the active global registry
        from ThemeableWidget import GLOBAL_THEME_REGISTRY
        theme_map = GLOBAL_THEME_REGISTRY.get(child_classname, GLOBAL_THEME_REGISTRY.get("sCTkDialContinuous", {}))

        # Extract active visual aesthetics cleanly
        bg_color = self._resolve_color(theme_map.get("fg_color", ("#F1F5F9", "#0A0A0A")))
        shadow_paint = self._resolve_color(theme_map.get("shadow_color", ("#CBD5E1", "#02040A")))
        text_color = self._resolve_color(theme_map.get("text_color", ("#1A4375", "#FF9100")))
        dial_color = self._resolve_color(theme_map.get("dial_color", ("#1E293B", "#181E2B")))
        is_dark_mode = (ctk.get_appearance_mode() == "Dark")

        # 🛠️ THE TUPLE CONVERSION FIX:
        # Instead of chasing raw dictionary lists, we look directly up to the
        # instance variable self._widget_disabled_map which has already been
        # completely transformed into safe, CustomTkinter-ready tuples!
        if self._state == "disabled":
            d_map = getattr(self, "_widget_disabled_map", {})

            # Map fallback strings cleanly if an entry property is missing from themes.json
            text_color = self._resolve_color(d_map.get("text_color") or ("#94A3B8", "#4B5563"))
            dial_color = self._resolve_color(d_map.get("fg_color") or ("#E2E8F0", "#1A1D24"))
            pointer_glow = self._resolve_color(d_map.get("disabled_dimple_glow") or ("#CBD5E1", "#334155"))
        else:
            pointer_glow = self._resolve_color(theme_map.get("pointer_glow_color", ("#CBD5E1", "#3A455C")))

        # Commit background rendering configuration to the tracking frame surface area
        self.canvas.configure(bg=bg_color)

        center_x = width / 2
        center_y = height / 2
        knob_radius = min(center_x, center_y) - 28

        has_arc_constraints = hasattr(self, "_arc_angle")
        arc_sweep = float(self._arc_angle) if has_arc_constraints else 360.0
        start_deg = -90.0 - (arc_sweep / 2.0) if has_arc_constraints else 0.0

        # Polymorphic subdivision state tracker sync check
        if child_classname == "sCTkDialSelector" and hasattr(self, "_labels"):
            if not self._labels or len(self._labels) == 0:
                self._labels = list(getattr(self, "_default_labels", ["POS 1", "POS 2", "POS 3"]))
            total_ticks = len(self._labels)
            self._divisions = total_ticks  # Synchronize state variable
        elif child_classname == "sCTkDialRange" and hasattr(self, "_divisions"):
            total_ticks = int(self._divisions) if (self._divisions and int(self._divisions) > 0) else 5
        else:
            total_ticks = int(self._divisions) if (hasattr(self, "_divisions") and self._divisions) else 24

        # 3. Draw tick scales and index text element overlays
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

            if child_classname == "sCTkDialSelector" and i < len(self._labels):
                tx = center_x + (knob_radius + 18) * math.cos(angle_rad)
                ty = center_y - (knob_radius + 18) * math.sin(angle_rad)
                self.canvas.create_text(tx, ty, text=str(self._labels[i]), fill=text_color, font=("Arial", 9, "bold"))
            elif child_classname == "sCTkDialRange":
                from_val = getattr(self, "_from", 0)
                to_val = getattr(self, "_to", 100)
                range_val = int(from_val + (to_val - from_val) * fraction)
                tx = center_x + (knob_radius + 18) * math.cos(angle_rad)
                ty = center_y - (knob_radius + 18) * math.sin(angle_rad)
                self.canvas.create_text(tx, ty, text=str(range_val), fill=text_color, font=("Arial", 9, "bold"))

        # Metallic Matte 3D Mechanical Knob Chassis Ring
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

        # 4. Render Active Mechanical Indicators & Pointers
        val_pct = self._get_value_fraction() if hasattr(self, "_get_value_fraction") else 0.0
        pointer_deg = start_deg + (val_pct * arc_sweep)
        pointer_rad = math.radians(-pointer_deg)

        if child_classname in ["sCTkDialSelector", "sCTkDialRange"]:
            px = center_x + (knob_radius - 2) * math.cos(pointer_rad)
            py = center_y - (knob_radius - 2) * math.sin(pointer_rad)

            # 🛠️ THE POINTER STATE FIX:
            # If the widget is disabled, first check if your custom disabled map has an explicit
            # pointer override. If it doesn't, fall back gracefully to your faded 'text_color'!
            if self._state == "disabled":
                d_map = getattr(self, "_widget_disabled_map", {})
                pointer_paint = self._resolve_color(d_map.get("pointer_color") or text_color)
            else:
                pointer_paint = self._resolve_color(theme_map.get("pointer_color", text_color))

            self.canvas.create_line(
                center_x, center_y, px, py,
                fill=pointer_paint,
                width=3.0,
                arrow="last",
                arrowshape=(8, 10, 3)
            )
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


"""
sCTkDialContinuous - Infinite Flywheel Tuning Encoder Subclass
"""
import time


class sCTkDialContinuous(sCTKDialBase):
    """
    Infinite flywheel tuning wheel encoder.
    Flashes a signature signed direction step velocity delta integer (+1, -1, etc.) on rotation.
    Visual indicator loop wraps around 360-degrees dynamically.
    Fully insulated against Pygubu-Designer empty-string callback removals.
    """

    def __init__(self, master=None, divisions=24, command=None, left_click_callback=None, right_click_callback=None,
                 diameter=120, **kw):
        # 1. Forward core parameters safely up to your modernized parent base class initialization track
        super().__init__(master, divisions=divisions, diameter=diameter, **kw)
        self._command = command

        # Guard: Sanitize empty design-time strings out of initial creation footprint safely
        self._left_click_callback = left_click_callback if (
                    left_click_callback and str(left_click_callback).strip()) else None
        self._right_click_callback = right_click_callback if (
                    right_click_callback and str(right_click_callback).strip()) else None
        self._current_value = 0

        # 🛠️ STATE SYNC FIX: Initialize framework operational trackers to maintain container cascade parity
        self._custom_current_state = "normal" if self._state == "normal" else "disabled"

    def _get_value_fraction(self):
        return self._current_value / self._divisions

    def configure(self, *args, **kwargs):
        """Unified continuous wheel configuration routing."""
        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Forward to sCTKDialBase Interceptor)
        # -----------------------------------------------------------------
        if args:
            return super().configure(*args, **kwargs)

        # -----------------------------------------------------------------
        # ZONE B: SPECIALIZED PROPERTY POPPING & SANITIZATION
        # -----------------------------------------------------------------
        if "divisions" in kwargs:
            divs = kwargs.pop("divisions")
            self._divisions = int(divs) if (divs and str(divs).strip()) else 24

        if "command" in kwargs:
            cb = kwargs.pop("command")
            self._command = cb if (cb and str(cb).strip()) else None

        if "left_click_callback" in kwargs:
            cb = kwargs.pop("left_click_callback")
            self._left_click_callback = cb if (cb and str(cb).strip()) else None

        if "right_click_callback" in kwargs:
            cb = kwargs.pop("right_click_callback")
            self._right_click_callback = cb if (cb and str(cb).strip()) else None

        # 🛠️ DIMENSION OVERRIDE SANITIZATION FIX:
        # Avoid direct mutations of unmapped _target trackers. Route geometry metrics
        # directly into width and height keyword arguments to trigger framework geometry passes.
        if "diameter" in kwargs:
            d_val = kwargs.pop("diameter")
            if d_val and str(d_val).strip():
                d = int(d_val)
            else:
                d = int(kwargs.get("width", super().cget("width") if hasattr(self, "cget") else 120))
            kwargs["width"], kwargs["height"] = d, d

        # -----------------------------------------------------------------
        # ZONE C: RUNTIME KEYWORDS MRO ROUTING PASS & RE-DRAW PROPS
        # -----------------------------------------------------------------
        result = super().configure(**kwargs)

        # Sync your custom framework tracker string with your parent base mode adjustments
        if "state" in kwargs:
            self._custom_current_state = self._state

        if self.canvas.winfo_exists():
            self._draw_dial_base()
        return result

    def cget(self, attribute_name):
        """Unified attribute state query lookup."""
        if attribute_name == "command":
            return self._command
        if attribute_name == "left_click_callback":
            return self._left_click_callback
        if attribute_name == "right_click_callback":
            return self._right_click_callback
        return super().cget(attribute_name)

    def set_position_index(self, step_delta):
        """Advances the 3D visual dimple layout coordinates via an integer delta tracking loop."""
        self._current_value = (self._current_value + int(step_delta)) % self._divisions
        if self.canvas.winfo_exists():
            self._draw_dial_base()
        if self._command is not None and self._state == "normal":
            self._command(int(step_delta))

    def _on_left_click_step(self, event):
        if self._state == "disabled":
            return
        if self._left_click_callback is not None and callable(self._left_click_callback):
            self._left_click_callback()
        else:
            self.set_position_index(-1)

    def _on_right_click_step(self, event):
        if self._state == "disabled":
            return
        if self._right_click_callback is not None and callable(self._right_click_callback):
            self._right_click_callback()
        else:
            self.set_position_index(1)

    def _on_button_press(self, event):
        self._last_y = event.y

    def _on_button_motion(self, event):
        if self._state == "disabled":
            return
        delta_y = self._last_y - event.y
        if abs(delta_y) > 2:
            direction = 1 if delta_y > 0 else -1
            self.set_position_index(direction)
            self._last_y = event.y

    def _process_mac_touchpad_scroll(self, event):
        if self._state == "disabled":
            return "break"
        current_time = time.time()
        if current_time - self._last_scroll_time < self._scroll_cooldown_seconds:
            return "break"
        delta_y = self._decode_mac_touchpad_delta(event.delta)
        if delta_y != 0:
            self._last_scroll_time = current_time
            self.set_position_index(1 if delta_y > 0 else -1)
        return "break"

    def _process_scroll_wheel(self, event):
        if self._state == "disabled":
            return
        if getattr(event, "num", 0) == 4 or (hasattr(event, "delta") and event.delta > 0):
            direction = 1
        elif getattr(event, "num", 0) == 5 or (hasattr(event, "delta") and event.delta < 0):
            direction = -1
        else:
            return
        self.set_position_index(direction)


"""
sCTkDialSelector - Rotary Switch Option Selector Subclass
"""
import ast
import time



class sCTkDialSelector(sCTKDialBase):
    """
    Rotary switch selector module. Constrained to custom arc angles (default 270).
    Loops infinitely past outer limits and reports the active integer item index position.
    """

    def __init__(self, master=None, labels=None, arc_angle=270, command=None, left_click_callback=None,
                 right_click_callback=None, diameter=120, **kw):
        # 1. Parse and sanitize design-time text array configurations
        if isinstance(labels, str) and labels.strip():
            try:
                labels = ast.literal_eval(labels.strip())
            except Exception:
                labels = [x.strip().strip("'\"") for x in labels.strip()[1:-1].split(",")]

        # Capture your core original defaults baseline natively
        self._default_labels = ["POS 1", "POS 2", "POS 3"]
        self._labels = labels if labels is not None else list(self._default_labels)
        self._arc_angle = float(arc_angle)

        # 2. Forward parameters safely up to your modernized parent base class initialization track
        super().__init__(master, divisions=len(self._labels), diameter=diameter, **kw)

        self._scroll_cooldown_seconds = 0.150
        self._command = command

        # Guard: Sanitize empty design-time strings out of initial creation footprint
        self._left_click_callback = left_click_callback if (
                    left_click_callback and str(left_click_callback).strip()) else None
        self._right_click_callback = right_click_callback if (
                    right_click_callback and str(right_click_callback).strip()) else None
        self._current_value = 0

        # Initialize custom framework tracker state string
        self._custom_current_state = "normal" if self._state == "normal" else "disabled"

    def _get_value_fraction(self):
        total_steps = len(self._labels) - 1
        return self._current_value / total_steps if total_steps > 0 else 0.0

    def configure(self, *args, **kwargs):
        """Unified switch selector configuration routing supporting comma-separated property strings."""
        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Forward to sCTKDialBase Interceptor)
        # -----------------------------------------------------------------
        if args:
            return super().configure(*args, **kwargs)

        # -----------------------------------------------------------------
        # ZONE B: SPECIALIZED PROPERTY POPPING & SANITIZATION
        # -----------------------------------------------------------------
        if "labels" in kwargs:
            lbls = kwargs.pop("labels")

            # COMMA SEPARATED PARSING LAYER: Cleanly strip brackets/quotes and split on commas
            if isinstance(lbls, str):
                stripped_lbls = lbls.strip().strip("[]\"'")
                if stripped_lbls:
                    lbls = [x.strip() for x in stripped_lbls.split(",")]
                else:
                    lbls = list(getattr(self, "_default_labels", ["POS 1", "POS 2", "POS 3"]))

            # CLEARANCE EXCEPTION GUARD: If wiped out completely, snap straight back to defaults
            if lbls is None or lbls == "" or len(lbls) == 0:
                self._labels = list(getattr(self, "_default_labels", ["POS 1", "POS 2", "POS 3"]))
            else:
                self._labels = lbls

            self._divisions = len(self._labels)

        if "arc_angle" in kwargs:
            arc = kwargs.pop("arc_angle")
            self._arc_angle = float(arc) if (arc and str(arc).strip()) else 270.0

        if "command" in kwargs:
            self._command = kwargs.pop("command")
        if "left_click_callback" in kwargs:
            self._left_click_callback = kwargs.pop("left_click_callback")
        if "right_click_callback" in kwargs:
            self._right_click_callback = kwargs.pop("right_click_callback")

        if "diameter" in kwargs:
            d_val = kwargs.pop("diameter")
            if d_val and str(d_val).strip():
                d = int(d_val)
            else:
                d = int(kwargs.get("width", super().cget("width") if hasattr(self, "cget") else 120))
            kwargs["width"], kwargs["height"] = d, d

        # -----------------------------------------------------------------
        # ZONE C: RUNTIME KEYWORDS MRO ROUTING PASS & RE-DRAW PROPS
        # -----------------------------------------------------------------
        result = super().configure(**kwargs)

        if "state" in kwargs:
            self._custom_current_state = self._state

        if self.canvas.winfo_exists():
            self._draw_dial_base()
        return result

    def cget(self, attribute_name):
        """Unified attribute state query lookup."""
        if attribute_name == "labels":
            return self._labels
        if attribute_name == "arc_angle":
            return self._arc_angle
        if attribute_name == "command":
            return self._command
        if attribute_name == "left_click_callback":
            return self._left_click_callback
        if attribute_name == "right_click_callback":
            return self._right_click_callback
        return super().cget(attribute_name)

    def set(self, value):
        """Sets the active index integer and forces canvas updates."""
        target = int(value)
        total_len = len(self._labels)
        if total_len == 0:
            return

        # Handle rolling index loops smoothly
        if target >= total_len:
            target = 0
        elif target < 0:
            target = total_len - 1

        self._current_value = target
        if self.canvas.winfo_exists():
            self._draw_dial_base()
        if self._command is not None and self._state == "normal":
            self._command(self._current_value)

    def get(self):
        return self._current_value

    def _on_left_click_step(self, event):
        if self._state == "disabled":
            return
        if self._left_click_callback is not None and callable(self._left_click_callback):
            self._left_click_callback()
        else:
            self.set(self._current_value - 1)

    def _on_right_click_step(self, event):
        if self._state == "disabled":
            return
        if self._right_click_callback is not None and callable(self._right_click_callback):
            self._right_click_callback()
        else:
            self.set(self._current_value + 1)

    def _on_button_press(self, event):
        self._last_y = event.y

    def _on_button_motion(self, event):
        if self._state == "disabled":
            return
        delta_y = self._last_y - event.y
        if abs(delta_y) > 25:
            direction = 1 if delta_y > 0 else -1
            self.set(self._current_value + direction)
            self._last_y = event.y

    def _process_mac_touchpad_scroll(self, event):
        if self._state == "disabled":
            return "break"
        current_time = time.time()
        if current_time - self._last_scroll_time < self._scroll_cooldown_seconds:
            return "break"
        delta_y = self._decode_mac_touchpad_delta(event.delta)
        if delta_y != 0:
            self._last_scroll_time = current_time
            self.set(self._current_value + (1 if delta_y > 0 else -1))
        return "break"

    def _process_scroll_wheel(self, event):
        if self._state == "disabled":
            return
        if getattr(event, "num", 0) == 4 or (hasattr(event, "delta") and event.delta > 0):
            direction = 1
        elif getattr(event, "num", 0) == 5 or (hasattr(event, "delta") and event.delta < 0):
            direction = -1
        else:
            return
        self.set(self._current_value + direction)


"""
sCTkDialRange - Ranged Potentiometer Boundary Controller Subclass
"""
import time


class sCTkDialRange(sCTKDialBase):
    """
    Ranged potentiometer module tracking discrete integer boundaries.
    Enforces absolute dead stops (does not loop at thresholds) and reports absolute integer states.
    """

    def __init__(self, master=None, from_=0, to=100, arc_angle=270, command=None, left_click_callback=None,
                 right_click_callback=None, diameter=120, divisions=5, **kw):
        self._from = int(from_)
        self._to = int(to)
        self._arc_angle = float(arc_angle)

        # Forward configuration metrics safely up to your modernized parent initialization track
        super().__init__(master, divisions=divisions, diameter=diameter, **kw)
        self._command = command

        # Guard: Sanitize empty design-time strings out of initial creation footprint safely
        self._left_click_callback = left_click_callback if (
                    left_click_callback and str(left_click_callback).strip()) else None
        self._right_click_callback = right_click_callback if (
                    right_click_callback and str(right_click_callback).strip()) else None
        self._current_value = self._from

        # 🛠️ STATE SYNC FIX: Explicitly map local framework tracker variables
        self._custom_current_state = "normal" if self._state == "normal" else "disabled"

    def _get_value_fraction(self):
        val_range = self._to - self._from
        return (self._current_value - self._from) / val_range if val_range > 0 else 0.0

    def configure(self, *args, **kwargs):
        """Unified ranged potentiometer configuration routing."""
        # -----------------------------------------------------------------
        # ZONE A: POSITION INTERCEPT (Forward to sCTKDialBase Interceptor)
        # -----------------------------------------------------------------
        if args:
            return super().configure(*args, **kwargs)

        # -----------------------------------------------------------------
        # ZONE B: SPECIALIZED PROPERTY POPPING & SANITIZATION
        # -----------------------------------------------------------------
        if "from_" in kwargs or "min_value" in kwargs:
            val = kwargs.pop("from_", kwargs.pop("min_value", 0))
            self._from = int(val) if (val and str(val).strip()) else 0

        if "to" in kwargs or "max_value" in kwargs:
            val = kwargs.pop("to", kwargs.pop("max_value", 100))
            self._to = int(val) if (val and str(val).strip()) else 100

        if "arc_angle" in kwargs:
            arc = kwargs.pop("arc_angle")
            self._arc_angle = float(arc) if (arc and str(arc).strip()) else 270.0

        if "divisions" in kwargs:
            divs = kwargs.pop("divisions")
            self._divisions = int(divs) if (divs and str(divs).strip()) else 5

        if "command" in kwargs:
            cb = kwargs.pop("command")
            self._command = cb if (cb and str(cb).strip()) else None

        if "left_click_callback" in kwargs:
            cb = kwargs.pop("left_click_callback")
            self._left_click_callback = cb if (cb and str(cb).strip()) else None

        if "right_click_callback" in kwargs:
            cb = kwargs.pop("right_click_callback")
            self._right_click_callback = cb if (cb and str(cb).strip()) else None

        if "diameter" in kwargs:
            d_val = kwargs.pop("diameter")
            if d_val and str(d_val).strip():
                d = int(d_val)
            else:
                d = int(kwargs.get("width", super().cget("width") if hasattr(self, "cget") else 120))
            kwargs["width"], kwargs["height"] = d, d

        # -----------------------------------------------------------------
        # ZONE C: RUNTIME KEYWORDS MRO ROUTING PASS & RE-DRAW PROPS
        # -----------------------------------------------------------------
        result = super().configure(**kwargs)

        if "state" in kwargs:
            self._custom_current_state = self._state

        if self.canvas.winfo_exists():
            self._draw_dial_base()
        return result

    def cget(self, attribute_name):
        """Unified attribute state query lookup."""
        if attribute_name in ["from_", "min_value"]:
            return self._from
        if attribute_name in ["to", "max_value"]:
            return self._to
        if attribute_name == "arc_angle":
            return self._arc_angle
        if attribute_name == "command":
            return self._command
        if attribute_name == "divisions":
            return self._divisions
        if attribute_name == "left_click_callback":
            return self._left_click_callback
        if attribute_name == "right_click_callback":
            return self._right_click_callback
        return super().cget(attribute_name)

    def set(self, value):
        """Sets the absolute integer value within hard bounded limits."""
        target = max(self._from, min(self._to, int(value)))
        if target != self._current_value:
            self._current_value = target
            if self.canvas.winfo_exists():
                self._draw_dial_base()
            if self._command is not None and self._state == "normal":
                self._command(self._current_value)

    def get(self):
        return self._current_value

    def _on_left_click_step(self, event):
        if self._state == "disabled":
            return
        if self._left_click_callback is not None and callable(self._left_click_callback):
            self._left_click_callback()
        else:
            self.set(self._current_value - 1)

    def _on_right_click_step(self, event):
        if self._state == "disabled":
            return
        if self._right_click_callback is not None and callable(self._right_click_callback):
            self._right_click_callback()
        else:
            self.set(self._current_value + 1)

    def _on_button_press(self, event):
        self._last_y = event.y

    def _on_button_motion(self, event):
        if self._state == "disabled":
            return
        delta_y = self._last_y - event.y
        if abs(delta_y) > 2:
            direction = 1 if delta_y > 0 else -1
            self.set(self._current_value + direction)
            self._last_y = event.y

    def _process_mac_touchpad_scroll(self, event):
        if self._state == "disabled":
            return "break"
        current_time = time.time()
        if current_time - self._last_scroll_time < self._scroll_cooldown_seconds:
            return "break"
        delta_y = self._decode_mac_touchpad_delta(event.delta)
        if delta_y != 0:
            self._last_scroll_time = current_time
            self.set(self._current_value + (1 if delta_y > 0 else -1))
        return "break"

    def _process_scroll_wheel(self, event):
        if self._state == "disabled":
            return
        if getattr(event, "num", 0) == 4 or (hasattr(event, "delta") and event.delta > 0):
            direction = 1
        elif getattr(event, "num", 0) == 5 or (hasattr(event, "delta") and event.delta < 0):
            direction = -1
        else:
            return
        self.set(self._current_value + direction)


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
    if tuning_dial.cget("state") == "disabled":
        return
    tuning_dial.set_position_index(-2)


def my_custom_right_click():
    if tuning_dial.cget("state") == "disabled":
        return
    tuning_dial.set_position_index(2)


# =====================================================================
# SYSTEM ASSEMBLY TEST BENCH RUNNER MAIN
# =====================================================================
if __name__ == "__main__":
    import customtkinter as ctk

    # Cross-module package imports
    from sCTkFrame import sCTkFrame
    from sCTkComboBox import sCTkComboBox
    from sCTkCheckBox import sCTkCheckBox
    from sCTkLabelSecondary import sCTkLabelSecondary
    from sCTkButtonPrimary import sCTkButtonPrimary
    from sCTkSlider import sCTkSlider

    # Concrete module lookups for our newly modernized child dials
    # from sCTkDialContinuous import sCTkDialContinuous
    # from sCTkDialSelector import sCTkDialSelector
    # from sCTkDialRange import sCTkDialRange

    app = ctk.CTk()
    app.title("sCTkDial Examples")
    app.geometry("1060x580")
    app.configure(fg_color=("#F1F5F9", "#1C1C1C"))

    main_deck = sCTkFrame(app, fg_color="transparent", border_width=0)
    main_deck.pack(padx=15, pady=15, fill="both", expand=True)

    # -----------------------------------------------------------------
    # CONTAINER 1: THE DISCRETE MODE SELECTOR SWITCH
    # -----------------------------------------------------------------
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
    frame_continuous = sCTkFrame(main_deck, fg_color=("#E2E8F0", "#262626"), corner_radius=8)
    frame_continuous.pack(side="left", padx=10, fill="both", expand=True)

    lbl_vfo_title = sCTkLabelSecondary(frame_continuous, text="3. INFINITE VFO WHEEL", font=("Arial", 12, "bold"))
    lbl_vfo_title.pack(pady=(12, 2))

    tuning_dial = sCTkDialContinuous(
        frame_continuous,
        divisions=24,
        command=on_vfo_dial_rotated,
        left_click_callback=my_custom_left_click,
        right_click_callback=my_custom_right_click,
        diameter=130
    )
    tuning_dial.pack(pady=10)

    # 🛠️ FIXED: This is now the ONLY reference to lbl_vfo_display in this container.
    # Placed safely *after* the dial pack so it is forced down beneath the wheel!
    lbl_vfo_display = sCTkLabelSecondary(frame_continuous, text="VFO Freq: 14.032.000 MHz", font=("Arial", 11, "bold"),
                                         text_color=("#1A4375", "#FF9100"))
    lbl_vfo_display.pack(side="bottom", pady=20)

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

        # 1. Update the custom mechanical dials
        dial_selector.configure(state=target_state)
        dial_range.configure(state=target_state)
        tuning_dial.configure(state=target_state)

        # 🛠️ THE HARNESS FIX: Explicitly propagate the target_state string
        # down to all live calibration slider instances sitting on your panels!
        s_sel_size.configure(state=target_state)
        s_sel_arc.configure(state=target_state)

        s_rng_size.configure(state=target_state)
        s_rng_arc.configure(state=target_state)
        s_rng_divs.configure(state=target_state)
        s_rng_ceil.configure(state=target_state)

        s_vfo_size.configure(state=target_state)


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





