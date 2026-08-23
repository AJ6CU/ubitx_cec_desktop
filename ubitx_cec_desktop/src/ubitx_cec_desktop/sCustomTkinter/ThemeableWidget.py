#!/usr/bin/python3
"""
ThemeableWidget - Piece 1 of 2

Centralized Theme Management and Global Structural Enforcement.
Natively structures color definitions into true 2-element dark/light tracking payloads
to ensure CustomTkinter's master appearance tracker loops never drop widget listeners.
"""
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
        f"CRITICAL SYSTEM BREAKDOWN: Centralized theme file '{THEME_FILE_PATH}' "
        f"could not be parsed. Error: {err}."
    )


class ThemeableWidget:
    def __init__(self, kwargs: dict):
        """
        Shared base mixin that resolves global theme lookups via introspection,
        extracts styling options, handles nested map sanitization, and filters
        custom layout properties to prevent native framework validation failures.
        """
        class_name = self.__class__.__name__

        theme_defaults = GLOBAL_THEME_REGISTRY.get(class_name) or {}

        if not isinstance(theme_defaults, dict):
            raise KeyError(f"CRITICAL STYLING EXCEPTION: Registry corrupted for type: '{class_name}'...")

        # Global unresolved null traffic check
        for style_key, style_value in theme_defaults.items():
            if isinstance(style_value, dict):
                for sub_key, sub_value in style_value.items():
                    if sub_value is None:
                        raise ValueError(
                            f"Null theme parameter encountered at ['{class_name}']['{style_key}']['{sub_key}']")
            elif style_value is None:
                raise ValueError(f"Null theme parameter encountered at ['{class_name}']['{style_key}']")

        # Nested color map extractions
        self._widget_disabled_map = ThemeableWidget._convert_lists_to_tuples(theme_defaults.get("disabled_map") or {})
        self._widget_pressed_map = ThemeableWidget._convert_lists_to_tuples(theme_defaults.get("pressed_map") or {})
        self._widget_alarm_map = ThemeableWidget._convert_lists_to_tuples(theme_defaults.get("alarm_map") or {})

        forbidden_keys = {"disabled_map", "pressed_map", "alarm_map"}
        CUSTOM_VECTOR_KEYS = {
            "dial_color", "shadow_color", "text_color", "pointer_color",
            "pointer_glow_color", "disabled_text_color", "disabled_dial_color",
            "disabled_dimple_glow", "diameter"
        }

        self.final_kw = {}
        is_vector_widget = any(v_key in theme_defaults for v_key in ["dial_color", "pointer_color", "diameter"])

        active_vector_guards = set(CUSTOM_VECTOR_KEYS)
        if not is_vector_widget:
            active_vector_guards.discard("text_color")

        for key, value in theme_defaults.items():
            if key not in forbidden_keys and key not in active_vector_guards:
                self.final_kw[key] = ThemeableWidget._sanitize_value(key, value)

        for key, value in kwargs.items():
            if value is not None and key not in forbidden_keys and key not in active_vector_guards:
                self.final_kw[key] = ThemeableWidget._sanitize_value(key, value)

        self._state = "normal"

    def cget(self, attribute_name: str) -> any:
        """
        Global Introspective Getter Interceptor.
        Dynamically extracts and evaluates the active mode string hex tokens out
        of your customized disabled mapping layouts on every screen frame query.
        """
        attr_lower = str(attribute_name).lower()

        if attr_lower == "state":
            return getattr(self, "_state", "normal")

        current_lock = str(getattr(self, "_state", "normal")).lower()

        if current_lock == "disabled" and hasattr(self, "_widget_disabled_map"):
            if attr_lower in ("fg_color", "fgcolor"):
                val = self._widget_disabled_map.get("fg_color")
                if val is not None: return self._resolve_color(val)
            if attr_lower in ("text_color", "textcolor"):
                val = self._widget_disabled_map.get("text_color")
                if val is not None: return self._resolve_color(val)
            if attr_lower in ("border_color", "bordercolor"):
                val = self._widget_disabled_map.get("border_color")
                if val is not None: return self._resolve_color(val)

        elif current_lock == "normal" and hasattr(self, "final_kw"):
            if attr_lower in ("fg_color", "fgcolor"):
                val = self.final_kw.get("fg_color")
                if val is not None: return self._resolve_color(val)
            if attr_lower in ("text_color", "textcolor"):
                val = self.final_kw.get("text_color")
                if val is not None: return self._resolve_color(val)
            if attr_lower in ("border_color", "bordercolor"):
                val = self.final_kw.get("border_color")
                if val is not None: return self._resolve_color(val)

        if hasattr(super(), "cget"):
            return super().cget(attribute_name)
        return None

    def _set_appearance_mode(self, mode_string: str):
        """
        🛠️ REAL-TIME LIFEHOOK FORWARDER:
        Intercepts CustomTkinter's private theme updates, forwards them up the MRO,
        and forcefully re-triggers a state configuration pass. This forces disabled
        widgets to re-evaluate their single hex string parameters against the newly
        broadcasted light/dark mode string immediately!
        """
        if hasattr(super(), "_set_appearance_mode"):
            try:
                super()._set_appearance_mode(mode_string)
            except Exception:
                pass

        # 🔑 FORCED OPERATIONAL REPAINT PASS:
        # Re-run our master configure pass during a theme shift to pick up the brand
        # new light/dark hex tokens out of your maps and apply them instantly!
        current_state = str(getattr(self, "_state", "normal")).lower()
        if current_state == "disabled":
            self.configure(state="disabled")
        else:
            self.configure(state="normal")

        if hasattr(self, "_on_theme_changed"):
            try:
                self._on_theme_changed()
            except Exception:
                pass

    def apply_theme(self):
        if hasattr(self, "configure"):
            self.configure(**self.final_kw)

    @classmethod
    def _convert_lists_to_tuples(cls, target_dict: dict) -> dict:
        output = {}
        for k, v in target_dict.items():
            if isinstance(v, list) and len(v) == 2:
                if "transparent" in v:
                    output[k] = "transparent"
                else:
                    output[k] = tuple(v)
            elif isinstance(v, str) and k in ("fg_color", "text_color", "border_color"):
                if v == "transparent":
                    output[k] = "transparent"
                else:
                    output[k] = (v, v)
            else:
                output[k] = v
        return output

    @classmethod
    def _sanitize_value(cls, key, value):
        if key in ("fg_color", "text_color", "border_color", "button_color", "button_hover_color"):
            if isinstance(value, list) and len(value) == 2:
                if "transparent" in value: return "transparent"
                return tuple(value)
            if isinstance(value, tuple) and len(value) == 2:
                if "transparent" in value: return "transparent"
                return value
            if isinstance(value, str):
                if value == "transparent": return "transparent"
                return (value, value)
        if isinstance(value, list):
            return tuple(value)
        return value

    def configure(self, require_redraw=False, **kwargs):
        """
        Global Framework Interceptor.
        Resolves dictionary maps down to single, solid hex strings before passing
        them up the chain, permanently bypassing CustomTkinter's disabled tuple caching lockouts!
        """
        class_name = self.__class__.__name__

        if "state" in kwargs:
            self._state = str(kwargs.pop("state")).lower()

            if class_name in ("sCTkFrame", "sCTkScrollableFrame", "ThemeAdaptiveTestChassis"):
                actual_state = "normal"
            else:
                actual_state = self._state

            # Determine our active properties source memory map
            target_map = self._widget_disabled_map if actual_state == "disabled" else self.final_kw

            disabled_txt = target_map.get("text_color")
            disabled_fg = target_map.get("fg_color")
            disabled_border = target_map.get("border_color")

            # 🔑 THE DYNAMIC HEX RE-RESOLVER PASS FIXED:
            # CustomTkinter's disabled loops drop multi-mode tuples across theme shifts.
            # To fix this, we resolve the tuple down to a single, solid hex string token
            # matching the current system look setting right before passing it up the chain!
            if disabled_txt is not None:
                kwargs["text_color"] = self._resolve_color(disabled_txt)
            if disabled_fg is not None:
                kwargs["fg_color"] = self._resolve_color(disabled_fg)
            if disabled_border is not None:
                kwargs["border_color"] = self._resolve_color(disabled_border)

            require_redraw = True

        # Process clean property normalization overrides on real-time app reconfigures
        for k, v in list(kwargs.items()):
            if k in ("fg_color", "text_color", "border_color", "button_color", "button_hover_color"):
                if isinstance(v, str) and v != "transparent":
                    kwargs[k] = (v, v)

        if hasattr(super(), "configure"):
            if class_name in ("sCTkFrame", "sCTkScrollableFrame", "ThemeAdaptiveTestChassis"):
                kwargs.pop("state", None)
            else:
                if getattr(self, "_state", "normal") == "disabled":
                    kwargs["state"] = "disabled"

            try:
                import inspect
                sig = inspect.signature(super().configure)
                if "require_redraw" in sig.parameters:
                    return super().configure(require_redraw=require_redraw, **kwargs)
            except Exception:
                pass

            return super().configure(**kwargs)
        return None

    def _resolve_color(self, color_value):
        """Safely extracts the active string hex token based on Light/Dark appearance mode."""
        if color_value == "transparent":
            return "transparent"
        if isinstance(color_value, (tuple, list)):
            current_mode = str(ctk.get_appearance_mode()).lower()
            mode_idx = 1 if current_mode == "dark" else 0
            return color_value[mode_idx]
        return color_value





