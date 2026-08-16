#!/usr/bin/python3
"""
ThemeableWidget - Centralized Theme Management and Global Structural Enforcement
"""
import os
import customtkinter as ctk

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
        if not theme_defaults or not isinstance(theme_defaults, dict):
            class_name = self.__class__.__name__
            raise KeyError(
                f"CRITICAL STYLING EXCEPTION: The sCTkThemes configuration registry is corrupted. "
                f"Could not locate a valid section or mapping entry dictionary for widget type: '{class_name}'. "
                f"Please verify your 'THEME_DEFAULTS' definition properties."
            )

        # GLOBAL UNRESOLVED NULL TRAFFIC INTERCEPTOR
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
                    # Use a clean local lookup string loop instead of breaking MRO lines
                    if hasattr(super(), "configure"):
                        super().configure(text_color=disabled_fg)
            elif self._state == "normal" and hasattr(self, "final_kw"):
                normal_fg = self.final_kw.get("text_color")
                if normal_fg and hasattr(self, "configure"):
                    if hasattr(super(), "configure"):
                        super().configure(text_color=normal_fg)

            require_redraw = True

        # 🛡️ FIXED MRO CHAIN HIJACK:
        # Verify if the sibling class in the multiple inheritance layout track
        # actually has a valid configure() method before calling it. This ensures
        # ctk.CTkFrame.configure() runs natively, initializing the canvas mouse intercept layers!
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
        from a CustomTkinter (Light, Dark) mode theme tuple.
        """
        if isinstance(color_value, (tuple, list)):
            # 0 for Light Mode, 1 for Dark Mode
            mode_idx = 1 if ctk.get_appearance_mode() == "Dark" else 0
            return color_value[mode_idx]
        return color_value

