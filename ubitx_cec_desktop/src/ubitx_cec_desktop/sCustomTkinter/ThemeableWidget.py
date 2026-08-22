#!/usr/bin/python3
"""
ThemeableWidget - Centralized Theme Management and Global Structural Enforcement
"""
#!/usr/bin/python3
import os
import json
import customtkinter as ctk

# 🛠️ GLOBAL JSON LOADER (Runs only once when the application boots)
THEME_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sCTkThemes.json")

try:
    with open(THEME_FILE_PATH, "r", encoding="utf-8") as file:
        GLOBAL_THEME_REGISTRY = json.load(file)
except Exception as err:
    raise FileNotFoundError(
        f"CRITICAL SYSTEM BREAKDOWN: The centralized theme configuration file "
        f"'{THEME_FILE_PATH}' could not be located or parsed. "
        f"Underlying error feed: {err}."
    )


class ThemeableWidget:
    def __init__(self, kwargs: dict):
        """
        Shared base mixin that resolves global theme lookups via introspection,
        extracts styling options, handles nested map sanitization, and filters
        custom layout properties to prevent native framework validation failures.
        """
        class_name = self.__class__.__name__

        theme_defaults = GLOBAL_THEME_REGISTRY.get(class_name)
        if theme_defaults is None:
            theme_defaults = {}

        # ✅ GLOBAL CORRUPTION GUARD
        if not isinstance(theme_defaults, dict):
            raise KeyError(
                f"CRITICAL STYLING EXCEPTION: The themes.json configuration registry is corrupted. "
                f"Expected a dictionary mapping entry for widget type: '{class_name}'..."
            )

        # ✅ GLOBAL UNRESOLVED NULL TRAFFIC INTERCEPTOR
        for style_key, style_value in theme_defaults.items():
            if isinstance(style_value, dict):
                for sub_key, sub_value in style_value.items():
                    if sub_value is None:
                        raise ValueError(
                            f"CRITICAL CONFIGURATION ERROR: Unresolved theme parameter encountered! "
                            f"Inside themes.json -> ['{class_name}']['{style_key}']['{sub_key}'] evaluates to None."
                        )
            elif style_value is None:
                raise ValueError(
                    f"CRITICAL CONFIGURATION ERROR: Unresolved theme parameter encountered! "
                    f"Inside themes.json -> ['{class_name}']['{style_key}'] evaluates to None."
                )

        # 🛡️ NESTED MAP EXTRACTION PASS (Runs first so custom vector engines capture them successfully!)
        self._widget_disabled_map = self._convert_lists_to_tuples(theme_defaults.get("disabled_map") or {})
        self._widget_pressed_map = self._convert_lists_to_tuples(theme_defaults.get("pressed_map") or {})
        self._widget_alarm_map = self._convert_lists_to_tuples(theme_defaults.get("alarm_map") or {})

        # Define block keys that should never be processed as raw framework layout arguments
        forbidden_keys = {"disabled_map", "pressed_map", "alarm_map"}

        # 🛠️ UNIVERSAL WIDGET KEYWORD FILTER GUARD
        CUSTOM_VECTOR_KEYS = {
            "dial_color", "shadow_color", "text_color", "pointer_color",
            "pointer_glow_color", "disabled_text_color", "disabled_dial_color",
            "disabled_dimple_glow", "diameter"
        }

        self.final_kw = {}

        # 1. Load global configuration file defaults (Filtering out custom layout keys)
        for key, value in theme_defaults.items():
            if key not in forbidden_keys and key not in CUSTOM_VECTOR_KEYS:
                self.final_kw[key] = self._sanitize_value(key, value)

        # 2. Layer direct inline runtime keyword modifications over the top
        for key, value in kwargs.items():
            if value is not None and key not in forbidden_keys and key not in CUSTOM_VECTOR_KEYS:
                self.final_kw[key] = self._sanitize_value(key, value)

    def apply_theme(self):
        """
        Explicit execution block called AFTER parent class initialization
        to forcefully override any layout defaults embedded within baseui layers.
        """
        if hasattr(self, "configure"):
            # Direct multi-property injection override pass
            self.configure(**self.final_kw)

    def _convert_lists_to_tuples(self, target_dict: dict) -> dict:
        """Helper to convert dictionary color lists back into CustomTkinter friendly tuples."""
        return {k: tuple(v) if isinstance(v, list) and len(v) == 2 else v for k, v in target_dict.items()}

    def _sanitize_value(self, key, value):
        """
        UNIVERSAL SANITIZER: Turns JSON lists [] back into Python tuples (),
        while catching and flattening transparency settings to keep CustomTkinter from crashing.
        """
        if isinstance(value, list):
            # 🛠️ THE TRANSPARENCY FIX: If the list is ["transparent", "transparent"], flatten it to a single string
            if len(value) == 2 and value[0] == "transparent":
                return "transparent"

            return tuple(value)

        # Fallback check just in case it was already pre-processed as a tuple
        if isinstance(value, tuple) and len(value) == 2 and value[0] == "transparent":
            return "transparent"

        return value

    def configure(self, require_redraw=False, **kwargs):
        """
        Global Framework Interceptor.
        Safely tracks state modifications across ALL custom sCTk widgets,
        automatically applying the correct text legibility configurations.
        """
        if "state" in kwargs:
            self._state = kwargs.pop("state")

            if self._state == "disabled" and hasattr(self, "_widget_disabled_map"):
                disabled_fg = self._widget_disabled_map.get("text_color")
                if disabled_fg and hasattr(self, "configure"):
                    if hasattr(super(), "configure"):
                        # Safe conversion verification
                        if isinstance(disabled_fg, list):
                            disabled_fg = tuple(disabled_fg)
                        super().configure(text_color=disabled_fg)
            elif self._state == "normal" and hasattr(self, "final_kw"):
                normal_fg = self.final_kw.get("text_color")
                if normal_fg and hasattr(self, "configure"):
                    if hasattr(super(), "configure"):
                        if isinstance(normal_fg, list):
                            normal_fg = tuple(normal_fg)
                        super().configure(text_color=normal_fg)

            require_redraw = True

        # 🛡️ FIXED MRO CHAIN HIJACK:
        if hasattr(super(), "configure"):
            return super().configure(require_redraw=require_redraw, **kwargs)

        return None

    def cget(self, attribute_name: str) -> any:
        """Exposes the state property to standard framework queries uniformly."""
        if attribute_name == "state":
            return getattr(self, "_state", "normal")
        if hasattr(super(), "cget"):
            return super().cget(attribute_name)
        return None

    def _resolve_color(self, color_value):
        """
        Helper method to safely pull the singular valid string hex color
        from a CustomTkinter (Light, Dark) mode theme tuple/list.
        """
        if isinstance(color_value, (tuple, list)):
            # 0 for Light Mode, 1 for Dark Mode
            mode_idx = 1 if ctk.get_appearance_mode() == "Dark" else 0
            return color_value[mode_idx]
        return color_value
