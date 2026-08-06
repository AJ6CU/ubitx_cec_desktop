#!/usr/bin/python3
"""
ThemeableWidget

The primary base structural abstraction class supporting dynamic dictionary property injections.
Handles initialization property filtering and universal state cascades automatically.
"""
import tkinter as tk
import customtkinter as ctk


class ThemeableWidget:
    def __init__(self, theme_defaults: dict, component_kw: dict):
        """
        Sanitizes constructor argument dictionaries dynamically against
        incoming overrides using the merge pipeline operator.
        """
        # Combine the user arguments and defaults
        combined = theme_defaults | component_kw

        # Pop out non-standard map configurations globally so they NEVER leak down to CTk widgets!
        self._custom_disabled_map = combined.pop("disabled_map", theme_defaults.get("disabled_map", {}))
        self._custom_pressed_map = combined.pop("pressed_map", theme_defaults.get("pressed_map", {}))
        self._custom_alarm_map = combined.pop("alarm_map", theme_defaults.get("alarm_map", {}))

        # Capture a clean reference of the defaults for fallback tracking
        self._local_defaults = theme_defaults

        # Store the sanitized keywords array safely for super().__init__() passes
        self.final_kw = combined
        self._custom_current_state = "normal"

    def get_state(self) -> str:
        """Universal layout state validation variable lookup track token."""
        return getattr(self, "_custom_current_state", "normal")

    def state(self, mode: str):
        """
        UNIVERSAL STATE CONTROLLER fallback loop engine.
        Natively handles basic widget locks, rotates dynamically through supported color properties,
        and cascades execution paths recursively down to child nodes automatically via duck typing.
        """
        mode = mode.lower()
        is_disabled = mode == "disabled"
        target_state = "disabled" if is_disabled else "normal"

        # 🔄 1. EXCEPTION BUILD: Force deep component locking via native unwrapped tk.Entry calls!
        # This completely freezes typing, echoes, and backspaces instantly at the core layer.
        if hasattr(self, "_entry"):
            try:
                tk.Entry.configure(self._entry, state=target_state)
            except Exception:
                pass

        # 2. Update native interactive widget state safely (only on items supporting interactive blocks)
        # We explicitly skip basic text tags or structural cards to prevent configuration lockouts
        if hasattr(self, "configure") and self.__class__.__name__ not in ("sCTkLabelPrimary", "sCTkLabelSecondary",
                                                                          "sCTkLabelTertiary", "sCTkFrame",
                                                                          "sCTkFrameOutlined"):
            try:
                self.configure(state=target_state)
            except Exception:
                pass

        # Core color key target catalog track paths
        color_keys = ("fg_color", "border_color", "text_color", "button_color",
                      "hover_color", "button_hover_color", "scrollbar_button_color", "scrollbar_button_hover_color")

        # 3. Dynamic Reflection Loop: Apply look changes securely without hardcoded class-specific dependencies
        if is_disabled:
            for key in color_keys:
                if key in self._custom_disabled_map:
                    try:
                        self.configure(**{key: self._custom_disabled_map[key]})
                    except Exception:
                        pass
            self._custom_current_state = "disabled"
        else:
            for key in color_keys:
                # Check for active custom values fed via runtime constructor overrides first, then class defaults
                active_val = self.final_kw.get(key, self._local_defaults.get(key))
                if active_val is not None:
                    try:
                        self.configure(**{key: active_val})
                    except Exception:
                        pass
            self._custom_current_state = "normal"

        # 🚀 4. RECURSIVE CASCADING: Loop over all widgets inside this layout node via duck typing
        if hasattr(self, "winfo_children"):
            for child in self.winfo_children():
                if hasattr(child, "winfo_children"):
                    for inner_child in child.winfo_children():
                        if hasattr(inner_child, "state") and callable(getattr(inner_child, "state")):
                            try:
                                inner_child.state(mode)
                            except Exception:
                                pass

                if hasattr(child, "state") and callable(getattr(child, "state")):
                    try:
                        child.state(mode)
                    except Exception:
                        pass
