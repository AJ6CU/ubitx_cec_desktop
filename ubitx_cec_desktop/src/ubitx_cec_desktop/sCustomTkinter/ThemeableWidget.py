import customtkinter as ctk

class ThemeableWidget(object):
    def __init__(self, theme_defaults: dict, component_kw: dict):
        """Centralized theme parsing and state setup."""
        # 1. Isolate the custom disabled map safely
        self._custom_disabled_map = theme_defaults.get("disabled_map", {})

        # 2. FIX: Create a sanitized copy of theme_defaults by popping ALL custom states.
        # This completely shields CustomTkinter's constructor from any non-standard keys!
        clean_theme = theme_defaults.copy()
        for custom_state_key in ("disabled_map", "pressed_map", "alarm_map", "hover_map"):
            clean_theme.pop(custom_state_key, None)

        # 3. Protect memory reference chains from bleeding positional arguments
        clean_component_kw = component_kw.copy()
        for duplicate_key in ("master", "parent", "root"):
            clean_component_kw.pop(duplicate_key, None)

        # 4. Merge default styles with sanitized keyword arguments via pipe operator
        self.final_kw = clean_theme | clean_component_kw

        # 5. Initialize the state tracker string right here safely!
        self._custom_current_state = "normal"

    def get_state(self) -> str:
        """
        Safely returns the true current status of the widget.
        Returns: 'normal' or 'disabled'
        """
        return getattr(self, "_custom_current_state", "normal")
