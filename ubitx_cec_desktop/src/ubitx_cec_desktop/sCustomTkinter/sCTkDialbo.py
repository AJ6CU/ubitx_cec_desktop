#!/usr/bin/python3
"""
sCTkDialbo

Unified Pygubu Builder Objects for the complete sCTkDial custom widget suite.
Houses sCTkDialContinuous, sCTkDialRange, and sCTkDialSelector builders
side-by-side, sharing the metadata configuration pipeline.
"""
import pygubu
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property
)

# Import the native custom classes directly out of your single-file source module
from sCTkDial import sCTkDialContinuous, sCTkDialRange, sCTkDialSelector

builder_namespace = "custom_widgets"
section_name = "sCustomTkinter"


# =====================================================================
# 1. BUILDER OBJECT: INFINITE FLYWHEEL TUNING ENCODER (CONTINUOUS)
# =====================================================================
class sCTkDialContinuousBO(BuilderObject):
    class_ = sCTkDialContinuous
    classname = "sCTkDialContinuous"
    _code_classname = "sCTkDialContinuous"
    container = False

    OPTIONS_STANDARD = ("width", "height", "state")
    OPTIONS_CUSTOM = ("divisions", "diameter")
    properties = OPTIONS_STANDARD + OPTIONS_CUSTOM

    def realize(self, parent, *args, **kwargs):
        props_map = self.wmeta.properties if hasattr(self, "wmeta") else {}
        diameter_val = props_map.get("diameter", None)
        divisions_val = props_map.get("divisions", 24)

        w = int(diameter_val) if (diameter_val and str(diameter_val).strip()) else 120

        if hasattr(self, "wmeta") and self.wmeta:
            self.wmeta.properties["width"] = str(w)
            self.wmeta.properties["height"] = str(w)

        widget = super().realize(parent, *args, **kwargs)

        if widget:
            widget._divisions = int(divisions_val) if divisions_val else 24
            if diameter_val and str(diameter_val).strip():
                widget.configure(diameter=int(diameter_val))

            widget.pack_propagate(False)
            widget.grid_propagate(False)

            if hasattr(widget, "_canvas") and widget._canvas is not None:
                widget._canvas.configure(width=w, height=w)

            widget._draw_dial_base()

        return widget


# =====================================================================
# 2. BUILDER OBJECT: HARD END-STOP POTENTIOMETER (RANGE)
# =====================================================================
class sCTkDialRangeBO(BuilderObject):
    class_ = sCTkDialRange
    classname = "sCTkDialRange"
    _code_classname = "sCTkDialRange"
    container = False

    OPTIONS_STANDARD = ("width", "height", "state")
    OPTIONS_CUSTOM = ("from_", "to", "divisions", "diameter", "arc_angle")
    properties = OPTIONS_STANDARD + OPTIONS_CUSTOM

    def realize(self, parent, *args, **kwargs):
        props_map = self.wmeta.properties if hasattr(self, "wmeta") else {}
        diameter_val = props_map.get("diameter", None)
        divisions_val = props_map.get("divisions", 5)
        from_val = props_map.get("from_", 0)
        to_val = props_map.get("to", 100)
        arc_val = props_map.get("arc_angle", 270)

        w = int(diameter_val) if (diameter_val and str(diameter_val).strip()) else 120

        if hasattr(self, "wmeta") and self.wmeta:
            self.wmeta.properties["width"] = str(w)
            self.wmeta.properties["height"] = str(w)

        widget = super().realize(parent, *args, **kwargs)

        if widget:
            widget._from = int(from_val)
            widget._to = int(to_val)
            widget._divisions = int(divisions_val) if divisions_val else 5
            widget._arc_angle = float(arc_val)

            if diameter_val and str(diameter_val).strip():
                widget.configure(diameter=int(diameter_val))

            widget.pack_propagate(False)
            widget.grid_propagate(False)

            if hasattr(widget, "_canvas") and widget._canvas is not None:
                widget._canvas.configure(width=w, height=w)

            widget._draw_dial_base()

        return widget


