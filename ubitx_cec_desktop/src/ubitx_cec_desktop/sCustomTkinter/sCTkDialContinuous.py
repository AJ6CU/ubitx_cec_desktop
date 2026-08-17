from sCTkDial import sCTkDialBase

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