#!/usr/bin/python3
"""
sCTkDialContinuousbo

Optimized Pygubu Builder Object for the sCTkDialContinuous custom widget.
Provides lightweight, high-utility metadata mappings for Pygubu Designer layout setups.
"""
import pygubu
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property
)

# Import the native custom child class directly out of your unified file
from sCTkDial import sCTkDialContinuous

widget_namespace = "sCTkDialContinuous"
widget_classname = "sCTkDialContinuous"
builder_namespace = "custom_widgets"
section_name = "sCustomTkinter"
builder_id = f"{builder_namespace}.{widget_classname}"


class sCTkDialContinuousBO(BuilderObject):
    class_ = sCTkDialContinuous

    # Enforce class parameters to preserve inspector selection focus tree links
    classname = widget_classname
    _code_classname = widget_classname
    container = False

    # Combined configuration registry arrays
    OPTIONS_STANDARD = ("width", "height", "state")
    OPTIONS_CUSTOM = ("divisions", "diameter")
    properties = OPTIONS_STANDARD + OPTIONS_CUSTOM

    def realize(self, parent, *args, **kwargs):
        """Pygubu Lifecycle Realize Intercept."""
        props_map = self.wmeta.properties if hasattr(self, "wmeta") else {}

        diameter_val = props_map.get("diameter", None)
        divisions_val = props_map.get("divisions", 24)

        # Calculate target boundary sizes with an active layout fallback threshold
        w = int(diameter_val) if (diameter_val and str(diameter_val).strip()) else 120

        # Hard-inject safe parameters into the layout manager registers before boot
        if hasattr(self, "wmeta") and self.wmeta:
            self.wmeta.properties["width"] = str(w)
            self.wmeta.properties["height"] = str(w)

        # Instantiate the custom component chassis forwarding all positioning parameters
        widget = super().realize(parent, *args, **kwargs)

        if widget:
            widget._divisions = int(divisions_val) if divisions_val else 24
            if diameter_val and str(diameter_val).strip():
                widget.configure(diameter=int(diameter_val))

            # Freeze propagation weights inside Pygubu's editor preview layout panels
            widget.pack_propagate(False)
            widget.grid_propagate(False)

            # Clamp CustomTkinter's private internal canvas layer to freeze empty box blowouts
            if hasattr(widget, "_canvas") and widget._canvas is not None:
                widget._canvas.configure(width=w, height=w)

            # Force an explicit final vector graph layout repaint pass to guarantee visibility
            widget._draw_dial_base()

        return widget


# =====================================================================
# RAW MODULE-LEVEL PYGUBU REGISTRATION LEDGER
# Matches your working sCTkBarSMeterbo module registration blueprint.
# =====================================================================

# 1. Register the builder class object explicitly into Pygubu's workspace parsing tree
register_widget(builder_id, sCTkDialContinuousBO, widget_classname, ("ttk", section_name))

# 2. Register Custom Properties panel elements to display in the Designer tray panel
register_custom_property(
    builder_id,
    "width",
    "naturalnumber",
    # help="Set total width in pixels of the canvas boundary box viewport frame."
)

register_custom_property(
    builder_id,
    "height",
    "naturalnumber",
    # help="Set total height in pixels of the canvas boundary box viewport frame."
)

register_custom_property(
    builder_id,
    "divisions",
    "naturalnumber",
    # default_value=24,
    # help="Number of detented visual tracking indices inside a single 360-degree rotation turn."
)

register_custom_property(
    builder_id,
    "diameter",
    "naturalnumber",
    # default_value=120,
    # help="Symmetrical diameter size constraint in pixels forcing a perfect 1:1 circle."
)