# =====================================================================
# 3. BUILDER OBJECT: DISCRETE SWITCH SELECTOR (SELECTOR)
# =====================================================================
class sCTkDialSelectorBO(BuilderObject):
    class_ = sCTkDialSelector
    classname = "sCTkDialSelector"
    _code_classname = "sCTkDialSelector"
    container = False

    OPTIONS_STANDARD = ("width", "height", "state")
    OPTIONS_CUSTOM = ("diameter", "arc_angle")  # Note: Labels handles lists, which are usually initialized in code
    properties = OPTIONS_STANDARD + OPTIONS_CUSTOM

    def realize(self, parent, *args, **kwargs):
        props_map = self.wmeta.properties if hasattr(self, "wmeta") else {}
        diameter_val = props_map.get("diameter", None)
        arc_val = props_map.get("arc_angle", 270)

        w = int(diameter_val) if (diameter_val and str(diameter_val).strip()) else 120

        if hasattr(self, "wmeta") and self.wmeta:
            self.wmeta.properties["width"] = str(w)
            self.wmeta.properties["height"] = str(w)

        widget = super().realize(parent, *args, **kwargs)

        if widget:
            widget._arc_angle = float(arc_val)
            if diameter_val and str(diameter_val).strip():
                widget.configure(diameter=int(diameter_val))

            widget.pack_propagate(False)
            widget.grid_propagate(False)

            if hasattr(widget, "_canvas") and widget._canvas is not None:
                widget._canvas.configure(width=w, height=w)

            widget._draw_dial_base()

        return widget
# =====================================================================
# UNIFIED MODULE-LEVEL PYGUBU REGISTRATION LEDGER
# Registers all three semantic variations simultaneously inside the palette.
# =====================================================================

# --- 1. CONTINUOUS VFO ENCODER MATRIX REGISTRY ---
id_continuous = f"{builder_namespace}.sCTkDialContinuous"
register_widget(id_continuous, sCTkDialContinuousBO, "sCTkDialContinuous", ("ttk", section_name))
register_custom_property(id_continuous, "width", "naturalnumber", help="Width in pixels.")
register_custom_property(id_continuous, "height", "naturalnumber", help="Height in pixels.")
register_custom_property(id_continuous, "divisions", "naturalnumber", default_value=24, help="Flywheel detents per 360 turn.")
register_custom_property(id_continuous, "diameter", "naturalnumber", default_value=120, help="Knob circle size.")

# --- 2. RANGED POTENTIOMETER MATRIX REGISTRY ---
id_range = f"{builder_namespace}.sCTkDialRange"
register_widget(id_range, sCTkDialRangeBO, "sCTkDialRange", ("ttk", section_name))
register_custom_property(id_range, "width", "naturalnumber", help="Width in pixels.")
register_custom_property(id_range, "height", "naturalnumber", help="Height in pixels.")
register_custom_property(id_range, "from_", "integer", default_value=0, help="Absolute minimum boundary limit.")
register_custom_property(id_range, "to", "integer", default_value=100, help="Absolute maximum boundary limit.")
register_custom_property(id_range, "divisions", "naturalnumber", default_value=5, help="Number of calibration tick lines drawn.")
register_custom_property(id_range, "diameter", "naturalnumber", default_value=120, help="Knob circle size.")
register_custom_property(id_range, "arc_angle", "naturalnumber", default_value=270, help="Symmetrical active arc sweep.")

# --- 3. MODE SELECTOR MATRIX REGISTRY ---
id_selector = f"{builder_namespace}.sCTkDialSelector"
register_widget(id_selector, sCTkDialSelectorBO, "sCTkDialSelector", ("ttk", section_name))
register_custom_property(id_selector, "width", "naturalnumber", help="Width in pixels.")
register_custom_property(id_selector, "height", "naturalnumber", help="Height in pixels.")
register_custom_property(id_selector, "diameter", "naturalnumber", default_value=120, help="Knob circle size.")
register_custom_property(id_selector, "arc_angle", "naturalnumber", default_value=270, help="Symmetrical active arc sweep.")
