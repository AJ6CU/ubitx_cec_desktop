#!/usr/bin/python3
"""
sCTkDialContinuous Pygubu Builder Object

Fully calibrated layout compliance mapping script. Decouples the properties
panel selection loops inside Pygubu-Designer, forcing custom radio attributes
to display cleanly instead of falling back to a generic container Frame mask.
"""
import pygubu
from pygubu.api.v1 import (
    BuilderObject,
    register_widget,
    register_custom_property
)

# Import the native custom class
from sCTkDialContinuous import sCTkDialContinuous

widget_namespace = "sCTkDialContinuous"
widget_classname = "sCTkDialContinuous"
builder_namespace = "custom_widgets"
section_name = "sCustomTkinter"


class sCTkDialContinuousBO(BuilderObject):
    # Bind the class reference directly to the concrete continuous dial module
    class_ = sCTkDialContinuous

    # FIXED: Explicitly register standard frame bounds alongside custom parameters
    # This prevents Pygubu from treating this class as a generic container frame!
    OPTIONS_STANDARD = ("width", "height", "state")
    OPTIONS_CUSTOM = ("divisions", "diameter")

    properties = OPTIONS_STANDARD + OPTIONS_CUSTOM

    def realize(self, parent):
        """
        Pygubu Lifecycle Realize Intercept.
        Explicitly binds and constraints CustomTkinter's invisible internal composition
        layers before fluid window manager weights can blow out the display.
        """
        diameter_val = self.wproperty_dict.get("diameter", None)
        divisions_val = self.wproperty_dict.get("divisions", 24)

        # Force a baseline structural size if unassigned to keep Pygubu stable
        w = int(diameter_val) if (diameter_val and str(diameter_val).strip() != "") else 120
        h = w

        self.wproperty_dict["width"] = w
        self.wproperty_dict["height"] = h

        # Create the widget instance through the standard builder engine
        widget = super().realize(parent)

        if widget:
            # 1. Map custom properties into your active widget attributes
            widget.configure(divisions=int(divisions_val))
            if diameter_val and str(diameter_val).strip() != "":
                widget.configure(diameter=int(diameter_val))

            # 2. INTERNAL OVERRIDE: Prevent the invisible CTk composition frames from collapsing
            # or blowing out by hard-locking their inner grid weight propagation states.
            if hasattr(widget, "pack_propagate"):
                widget.pack_propagate(False)
            if hasattr(widget, "grid_propagate"):
                widget.grid_propagate(False)

            # 3. FIXED INVISIBLE LAYER CLAMP: Force CustomTkinter's private internal canvas rounding
            # frame layer to strictly lock onto your structural pixel width/height constraints!
            if hasattr(widget, "_canvas") and widget._canvas is not None:
                widget._canvas.configure(width=w, height=h)

        return widget

    def _code_get_kw(self):
        """Safely maps parameters out to clean outbound Python source generation scripts."""
        kw = super()._code_get_kw()
        for prop in self.OPTIONS_CUSTOM:
            if prop in self.wproperty_dict:
                kw[prop] = self.wproperty_dict[prop]
        return kw


# =====================================================================
# SYSTEM REGISTRATION SCHEMATICS
# =====================================================================
builder_id = f"{builder_namespace}.{widget_classname}"

# Mount component directly into Pygubu's designer layout tree selection panel
register_widget(builder_id, sCTkDialContinuousBO, widget_classname, ("ttk", section_name))

# Register Custom Properties panel elements to show up inside the Designer tray window
register_custom_property(
    builder_id,
    "width",
    "naturalnumber",
    help="Fallback custom width boundary box layout constraints."
)

register_custom_property(
    builder_id,
    "height",
    "naturalnumber",
    help="Fallback custom height boundary box layout constraints."
)

register_custom_property(
    builder_id,
    "divisions",
    "naturalnumber",
    default_value=24,
    help="Number of detented visual tracking indices inside a single 360-degree rotation turn."
)

register_custom_property(
    builder_id,
    "diameter",
    "naturalnumber",
    default_value=120,
    help="Symmetrical diameter size constraint in pixels forcing a perfect 1:1 circle."
)
