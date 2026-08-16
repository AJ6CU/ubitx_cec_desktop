import sys
import math
import customtkinter as ctk

# Direct framework path module and theme dictionary registry imports
from sCTkFrame import sCTkFrame
from ThemeableWidget import ThemeableWidget
from sCTkThemes import THEME_DEFAULTS


class sCTkDial(sCTkFrame, ThemeableWidget):
    """
    A standalone, theme-adaptive mechanical rotary tuning dial widget with scroll wheel input tracking.
    Inherits geometry patterns from sCTkFrame and style definitions from ThemeableWidget.
    Features isolated cross-platform focus hooks specifically optimized for macOS Magic Mouse profiles.
    Strictly handles theme parameters via central registry lookups with zero local fallbacks.
    """

    def __init__(self, master=None, min_value=0.0, max_value=24.0, step=1.0, divisions=24,
                 command=None, left_click_callback=None, right_click_callback=None,
                 diameter=None, state="normal", width=120, height=120, **kw):
        theme_defaults = THEME_DEFAULTS["sCTkDial"]

        # 1. Initialize Themeable mixin safely to assemble self.final_kw and attributes
        ThemeableWidget.__init__(self, theme_defaults, kw)

        # 2. Map standard compatible configuration fields from registry records
        theme_bg_raw = theme_defaults.get("fg_color")

        # 3. Clean custom variables out of the keyword dictionary to shield the frame layer.
        self.final_kw.pop("fg_color", None)
        self.final_kw.pop("text_color", None)
        self.final_kw.pop("dial_color", None)
        self.final_kw.pop("shadow_color", None)
        self.final_kw.pop("disabled_text_color", None)
        self.final_kw.pop("disabled_dial_color", None)
        self.final_kw.pop("disabled_dimple_glow", None)

        # Dynamic Diameter Overrides evaluation math logic
        if diameter is not None:
            width = int(diameter)
            height = int(diameter)

        # 4. Construct the custom base frame using raw configuration mappings
        super().__init__(master, width=width, height=height, fg_color=theme_bg_raw, **self.final_kw)

        # Core operational constraint boundaries
        self.min_value = float(min_value)
        self.max_value = float(max_value)
        self.step = float(step)
        self._current_value = self.min_value
        self.divisions = int(divisions) if int(divisions) > 0 else 24

        # State Machine register hooks
        self._state = "normal" if state.lower() == "normal" else "disabled"

        # Action Callback slot array references
        self._command = command
        self._left_click_callback = left_click_callback
        self._right_click_callback = right_click_callback

        # Adjustable software swipe velocity filter (seconds debounce window)
        self._scroll_cooldown_seconds = 0.060
        self._last_scroll_time = 0.0

        # 5. Explicitly pass 'self' into instance method references to translate canvas backgrounds
        bg_resolved_string = ThemeableWidget._resolve_color(self, theme_bg_raw)

        self.canvas = ctk.CTkCanvas(self, highlightthickness=0, bd=0, bg=bg_resolved_string)
        self.canvas.pack(fill="both", expand=True, padx=0, pady=0)

        # Prevent layout shrinkage if nested loosely
        self.pack_propagate(False)
        self.grid_propagate(False)

        # Track mouse coordinates for drag operations
        self._last_y = 0

        # 6. BIND STANDARD EVENT ROUTING HANDLERS IMMEDIATELY
        self.canvas.bind("<Enter>", lambda e: self._on_mouse_enter())

        # Localized discrete mouse button click step shifting hooks
        self.canvas.bind("<Button-1>", self._on_left_click_step)
        self.canvas.bind("<Button-2>", self._on_right_click_step)
        self.canvas.bind("<Button-3>", self._on_right_click_step)

        # Shift + Click and Drag fallback routing channels
        self.canvas.bind("<Shift-ButtonPress-1>", self._on_button_press)
        self.canvas.bind("<Shift-B1-Motion>", self._on_button_motion)

        self.canvas.bind("<Configure>", lambda e: self._draw_dial())

        # 7. MULTI-PLATFORM ASYNCHRONOUS INITIALIZATION INTERCEPT PIPELINE
        self.after(50, self._inject_private_layer_bindings)

    def _inject_private_layer_bindings(self):
        """Attaches scrolling event listeners right across CustomTkinter's private layout tree canvas."""
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
        """Locks focus on hover only if the component state is active."""
        if self._state == "normal":
            self.canvas.focus_set()

    def _set_appearance_mode(self, mode_string):
        """Intercepts the top-level application background theme color shifts."""
        super()._set_appearance_mode(mode_string)
        if hasattr(self, "canvas") and self.canvas.winfo_exists():
            self.after(20, self._process_theme_repaint)

    def _process_theme_repaint(self):
        """Wipes and paints fresh layout parameters using active operational state configurations."""
        theme_map = THEME_DEFAULTS["sCTkDial"]
        bg_color = self._resolve_color(theme_map.get("fg_color"))
        self.canvas.configure(bg=bg_color)
        self._draw_dial()

    def configure(self, **kwargs):
        """Public unified frame layout configuration and state machine update modifiers."""
        if "state" in kwargs:
            self._state = "normal" if kwargs["state"].lower() == "normal" else "disabled"
            del kwargs["state"]
        if "diameter" in kwargs:
            dim = int(kwargs["diameter"])
            super().configure(width=dim, height=dim)
            del kwargs["diameter"]

        super().configure(**kwargs)
        if self.canvas.winfo_exists():
            self._draw_dial()

    def cget(self, attribute_name):
        """Public attribute state getter property lookup."""
        if attribute_name == "state":
            return self._state
        if attribute_name == "diameter":
            return self.winfo_width()
        return super().cget(attribute_name)

    def _draw_dial(self):
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width < 10 or height < 10:
            return

        theme_map = THEME_DEFAULTS["sCTkDial"]
        bg_color = self._resolve_color(theme_map.get("fg_color"))

        # FIXED: Legacy hardcoded fallback tuples entirely purged.
        # Resolves colors exclusively through central dictionary properties.
        if self._state == "disabled":
            text_color = self._resolve_color(theme_map.get("disabled_text_color"))
            dial_color = self._resolve_color(theme_map.get("disabled_dial_color"))
            dimple_glow = self._resolve_color(theme_map.get("disabled_dimple_glow"))
        else:
            text_color = self._resolve_color(theme_map.get("text_color"))
            dial_color = self._resolve_color(theme_map.get("dial_color"))
            dimple_glow = self._resolve_color(("#CBD5E1", "#3A455C"))  # Independent slate contrast ring

        shadow_paint = self._resolve_color(theme_map.get("shadow_color"))

        self.canvas.configure(bg=bg_color)

        center_x = width / 2
        center_y = height / 2

        max_radius = min(center_x, center_y) - 6
        knob_radius = max_radius - 14

        is_dark_mode = (ctk.get_appearance_mode() == "Dark")

        # 1. DRAW PERIPHERAL GRADUATION CALIBRATION COCKPIT TICKS
        for i in range(self.divisions):
            fraction = i / self.divisions
            angle_deg = fraction * 360.0
            angle_rad = math.radians(-angle_deg)

            x1 = center_x + knob_radius * math.cos(angle_rad)
            y1 = center_y - knob_radius * math.sin(angle_rad)
            x2 = center_x + (knob_radius + 6) * math.cos(angle_rad)
            y2 = center_y - (knob_radius + 6) * math.sin(angle_rad)

            is_major = (i % max(1, self.divisions // 4) == 0)
            self.canvas.create_line(x1, y1, x2, y2, fill=text_color, width=2.0 if is_major else 1.0)

        # 2. METALLIC MATTE 3D KNOB SURFACE SYSTEM
        self.canvas.create_oval(center_x - knob_radius + 1, center_y - knob_radius + 4,
                                center_x + knob_radius + 4, center_y + knob_radius + 4, fill=shadow_paint, outline="")

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

        # 3. PHOTO-MATCHED REVERSED-GRADIENT 3D SCOOPED DIMPLE CAVITY
        val_range = self.max_value - self.min_value
        val_pct = (self._current_value - self.min_value) / val_range if val_range != 0 else 0.0

        pointer_deg = val_pct * 360.0
        pointer_rad = math.radians(-pointer_deg)

        dimple_center_radius = knob_radius - 14
        dx = center_x + dimple_center_radius * math.cos(pointer_rad)
        dy = center_y - dimple_center_radius * math.sin(pointer_rad)

        ind_radius = 14.5

        dimple_abyss = "#010205" if is_dark_mode else "#0F172A"
        dimple_shade = "#0A0F1D" if is_dark_mode else "#334155"
        dimple_face = "#181E2B" if is_dark_mode else "#475569"

        self.canvas.create_oval(dx - ind_radius, dy - ind_radius, dx + ind_radius, dy + ind_radius, fill=dimple_face,
                                outline="")
        self.canvas.create_oval(dx - ind_radius - 1.5, dy - ind_radius - 1.5, dx + ind_radius - 1, dy + ind_radius - 1,
                                fill=dimple_shade, outline="")
        self.canvas.create_oval(dx - ind_radius - 2.5, dy - ind_radius - 2.5, dx + ind_radius - 2, dy + ind_radius - 2,
                                fill=dimple_abyss, outline="")
        self.canvas.create_oval(dx - ind_radius + 1.5, dy - ind_radius + 1.5, dx + ind_radius + 1.5,
                                dy + ind_radius + 1.5, fill="", outline=dimple_glow, width=1.5)

    def _on_button_press(self, event):
        """Saves initial mouse context coordinates to calculate Shift+Drag deltas."""
        if self._state == "disabled": return
        self._last_y = event.y

    def _on_button_motion(self, event):
        """Tracks vertical drag offsets to smoothly rotate dial vectors on desktop layouts."""
        if self._state == "disabled": return
        delta_y = self._last_y - event.y
        if abs(delta_y) > 2:
            direction = 1 if delta_y > 0 else -1
            self.set(self._current_value + (direction * self.step), invoke_callback=True, click_delta=direction)
            self._last_y = event.y

    def _on_left_click_step(self, event):
        """Localized Left-Click action route processor."""
        if self._state == "disabled": return
        if self._left_click_callback is not None:
            self._left_click_callback()
        else:
            new_value = self._current_value - self.step
            self.set(new_value, invoke_callback=True, click_delta=-1)

    def _on_right_click_step(self, event):
        """Localized Right-Click action route processor."""
        if self._state == "disabled": return
        if self._right_click_callback is not None:
            self._right_click_callback()
        else:
            new_value = self._current_value + self.step
            self.set(new_value, invoke_callback=True, click_delta=1)

    def _decode_mac_touchpad_delta(self, raw_delta):
        raw = raw_delta & 0xFFFFFFFF
        delta_y = raw & 0xFFFF
        if delta_y >= 0x8000:
            delta_y -= 0x10000
        return delta_y

    def _process_mac_touchpad_scroll(self, event):
        """Processes high-resolution continuous touchpad/Magic Mouse swiping events."""
        if self._state == "disabled": return "break"
        import time
        current_time = time.time()

        if current_time - self._last_scroll_time < self._scroll_cooldown_seconds:
            return "break"

        delta_y = self._decode_mac_touchpad_delta(event.delta)
        if delta_y != 0:
            direction = 1 if delta_y > 0 else -1
            new_value = self._current_value + (direction * self.step)

            if new_value >= self.max_value: new_value = self.min_value
            if new_value < self.min_value: new_value = self.max_value - self.step

            self._last_scroll_time = current_time
            self.set(new_value, invoke_callback=True, click_delta=direction)

        return "break"

    def _process_scroll_wheel(self, event):
        """Standard wheel event fallback handler for Windows, Linux, and traditional hardware mice."""
        if self._state == "disabled": return
        if getattr(event, "num", 0) == 4:
            direction = 1
        elif getattr(event, "num", 0) == 5:
            direction = -1
        elif hasattr(event, "delta") and event.delta != 0:
            direction = 1 if event.delta > 0 else -1
        else:
            return

        new_value = self._current_value + (direction * self.step)
        if new_value >= self.max_value: new_value = self.min_value
        if new_value < self.min_value: new_value = self.max_value - self.step
        self.set(new_value, invoke_callback=True, click_delta=direction)

    def set(self, value, invoke_callback=False, click_delta=0):
        """Unified setter method. Updates registers and repaints pointers."""
        old_value = self._current_value
        target_value = float(value)

        if target_value >= self.max_value:
            target_value = self.min_value
        elif target_value < self.min_value:
            target_value = self.max_value - self.step

        self._current_value = target_value

        if self.canvas.winfo_exists():
            self._draw_dial()

        if invoke_callback and self._command is not None and self._state == "normal":
            if click_delta != 0:
                self._command(click_delta)
            else:
                calc_delta = self._current_value - old_value
                if abs(calc_delta) > (self.max_value * 0.5):
                    calc_delta = -calc_delta if calc_delta > 0 else calc_delta
                self._command(int(round(calc_delta)))

    def get(self):
        return self._current_value


import customtkinter as ctk

# Ensure cross-module tracking points find your local widget packages
from sCTkDial import sCTkDial
from sCTkFrame import sCTkFrame
from sCTkComboBox import sCTkComboBox
from sCTkCheckBox import sCTkCheckBox
from sCTkSlider import sCTkSlider  # INTEGRATED: Your framework slider module!
from sCTkLabelSecondary import sCTkLabelSecondary
from sCTkButtonPrimary import sCTkButtonPrimary

# Global frequency tracking register (14.032.000 MHz baseline default)
current_frequency_hz = 14032000


def refresh_frequency_display():
    """Formats raw integers into standard 14.032.000 layout specifications."""
    global current_frequency_hz
    freq_str = f"{current_frequency_hz:08d}"
    formatted_freq = f"{freq_str[-8:-6]}.{freq_str[-6:-3]}.{freq_str[-3:]}"
    if formatted_freq.startswith("."): formatted_freq = formatted_freq[1:]
    vfo_display.configure(text=formatted_freq)


def on_vfo_dial_rotated(clicks_delta):
    """Unified event-driven callback called automatically on every valid scroll/drag change."""
    global current_frequency_hz
    current_frequency_hz += clicks_delta * 100
    current_frequency_hz = max(0, current_frequency_hz)
    refresh_frequency_display()


# Custom accelerated override routines (Moves physical dial 2 notches)
def my_custom_left_click():
    global current_frequency_hz
    if tuning_dial.cget("state") == "disabled": return
    new_dial_val = tuning_dial.get() - (2.0 * tuning_dial.step)
    tuning_dial.set(new_dial_val, invoke_callback=True, click_delta=-2)


def my_custom_right_click():
    global current_frequency_hz
    if tuning_dial.cget("state") == "disabled": return
    new_dial_val = tuning_dial.get() + (2.0 * tuning_dial.step)
    tuning_dial.set(new_dial_val, invoke_callback=True, click_delta=2)


# =====================================================================
# SYSTEM ASSEMBLY TEST BENCH RUNNER MAIN
# =====================================================================
if __name__ == "__main__":
    app = ctk.CTk()  # Kept strictly untouched
    app.title("sCTk Event-Driven VFO Encoder Deck")
    app.geometry("460x620")
    app.configure(fg_color=("#F1F5F9", "#1C1C1C"))

    # Parent frame layer updated to sCTkFrame
    dashboard_panel = sCTkFrame(app, fg_color="transparent", border_width=0)
    dashboard_panel.pack(padx=20, pady=10, fill="both", expand=True)

    # 1. MOUNT: Primary VFO Frequency Readout Box (sCTkLabelSecondary)
    vfo_display = sCTkLabelSecondary(dashboard_panel, text="14.032.000", font=("Arial", 36, "bold"),
                                     text_color=("#1A4375", "#FF9100"))
    vfo_display.pack(pady=5)

    # 2. MOUNT: The Rotary Tuning Encoder Knob Widget
    tuning_dial = sCTkDial(
        dashboard_panel,
        min_value=0.0, max_value=24.0, step=1.0, divisions=24,
        command=on_vfo_dial_rotated,
        left_click_callback=my_custom_left_click,
        right_click_callback=my_custom_right_click,
        diameter=130
    )
    tuning_dial.pack(pady=5)
    tuning_dial.set(0.0)

    # 3. MOUNT: Control Panel Box for live configuration tweaks (sCTkFrame)
    control_frame = sCTkFrame(dashboard_panel, fg_color=("#E2E8F0", "#262626"), corner_radius=6)
    control_frame.pack(fill="x", padx=30, pady=5)

    # --- A. Sensitivity Regulator Combobox (sCTkLabelSecondary & sCTkComboBox) ---
    lbl_sens = sCTkLabelSecondary(control_frame, text="Sensitivity Delay:", font=("Arial", 11, "bold"))
    lbl_sens.grid(row=0, column=0, padx=15, pady=5, sticky="w")


    def on_sensitivity_changed(choice):
        numeric_part = choice.split()
        ms_value = int(numeric_part.replace("ms", ""))
        tuning_dial.set_scroll_cooldown(ms_value)


    sens_dropdown = sCTkComboBox(control_frame,
                                 values=["30ms (Fast)", "60ms (Normal)", "120ms (Slow)", "250ms (Heavy)"],
                                 command=on_sensitivity_changed, width=150)
    sens_dropdown.grid(row=0, column=1, padx=15, pady=5, sticky="e")
    sens_dropdown.set("60ms (Normal)")

    # --- B. Live Divisions Scale Regulator Combobox (sCTkLabelSecondary & sCTkComboBox) ---
    lbl_divs = sCTkLabelSecondary(control_frame, text="Dial Scale Ticks:", font=("Arial", 11, "bold"))
    lbl_divs.grid(row=1, column=0, padx=15, pady=5, sticky="w")


    def on_divisions_changed(choice):
        div_count = int(choice.split())
        tuning_dial.divisions = div_count
        tuning_dial.max_value = float(div_count)
        tuning_dial.set(0.0)


    divs_dropdown = sCTkComboBox(control_frame,
                                 values=["12 Ticks", "24 Ticks (Default)", "50 Ticks (Fine)", "100 Ticks (Dense)"],
                                 command=on_divisions_changed, width=150)
    divs_dropdown.grid(row=1, column=1, padx=15, pady=5, sticky="e")
    divs_dropdown.set("24 Ticks (Default)")

    # --- C. Live Geometry Size Diameter Constraint Slider (MIGRATED: sCTkLabelSecondary & sCTkSlider) ---
    lbl_size = sCTkLabelSecondary(control_frame, text="Knob Diameter Size:", font=("Arial", 11, "bold"))
    lbl_size.grid(row=2, column=0, padx=15, pady=5, sticky="w")


    def on_diameter_slider_moved(val):
        tuning_dial.configure(diameter=int(val))


    # Fully integrated your custom framework slider element cleanly
    size_slider = sCTkSlider(control_frame, from_=80, to=180, number_of_steps=10, command=on_diameter_slider_moved,
                             width=150)
    size_slider.grid(row=2, column=1, padx=15, pady=5, sticky="e")
    size_slider.set(130)

    # --- D. Direct Framework Operational State Switcher Option (sCTkLabelSecondary & sCTkComboBox) ---
    lbl_state = sCTkLabelSecondary(control_frame, text="Component State:", font=("Arial", 11, "bold"))
    lbl_state.grid(row=3, column=0, padx=15, pady=5, sticky="w")


    def on_state_toggle_changed(choice):
        target_state = "normal" if "Normal" in choice else "disabled"
        tuning_dial.configure(state=target_state)


    state_dropdown = sCTkComboBox(control_frame, values=["Normal State (Active)", "Disabled State (Locked)"],
                                  command=on_state_toggle_changed, width=150)
    state_dropdown.grid(row=3, column=1, padx=15, pady=5, sticky="e")
    state_dropdown.set("Normal State (Active)")


    # --- E. DYNAMIC CUSTOM EVENT ROUTING CONTROLLER CHECKBOX (sCTkCheckBox) ---
    def on_routing_mode_toggled():
        use_external = bool(check_routing.get())
        if use_external:
            tuning_dial._left_click_callback = my_custom_left_click
            tuning_dial._right_click_callback = my_custom_right_click
        else:
            tuning_dial._left_click_callback = None
            tuning_dial._right_click_callback = None


    check_routing = sCTkCheckBox(control_frame, text="Enable External Click Callbacks (Fast Tune x2)",
                                 command=on_routing_mode_toggled, font=("Arial", 11))
    check_routing.grid(row=4, column=0, columnspan=2, padx=15, pady=8, sticky="w")
    check_routing.select()


    # 4. Add an on-the-fly theme switcher button to check layout color flips live (sCTkButtonPrimary)
    def toggle_theme():
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")


    theme_btn = sCTkButtonPrimary(app, text="Toggle Light/Dark Theme", command=toggle_theme)
    theme_btn.pack(pady=10)

    app.mainloop()


