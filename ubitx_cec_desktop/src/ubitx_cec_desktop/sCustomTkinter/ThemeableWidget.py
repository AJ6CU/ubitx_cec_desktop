#!/usr/bin/python3
"""
ThemeableWidget - Centralized Theme Management and Global Structural Enforcement
"""
import os

try:
    from sCTkThemes import THEME_DEFAULTS
except (ImportError, ModuleNotFoundError) as err:
    # Stop execution loops immediately if the shared theme config module cannot be resolved
    raise FileNotFoundError(
        f"CRITICAL SYSTEM BREAKDOWN: The mandatory theme stylesheet tracking file "
        f"'sCTkThemes.py' could not be found or resolved within the local python path space. "
        f"Underlying tracking loop error feed: {err}. Please restore this module to your "
        f"active project utilities folder to re-enable custom widgets compilation blocks."
    )


class ThemeableWidget:
    def __init__(self, theme_defaults: dict, kwargs: dict):
        """
        Shared base mixin that resolves global theme dictionary lookups,
        extracts styling options, and aggressively enforces complete key configurations.
        """
        # GLOBAL CORRUPTION GUARD
        # Intercept and block initialization immediately if a widget's core dictionary map
        # is missing or evaluates to an empty object.
        if not theme_defaults or not isinstance(theme_defaults, dict):
            class_name = self.__class__.__name__
            raise KeyError(
                f"CRITICAL STYLING EXCEPTION: The sCTkThemes configuration registry is corrupted. "
                f"Could not locate a valid section or mapping entry dictionary for widget type: '{class_name}'. "
                f"Please verify your 'THEME_DEFAULTS' definition properties."
            )

        # GLOBAL UNRESOLVED NULL TRAFFIC INTERCEPTOR
        # Aggressively scan the targeted theme dictionary section. If any configuration field
        # resolves to 'None', throw a structured exception right now to protect the application UI.
        for style_key, style_value in theme_defaults.items():
            if isinstance(style_value, dict):
                for sub_key, sub_value in style_value.items():
                    if sub_value is None:
                        class_name = self.__class__.__name__
                        raise ValueError(
                            f"CRITICAL CONFIGURATION ERROR: Unresolved theme parameter encountered! "
                            f"Inside sCTkThemes.py -> ['{class_name}']['{style_key}']['{sub_key}'] evaluates to None. "
                            f"Every structural custom theme parameter property must contain an explicit hexadecimal, "
                            f"string, or list mapping profile token before initialization passes can execute."
                        )
            elif style_value is None:
                class_name = self.__class__.__name__
                raise ValueError(
                    f"CRITICAL CONFIGURATION ERROR: Unresolved theme parameter encountered! "
                    f"Inside sCTkThemes.py -> ['{class_name}']['{style_key}'] evaluates to None. "
                    f"Every structural custom theme parameter property must contain an explicit hexadecimal, "
                    f"string, or list mapping profile token before initialization passes can execute."
                )

        # 🛡️ GLOBAL SANITIZATION RESCUE
        # Isolate special tracking layers into private class properties, then strip them completely
        # from final_kw so they can never contaminate native CustomTkinter base constructor passes.
        self._widget_disabled_map = theme_defaults.get("disabled_map") or {}
        self._widget_pressed_map = theme_defaults.get("pressed_map") or {}
        self._widget_alarm_map = theme_defaults.get("alarm_map") or {}

        # Define internal forbidden key tags to strip automatically
        forbidden_keys = {"disabled_map", "pressed_map", "alarm_map"}

        self.final_kw = {}

        # Load the global theme mapping defaults first (filtering out internal tracking keys)
        for key, value in theme_defaults.items():
            if key not in forbidden_keys:
                self.final_kw[key] = value

        # Layer any direct inline runtime configuration overrides over the top
        for key, value in kwargs.items():
            if value is not None and key not in forbidden_keys:
                self.final_kw[key] = value
